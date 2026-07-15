# Lab Question:  AI Config Builder for Microservices

1. The datacenter AI DevOps Team is experimenting with how artificial intelligence can automatically build infrastructure configuration files. In this project, you will explore how AI can generate and validate Kubernetes YAML through automation.

2. Your task is to build a two-stage AI pipeline in config_builder.py. A user prompt will be turned into a Kubernetes Deployment YAML file, and then validated for correctness.

    a. Initialize Client: Create the OpenAI client using api_key and base_url provided under /root/.bash_profile.

    b. Function 1: generate_yaml(prompt: str, output_path: str) (The Config Generator)

        * Accept a natural-language prompt.

        * Call the OpenAI API with instructions: "Generate a valid Kubernetes Deployment YAML file for deployment for nginx. Respond ONLY with raw YAML."

        * Save the YAML text to the file path provided (/root/openaiproject/deployment.yaml).

    c. Function 2: validate_yaml(file_path: str) -> bool (The Validator)
        * Read the YAML file created at /root/openaiproject/deployment.yaml

        * Use Python's yaml module to check whether the file is syntactically valid.

    d. Main Execution:
        * Call generate_yaml() using a simple prompt ("create a deployment for nginx").

        * Call validate_yaml().

        * Print the AI's response output "VALID" if YAML is valid, otherwise print "INVALID".


# Notes:

1. Ensure you are working in /root/openaiproject.

2. Your API credentials will be available under /root/.bash_profile.

3. The final output printed must be exactly either VALID or INVALID.

4. Use temperature=0.2 and max_tokens=500 for YAML generation. Use model=openai/gpt-4.1-mini.

5. Use hardcoded values for api_key and base_url when initializing the OpenAI client or read them from environment variables via os.environ.get('OPENAI_API_KEY') and os.environ.get('OPENAI_API_BASE').

6. Before running config_builder.py, create and activate a virtual environment, then install dependencies using:

python3 -m venv venv && source venv/bin/activate && pip install openai pyyaml

7. You are allowed a maximum of 10 total requests. After this, you may hit a rate limiter.

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
*Update config_builder.py*
import os
from openai import OpenAI
import yaml

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE")
)

def generate_yaml(prompt: str, output_path: str):
    base_dir = "/root/openaiproject"
    out_full = os.path.join(base_dir, output_path) if not os.path.isabs(output_path) else output_path

    instructions = "Generate a valid Kubernetes Deployment YAML file for deployment for nginx. Respond ONLY with raw YAML."
    full_prompt = f"{prompt}: {instructions}"

    response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        temperature=0.2,
        max_tokens=500,
        messages=[
            {"role": "user", "content": full_prompt}
        ]
    )
    yaml_text = response.choices[0].message.content.strip()

    if yaml_text.startswith("```"):
        lines = yaml_text.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        yaml_text = "\n".join(lines).strip()

    with open(out_full, "w") as f:
        f.write(yaml_text)

def validate_yaml(file_path: str) -> bool:
    base_dir = "/root/openaiproject"
    full_path = os.path.join(base_dir, file_path) if not os.path.isabs(file_path) else file_path

    try:
        with open(full_path, "r") as f:
            content = f.read()
        yaml.safe_load(content)
        return True
    except Exception:
        return False

if __name__ == "__main__":
    os.chdir("/root/openaiproject")
    generate_yaml("create a deployment for nginx", "deployment.yaml")
    is_valid = validate_yaml("deployment.yaml")
    if is_valid:
        print("VALID")
    else:
        print("INVALID")

**Step 6 — Execute the Script**

```
python config_builder.py
```

**Step 7 — Verify Output**
VALID

