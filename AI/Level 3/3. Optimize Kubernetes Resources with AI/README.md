# Lab Question: AI Kubernetes Resource Optimizer

1. The devops AI Reliability team is designing intelligent tools that analyze Kubernetes workloads, detect resource bottlenecks, and automatically recommend optimized configuration changes. Your task is to build a Python-based AI Kubernetes Resource Optimizer that reads deployment YAMLs alongside production alerts, identifies CPU and memory pressure, and generates an improved resource configuration, helping engineers proactively prevent throttling and production outages.

2. Your task is to build a two-stage AI pipeline in k8s_optimizer.py that reads a K8s YAML and a metrics file, calculates an optimized resource block, and generates a commit message for the change. The files nginx-deployment.yaml (low resources) and prometheus-alert.txt (high usage) are created.

    a. Initialize Client: Create the OpenAI client using the api_key &base_url.

    b. Function 1: get_optimized_resources(yaml_content: str, alert_content: str) -> str

    * This function takes the content of both files.

    * Call the OpenAI API (as an "SRE") with a prompt: "Read the attached deployment YAML and the Prometheus alert. The app is throttling. Calculate new resources: limits.cpu = P99 + 100m, limits.memory = P99 + 50Mi. requests should match limits. Respond ONLY with the 4-line resources: YAML block (cpu/memory for requests/limits) and nothing else."

    * Return the AI's YAML block string.

    c. Function 2: generate_commit_message(original_yaml: str, new_resources: str) -> str

    * This function takes the original YAML content and the string output from Function 1.

    * Call the OpenAI API a second time (as a "Release Manager"): "Here is the original K8s YAML and the proposed new 'resources:' block. Write a one-line Git commit message that summarizes the change.

    * Return the AI's single-line commit message.

    d.Main Execution:

    * Read the content of both nginx-deployment.yaml and prometheus-alert.txt.

    * Call get_optimized_resources().

    * Call generate_commit_message() using the output from the first call.

    * print() the final one-line commit message with (Conventional Commit format) perf: ...


# Notes:

1. Ensure you are working in the /root/openaiproject folder.

2. You will be provided with an OpenAI api_key &base_url for this session under /root/.bash_profile

3. This is a two-call chain. The output of Call 1 is the input for Call 2.

4. The final output must be only the raw, single-line commit message.

5. Use temperature=0.0 & max_tokens=100 for function 1 and temperature=0.5 & max_tokens=50 for function 2. Use model="openai/gpt-4.1-mini" for both the calls.

6. Use hardcoded values for api_key and base_url when initializing the OpenAI client or read them from environment variables via os.environ.get('OPENAI_API_KEY') and os.environ.get('OPENAI_API_BASE').

7. Before running k8s_optimizer.py, create and activate a virtual environment, then install OpenAI using:

    python3 -m venv venv && source venv/bin/activate && pip install openai

8. You are allowed a maximum of 10 requests. After this, you may encounter a rate limiter error. Therefore, use your requests judiciously."

# Solution:

# Part 1: Lab Step-by-Step Guidelines

**Step 1 — Navigate to the Project Directory**

```
cd /root/openaiproject
```

**Step 2 — Create and Activate a Virtual Environment**

Run:

```
cat /root/.bash_profile # to confirm OPENAI_API_KEY and OPENAI_API_BASE
source /root/.bash_profile


```

**Step 3 — Install OpenAI SDK**

```
python3 -m venv venv && source venv/bin/activate && pip install openai
```

**Step 4 — Open the Python File**
*Update k8s_optimizer.py*
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE")
)

def get_optimized_resources(yaml_content: str, alert_content: str) -> str:
    prompt = (
        "Read the attached deployment YAML and the Prometheus alert. The app is throttling. "
        "Calculate new resources: limits.cpu = P99 + 100m, limits.memory = P99 + 50Mi. "
        "requests should match limits. Respond ONLY with the 4-line resources: YAML block "
        "(cpu/memory for requests/limits) and nothing else.\n\n"
        f"Deployment YAML:\n{yaml_content}\n\n"
        f"Prometheus Alert:\n{alert_content}"
    )

    response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        temperature=0.0,
        max_tokens=100,
        messages=[
            {"role": "system", "content": "You are an SRE."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def generate_commit_message(original_yaml: str, new_resources: str) -> str:
    prompt = (
        "Here is the original K8s YAML and the proposed new 'resources:' block. "
        "Write a one-line Git commit message that summarizes the change.\n\n"
        f"Original YAML:\n{original_yaml}\n\n"
        f"New resources block:\n{new_resources}\n\n"
        "Use Conventional Commit format starting with perf:..."
    )

    response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        temperature=0.5,
        max_tokens=50,
        messages=[
            {"role": "system", "content": "You are a Release Manager."},
            {"role": "user", "content": prompt}
        ]
    )
    commit_msg = response.choices[0].message.content.strip()
    commit_msg = commit_msg.splitlines()[0].strip()
    return commit_msg

if __name__ == "__main__":
    os.chdir("/root/openaiproject")

    with open("nginx-deployment.yaml", "r") as f:
        yaml_content = f.read()
    with open("prometheus-alert.txt", "r") as f:
        alert_content = f.read()

    new_resources = get_optimized_resources(yaml_content, alert_content)
    final_message = generate_commit_message(yaml_content, new_resources)
    print(final_message)

**Step 6 — Execute the Script**

```
python k8s_optimizer.py
```

**Step 7 — Verify Output**

perf: increase CPU and memory resource requests and limits for nginx container