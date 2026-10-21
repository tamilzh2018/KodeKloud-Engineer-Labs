# Task: SRE Incident Response & Playbook Generator

The nautilus Automation Research Group is advancing its exploration of AI-augmented Site Reliability Engineering (SRE). Following experiments with autonomous CI/CD optimization and infrastructure auditing, the team is now testing whether AI can intelligently handle incident triage and response orchestration.

In this challenge, you will build a three-stage AI incident response pipeline in incident_pipeline.py that mimics the core workflow of a modern SRE team, from parsing alerts to understanding dependencies and generating recovery playbooks.

This experiment explores whether a large language model can act as an incident assistant, automatically interpreting alerts, identifying potential service relationships, and generating standardized mitigation procedures.

**Initialize Client:** Create the OpenAI client (model: gpt-5.6-luna) using the api_key&base_url.

**Function 1:** parse_alert(alert_content: str) -> str (The Triage Bot)

* Read the content of prometheus_alert.txt.

* Call OpenAI as a PagerDuty Bot. Ask it to parse the alert and return a JSON object with two keys: service_name (string) and symptom (string).

* Must respond ONLY with the raw JSON string.

**Function 2:** get_dependencies(service_name: str) -> str (The Service Catalog)

* Take the service_name from the JSON in Step 2.

* Call OpenAI a second time as a Service Catalog API. Ask it: "What are the direct downstream dependencies for the ''?"

* Must respond ONLY with a raw JSON list of service names (e.g., ["payment-service", "inventory-db"]).

**Function 3:** generate_playbook(symptom: str, dependencies: list) -> str (The Incident Commander)

* Take the symptom from Call 1 and the parsed list of dependencies from Call 2.

* Call OpenAI a third time as an Incident Commander. Ask it to write a step-by-step incident response playbook in Markdown.

* The playbook MUST start with a '## Problem' section that restates the exact symptom, followed by the dependencies to check.

**Main Execution:**

* Orchestrate the full pipeline: Call 1 → Parse JSON 1 → Call 2 → Parse JSON 2 → Call 3.

* print() the final Markdown playbook string from Function 3.


**Notes:**

* Ensure you are working in the /root/openaiproject directory.

* Your API credentials will be provided under /root/.bash_profile.

* This is a 3-call chain. The script must parse two different JSON outputs to feed the final call.

* The final output must be only the raw Markdown playbook.

* Use temperature=0.0 for Function 1,Function 2& temperature=0.5 for Function 3

* Use hardcoded values for api_key and base_url when initializing the OpenAI client or read them from environment variables via os.environ.get('OPENAI_API_KEY') and os.environ.get('OPENAI_API_BASE').

* Before running incident_pipeline.py, create and activate a virtual environment, then install OpenAI using:

python3 -m venv venv && source venv/bin/activate && pip install openai

* You are allowed a maximum of 10 requests. After this, you may encounter a rate limiter error, so use your calls wisely.

# Answer:
To complete the **SRE Incident Response & Playbook Generator** lab, follow the steps below to set up your environment, create the required input file, and write the Python script to orchestrate the pipeline.

---

### Step 1: Set Up the Virtual Environment and Install Dependencies

Run the following commands in your terminal to navigate to the correct directory, create and activate a Python virtual environment, and install the `openai` library:

```bash
cd /root/openaiproject
python3 -m venv venv
source venv/bin/activate
pip install openai

```

---

### Step 2: Create the Alert File (`prometheus_alert.txt`)

Ensure you have your sample alert content in `prometheus_alert.txt`. For example:

```text
ALERT HighErrorRate
  IF http_requests_total{status="500"} > 100
  FOR 5m
  ANNOTATIONS:
    summary: "High HTTP 500 error rate detected on auth-service"
    description: "The auth-service is returning an excessive number of 500 errors over the last 5 minutes."

```

---

### Step 3: Create the Python Script (`incident_pipeline.py`)

Create `incident_pipeline.py` using your preferred editor (e.g., `nano incident_pipeline.py`) and paste the following implementation:

```python
import os
import json
from openai import OpenAI

# Initialize the OpenAI client using environment variables or fallbacks
api_key = os.environ.get('OPENAI_API_KEY', 'your-api-key')
base_url = os.environ.get('OPENAI_API_BASE', 'https://api.openai.com/v1')

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

def parse_alert(alert_content: str) -> str:
    """Function 1: The Triage Bot"""
    prompt = (
        "Parse the following Prometheus alert and return a JSON object with exactly two keys: "
        "'service_name' (string) and 'symptom' (string). "
        "You must respond ONLY with the raw JSON string, no markdown formatting or extra text.\n\n"
        f"Alert:\n{alert_content}"
    )
    
    response = client.chat.completions.create(
        model="gpt-5.6-luna",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    return response.choices[0].message.content.strip()

def get_dependencies(service_name: str) -> str:
    """Function 2: The Service Catalog"""
    prompt = (
        f"What are the direct downstream dependencies for the '{service_name}'? "
        "Respond ONLY with a raw JSON list of service names (e.g., [\"payment-service\", \"inventory-db\"]), "
        "with no markdown formatting or extra text."
    )
    
    response = client.chat.completions.create(
        model="gpt-5.6-luna",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    return response.choices[0].message.content.strip()

def generate_playbook(symptom: str, dependencies: list) -> str:
    """Function 3: The Incident Commander"""
    prompt = (
        f"As an Incident Commander, write a step-by-step incident response playbook in Markdown.\n"
        f"Symptom: {symptom}\n"
        f"Dependencies to check: {dependencies}\n\n"
        f"The playbook MUST start with a '## Problem' section that restates the exact symptom ('{symptom}'), "
        f"and explicitly lists all the dependencies to check (including {dependencies}), "
        "followed by subsequent mitigation and recovery steps."
    )
    
    response = client.chat.completions.create(
        model="gpt-5.6-luna",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    # 1. Read the alert content
    with open("prometheus_alert.txt", "r") as f:
        alert_content = f.read()

    # 2. Call Function 1: Parse Alert
    json_alert_str = parse_alert(alert_content)
    alert_data = json.loads(json_alert_str)
    service_name = alert_data.get("service_name")
    symptom = alert_data.get("symptom")

    # 3. Call Function 2: Get Dependencies
    json_deps_str = get_dependencies(service_name)
    dependencies = json.loads(json_deps_str)

    # 4. Call Function 3: Generate Playbook & Print Result
    playbook_markdown = generate_playbook(symptom, dependencies)
    print(playbook_markdown)
```

---

### Step 4: Run the Pipeline

Make sure your environment variables are sourced from `/root/.bash_profile` (if required) and run the script:

```bash
source /root/.bash_profile
python3 incident_pipeline.py

```