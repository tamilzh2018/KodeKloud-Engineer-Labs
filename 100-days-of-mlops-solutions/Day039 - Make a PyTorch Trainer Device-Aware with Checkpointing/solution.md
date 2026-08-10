# Task:
The xFusionCorp Industries ML platform team is tasked with deploying fraud-detection models utilizing a compact PyTorch network. It is essential that the training script operates seamlessly on any available accelerator, whether that be CUDA GPUs in the production cluster or standard CPUs on the lab's nodes. This ensures uniform functionality across all platforms.

Currently, a preliminary version of the trainer is available at /root/code/fraud-detection/src/models/train_pytorch.py. However, this script is not device-aware; it assumes the presence of CUDA, resulting in failures upon the first tensor operation on incompatible hardware. Additionally, the device parameter logged to MLflow is hardcoded, leading to inaccuracies in reporting.

Your objective is to enhance the trainer by implementing device awareness, enabling it to accurately reflect the utilized device in the MLflow logs. Furthermore, you are required to incorporate per-epoch checkpointing to facilitate resuming long training sessions.


The MLflow tracking server is already running on port 5000. The MLflow UI button at the top of the lab can be opened to confirm—the dashboard loads with an empty pytorch-training experiment. PyTorch (CPU build) is baked into the lab image; import torch works out of the box. The host does not expose a GPU (torch.cuda.is_available() returns False).

The project layout under /root/code/fraud-detection/:

data/train.csv – The same 200-row synthetic binary-classification dataset the rest of the Training section uses.
src/models/train_pytorch.py – The trainer scaffold. The two-layer feedforward network, the optimiser, the loss function, the MLflow experiment setup, and the model-persistence call to models/fraud_model.pt are already wired; the work is confined to this file (two device corrections plus a per-epoch checkpointing TODO in the training loop).
Run the trainer once against the scaffold as-is—python src/models/train_pytorch.py—to see it fail on the first tensor operation.

The end state must include:

The script completes successfully and writes a PyTorch state-dict to /root/code/fraud-detection/models/fraud_model.pt.
One run exists in the pytorch-training experiment on MLflow, carrying params.device = "cpu" and metrics.final_loss.
No bare .cuda() calls remain anywhere in train_pytorch.py.
At least two resumable checkpoints exist under /root/code/fraud-detection/checkpoints/ (named ckpt_epoch_*.pt), each a dict carrying the model and optimiser state (so training can resume).

# Solution

Training code should run unchanged on whatever hardware it lands on — a CUDA GPU in the cluster, plain CPU in a lab. The idiom is to select a `device` **once** with `torch.device("cuda" if torch.cuda.is_available() else "cpu")` and route every tensor and the model through `.to(device)`; a bare `.cuda()` hard-fails on a CPU-only host. Long runs also need to be **resumable**: a checkpoint periodically saves the model *and* optimizer state (plus the epoch and loss) so an interrupted run restarts where it left off rather than from scratch — saving only the final weights cannot resume mid-training. This task makes the trainer device-aware and adds per-epoch checkpointing.

> As an MLOps engineer, you write device-agnostic, resumable training code so it is GPU-ready—you are not judging model quality. The data is synthetic and the loss values are incidental.

#### Follow the steps below

##### 1. Confirm the starting state.
Open the **MLflow UI** button at the top of the lab — the `pytorch-training` experiment is present and empty. From a VS Code terminal:
```
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:5000/
python3 -c "import torch; print(torch.__version__, 'cuda?', torch.cuda.is_available())"
```
A `200` confirms MLflow is reachable. The `cuda?` flag prints `False` — this host has no GPU, so the trainer must run on CPU.

##### 2. Run the draft script and observe the crash.
```
python3 /root/code/fraud-detection/src/models/train_pytorch.py
```
The script aborts before training with an error along the lines of `Torch not compiled with CUDA enabled` or `CUDA is not available`. The traceback points at `model.cuda()` in `train_pytorch.py`.

##### 3. Inspect `train_pytorch.py`.
Open `/root/code/fraud-detection/src/models/train_pytorch.py` in the VS Code editor. Two things need attention.

- `model = model.cuda()` plus `X_t.cuda()` and `y_t.cuda()` inside `main()` assume a GPU is always present. The script needs a single runtime-selected `device` handle, used consistently on every tensor and on the model.
- `mlflow.log_param("device", "cuda")` is hardcoded. Even after the device handling fires, the logged parameter will misreport what the run actually used.
- Inside the training loop, a `# TODO` marks where to write a per-epoch checkpoint — currently nothing is saved mid-run.

##### 4. Add a device handle and drop every bare `.cuda()`.
All of these edits are inside `main()`. The scaffold hard-codes the GPU on two adjacent lines:
```python
    model = FraudNet()
    model = model.cuda()
```
Replace those two lines with a runtime-selected device plus a single `.to(device)` move:
```python
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = FraudNet().to(device)
```
Then, inside the `with mlflow.start_run(...)` block, find the two tensor moves:
```python
        xb = X_t.cuda()
        yb = y_t.cuda()
```
and change them to use the same handle:
```python
        xb = X_t.to(device)
        yb = y_t.to(device)
```

##### 5. Log the actual device value.
In that same `with mlflow.start_run(...)` block, replace the hardcoded line `mlflow.log_param("device", "cuda")` with the selected handle:
```python
        mlflow.log_param("device", str(device))
```

##### 6. Author the per-epoch checkpointing (TODO inside the loop).
Replace the `# TODO` comment inside the `for epoch in range(EPOCHS)` loop with the checkpoint write. A resumable checkpoint stores everything needed to continue training — the epoch, the model weights, **and** the optimizer state (SGD's momentum buffers, etc.). Save one every 10th epoch into `CHECKPOINT_DIR`:
```python
            if epoch % 10 == 0:
                torch.save(
                    {
                        "epoch": epoch,
                        "model_state_dict": model.state_dict(),
                        "optimizer_state_dict": optimizer.state_dict(),
                        "loss": final_loss,
                    },
                    os.path.join(CHECKPOINT_DIR, f"ckpt_epoch_{epoch}.pt"),
                )
```
Save the file.

##### 7. Re-run the trainer.
```
python3 /root/code/fraud-detection/src/models/train_pytorch.py
```
The script prints a loss per epoch and finishes with `Model saved to /root/code/fraud-detection/models/fraud_model.pt`.
```
ls -l /root/code/fraud-detection/models/fraud_model.pt
ls /root/code/fraud-detection/checkpoints/
```
The `checkpoints/` directory now holds `ckpt_epoch_0.pt`, `ckpt_epoch_10.pt`, and `ckpt_epoch_20.pt`.

##### 8. Verify in the MLflow UI.
Open the **MLflow UI** button → `pytorch-training` experiment → click the `fraud-mlp` run. The **Parameters** panel reads `device = cpu`, and the **Metrics** panel lists `final_loss`. The run reflects what the lab host can actually offer.

#### References
- PyTorch — saving & loading a general checkpoint (model + optimizer state for resuming): https://pytorch.org/tutorials/beginner/saving_loading_models.html
- PyTorch CUDA semantics (`torch.cuda.is_available`, device handling): https://pytorch.org/docs/stable/notes/cuda.html
- `torch.save`: https://pytorch.org/docs/stable/generated/torch.save.html
