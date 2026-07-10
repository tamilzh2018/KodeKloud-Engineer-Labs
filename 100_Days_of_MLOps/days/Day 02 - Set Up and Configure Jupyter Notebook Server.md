# Lab Information:

A teammate has configured a JupyterLab server for the xFusionCorp Industries data science team, but the server does not behave correctly. Inspect the configuration, diagnose the issues, and start the server.

  

1. JupyterLab is already installed in the virtual environment at `/root/code/ml-env/`. The team's configuration file is at `/root/code/jupyter_lab_config.py` and is visible in the file explorer.
    
2. When JupyterLab is started, the **Jupyter UI** button at the top of the lab must open the notebook interface.
    
3. For this to work, the running server must meet the following requirements:
    
    - it listens on port `8888`;
    - it binds on `0.0.0.0` (the lab proxy cannot reach a server that is only bound on `127.0.0.1`);
    - the notebook root directory is `/root/notebooks/`, and that directory exists on disk.
4. Open the configuration file, identify every setting that prevents the requirements above from being met, and correct it. Create any missing directories.
    
5. Start JupyterLab from the virtual environment using the corrected configuration:
    

```
   source /root/code/ml-env/bin/activate
   jupyter lab --config=/root/code/jupyter_lab_config.py --allow-root --no-browser &
```

Make sure JupyterLab is running before using the button at the top of the lab.

---

# Solution
🧭 Part 1: Lab Step-by-Step Guidelines
Check jupyter_lab_config.py
- incorrect root directory
- incorrect ip address
- incorrect port

Correct config file

```python
# Jupyter configuration file for the xFusionCorp Industries data science team

# --- xFusionCorp team overrides (review before starting the server) ---
c.ServerApp.token = ''
c.ServerApp.password = ''
c.ServerApp.disable_check_xsrf = True
c.ServerApp.notebook_dir = '/root/notebooks/'
c.ServerApp.port = 8888
c.ServerApp.ip = '0.0.0.0'
```

Create required directory

```shell
mkdir -p /root/notebooks/
```

Start virtual environment

```shell
source /root/code/ml-env/bin/activate
jupyter lab --config=/root/code/jupyter_lab_config.py --allow-root --no-browser &
```
🧠 Part 2: Simple Beginner-Friendly Explanation

**What is happening in this lab?**

JupyterLab is already installed, but its configuration is incorrect.

Your job is to:

inspect the config fix bad settings create the required notebook directory start the server correctly Understanding the Required Settings

**The lab requires:**

Requirement Meaning Port 8888 Jupyter must listen on this port Bind to 0.0.0.0 Allow external access from the lab proxy Root directory /root/notebooks This is where notebooks are stored Why 127.0.0.1 Causes Problems

If Jupyter binds to:

127.0.0.1

It only accepts local connections from inside the server itself.

The lab UI button cannot reach it.

Using:

0.0.0.0

means:

“Accept connections from all network interfaces.”

This allows the lab proxy to connect.

Understanding the Config File

Typical Jupyter config lines look like:

c.ServerApp.port = 8888

Meaning:

c = configuration object ServerApp = Jupyter server settings port = listening port Why Create /root/notebooks

Jupyter needs a valid working directory.

If the folder does not exist:

startup may fail notebook browser may break

Creating it with:

mkdir -p /root/notebooks

ensures the directory exists.

Starting JupyterLab

Command:

jupyter lab --config=/root/code/jupyter_lab_config.py --allow-root --no-browser &

Explanation:

Option Purpose --config= Use the specified config file --allow-root Permit running as root --no-browser Do not open a GUI browser & Run in background
