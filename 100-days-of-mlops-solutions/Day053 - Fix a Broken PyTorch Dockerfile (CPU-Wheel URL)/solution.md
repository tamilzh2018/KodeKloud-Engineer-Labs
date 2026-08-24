# Task
The xFusionCorp Industries ML platform team has provided the PyTorch deep-learning images under the tag dl-trainer:v1. Each lab host is equipped with CPU-only capabilities, necessitating that the Dockerfile targets the CPU wheel index and that the container's default command operates effectively on hardware without a GPU. The current draft of the Dockerfile, located at /root/code/dl-docker/, does not fulfill these specifications; attempts to execute docker build are unsuccessful, and once an image is generated, the container fails to run upon startup. Your objective is to revise the Dockerfile to ensure that the command docker build -t dl-trainer:v1 . executes successfully and that the command docker run --rm dl-trainer:v1 outputs the installed torch version alongside the message cuda? False.


The Docker daemon is already running. docker version can be run in a VS Code terminal to confirm. The lab host does not expose a GPU—nvidia-smi returns command not found and torch.cuda.is_available() returns False inside any CPU-only container. Run docker build -t dl-trainer:v1 . in /root/code/dl-docker/ to see the build fail against the draft.

The project layout under /root/code/dl-docker/:

Dockerfile – A FROM, a WORKDIR, a RUN pip install line targeting torch, and a CMD that probes torch.cuda.
The end state must include:

docker images dl-trainer:v1 lists the built image.
docker run --rm dl-trainer:v1 exits 0 and prints the installed torch version alongside the CUDA flag (e.g. 2.5.0+cpu cuda? False).

# Solution

PyTorch ships different wheels for different hardware, and installing the wrong one is a classic Docker failure. This task fixes a broken PyTorch `Dockerfile` so it builds and runs on a **CPU-only** host — the reality for most CI runners and many training boxes. Two bugs: the `pip install` points at a non-existent `/whl/gpu` index (so the build fails to resolve `torch` at all), and the default `CMD` hard-asserts `torch.cuda.is_available()` (so even a successful build exits non-zero on a machine with no GPU). The fixes are to target the official CPU wheel index (`/whl/cpu`) and to replace the assertion with a diagnostic print.

> As an MLOps engineer, you match the image's dependencies to the hardware it will actually run on and don't let a container hard-fail when a GPU is absent — you are not doing any deep-learning training here. The container just imports torch and reports its version.

#### Follow the steps below

##### 1. Confirm the starting state.
From a VS Code terminal:
```
cd /root/code/dl-docker
cat Dockerfile
```
The Dockerfile points the pip install at `https://download.pytorch.org/whl/gpu` and the `CMD` asserts `torch.cuda.is_available()`.

##### 2. Run the draft build and observe the failure.
```
docker build -t dl-trainer:v1 .
```
The build aborts during the pip layer with a message along the lines of `ERROR: Could not find a version that satisfies the requirement torch`. The `whl/gpu` path is not a real PyTorch wheel index — pip gets an empty index and has no wheel to resolve.

##### 3. Fix the wheel index URL.
Open `/root/code/dl-docker/Dockerfile` in the VS Code editor. Change the pip index to the official CPU wheel path:
```dockerfile
RUN pip install --no-cache-dir \
    --index-url https://download.pytorch.org/whl/cpu \
    torch
```
Save the file.

##### 4. Re-run the build and observe the second failure.
```
docker build -t dl-trainer:v1 .
docker run --rm dl-trainer:v1
```
The build now completes (pip pulls the ~200 MB CPU wheel). The container then exits non-zero with `AssertionError: CUDA required` — the `CMD` asserts CUDA availability, which this host cannot satisfy.

##### 5. Fix the CMD.
Replace the asserting CMD with a non-fatal diagnostic that prints the torch version and the CUDA flag:
```dockerfile
CMD ["python3", "-c", "import torch; print(torch.__version__, 'cuda?', torch.cuda.is_available())"]
```
Save the file.

##### 6. Rebuild and verify.
```
docker build -t dl-trainer:v1 .
docker run --rm dl-trainer:v1
```
Output prints the installed `torch` version followed by `cuda? False` (e.g. `2.12.1+cpu cuda? False`) — the CPU wheel resolves, the container exits `0`, and the CUDA flag correctly reports `False`. (torch may also emit a harmless `Failed to initialize NumPy` warning; the version line still prints, which is all the check needs.)

##### 7. Confirm the image tag.
```
docker images dl-trainer:v1
```
The image listing shows `dl-trainer:v1` on the order of ~1.3 GB (it varies with the torch release) — still far smaller than the multi-GB CUDA-bundled install the broken `/whl/gpu` URL would have pulled.

#### References

- PyTorch install selector — the CPU wheel index `https://download.pytorch.org/whl/cpu`: https://pytorch.org/get-started/locally/
- Dockerfile reference — the `RUN` / `CMD` instructions corrected here: https://docs.docker.com/reference/dockerfile/
