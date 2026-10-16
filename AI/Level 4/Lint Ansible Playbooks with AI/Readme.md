# Task: Ansible Playbook Generator & Linter

The datacenter Automation Research Group is exploring the boundaries of machine-generated infrastructure workflows. After experimenting with deployment generators, PR pipelines, and multistage Docker analysis, the team is now evaluating whether AI can not only generate config files but also lint them intelligently.

In this project, you will build a two-stage AI pipeline inside ansible_pipeline.py. The system will first act as an Ansible Expert generating a valid playbook based on a task description, and then shift into an Ansible Linter that audits the file for best practices. A task.txt file has already been created for you.

**Initialize Client:** Create the OpenAI client (model: gpt-5.6-luna) using the api_key&base_url.

**Function 1:** generate_playbook(task_path: str, output_path: str) (The Expert)

    * Read the content of task.txtfile present under /root/openaiproject.

    * Call the OpenAI API with this instruction: "You are an Ansible expert. Based on this task, write a complete, valid Ansible playbook. Use the apt and service/ufw modules. Respond ONLY with the raw YAML, with no Markdown fences (```yaml)."

    * Save the AI-generated YAML to output_path( playbook.yaml) under /root/openaiproject.

**Function 2:** lint_playbook(playbook_path: str) -> str (The Linter)

    * Read the entire content of the generated playbook.yaml under /root/openaiproject.

    * Call the OpenAI API a second time using this system prompt: "You are ansible-lint. Review this playbook. Check for: 1) Missing name on any tasks. 2) Missing become: yes for privileged tasks (like apt or service). 3) Using state: latest for packages. Return a JSON object with a single key lint_errors, which is a list of strings. If there are no issues, return an empty list. Respond ONLY with the raw JSON."

    * Return the JSON string produced by the AI.

**Main Execution:**

Call generate_playbook('task.txt', 'playbook.yaml').

Call lint_playbook('playbook.yaml').

print() the final JSON result from the linter.


**Notes:**

    * Ensure you are working in the /root/openaiproject directory.

    * Your API credentials will be provided under /root/.bash_profile.

    * The script must create playbook.yaml and then read from it.

    * The final output must be only the raw JSON from the second AI call.

    * Use temperature=0.0 for the YAML generation (Call 1) and temperature=0.1 & max_tokens=250 for the linting (Call 2).

    * Use hardcoded values for api_key and base_url when initializing the OpenAI client or read them from environment variables via os.environ.get('OPENAI_API_KEY') and os.environ.get('OPENAI_API_BASE').

    * Before running ansible_pipeline.py, create and activate a virtual environment, then install OpenAI using:

        python3 -m venv venv && source venv/bin/activate && pip install openai

    * You are allowed up to 10 OpenAI requests. Past this limit you may encounter a rate limiter error, so optimize your request usage.

# Answer:
Create `/root/openaiproject/ansible_pipeline.py` with the following code. I can provide the complete implementation, but I can't directly access or execute commands in your `/root/openaiproject` environment from this chat.

## 1. Create `ansible_pipeline.py`

python
````

import os
from pathlib import Path
from openai import OpenAI

PROJECT_DIR = Path("/root/openaiproject")

# Initialize the OpenAI client using environment variables.
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE"),
)

def generate_playbook(task_path: str, output_path: str) -> None:
    """Generate an Ansible playbook from the specified task description."""
    task_file = PROJECT_DIR / task_path
    output_file = PROJECT_DIR / output_path

    task_content = task_file.read_text(encoding="utf-8")

    response = client.chat.completions.create(
        model="gpt-5.6-luna",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an Ansible expert. Based on this task, write "
                    "a complete, valid Ansible playbook. Use the apt and "
                    "service/ufw modules. Respond ONLY with the raw YAML, "
                    "with no Markdown fences (```yaml)."
                ),
            },
            {
                "role": "user",
                "content": task_content,
            },
        ],
        temperature=0.0,
    )

    playbook = response.choices[0].message.content
    if playbook is None:
        raise RuntimeError("The API returned no playbook content.")

    output_file.write_text(playbook.strip() + "\n", encoding="utf-8")

def lint_playbook(playbook_path: str) -> str:
    """Audit the generated playbook and return the raw JSON response."""
    playbook_file = PROJECT_DIR / playbook_path
    playbook_content = playbook_file.read_text(encoding="utf-8")

    response = client.chat.completions.create(
        model="gpt-5.6-luna",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are ansible-lint. Review this playbook. Check for: "
                    "1) Missing name on any tasks. "
                    "2) Missing become: yes for privileged tasks "
                    "(like apt or service). "
                    "3) Using state: latest for packages. "
                    "Return a JSON object with a single key lint_errors, "
                    "which is a list of strings. If there are no issues, "
                    "return an empty list. Respond ONLY with the raw JSON."
                ),
            },
            {
                "role": "user",
                "content": playbook_content,
            },
        ],
        temperature=0.1,
        max_tokens=250,
    )

    result = response.choices[0].message.content
    if result is None:
        raise RuntimeError("The API returned no lint results.")

    return result.strip()

if __name__ == "__main__":
    os.chdir(PROJECT_DIR)

    generate_playbook("task.txt", "playbook.yaml")
    lint_result = lint_playbook("playbook.yaml")

    print(lint_result)
````

## 2. Set up the virtual environment and run

Execute these commands in your terminal:

bash
```
cd /root/openaiproject

source /root/.bash_profile

python3 -m venv venv
source venv/bin/activate

pip install openai

python ansible_pipeline.py
```

If the environment variables are not exported after sourcing `.bash_profile`, set them using your existing credentials without printing or exposing the secret values.

## 3. Verify the output

The script performs the required two API calls in sequence:

1. Reads `task.txt` and writes the generated YAML to `/root/openaiproject/playbook.yaml`.
2. Reads `playbook.yaml`, sends it to the linter, and returns the raw JSON string.
3. Prints only the linter's response to standard output.

The final output should have this structure (the actual errors depend on the generated playbook):

json
```
{
  "lint_errors": []
}
```

The example above is illustrative; it is not a result from an API call.