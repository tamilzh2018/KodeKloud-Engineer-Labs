Docker Stack Architect & Network Analyst

The datacenter AI Engineering Division is expanding its research into AI-driven infrastructure automation. After experimenting with poetry, testing frameworks, and optimization workflows, the team now wants to evaluate how well AI can design infrastructure and reason about networking in a multi-stage pipeline.

In this you will build a two-stage intelligent DevOps workflow inside docker_stack.py. The system will first act as a DevOps Architect generating a Docker Compose file, and then transform into a Network Analyst evaluating how the generated stack communicates internally. A app_spec.txt file has already been created for you.

Initialize Client: Create the OpenAI client (model: gpt-5.6-luna) using the api_key&base_url.

Function 1: generate_compose(spec_path: str, output_path: str) (The Architect)

Read the content of app_spec.txt present under /root/openaiproject.

Call the OpenAI API with a prompt: "You are a DevOps Architect. Based on this app spec, write a complete, valid docker-compose.yml file. The web service must depend on db and cache. Use environment variables for the Postgres password. Respond ONLY with the raw YAML, with no Markdown fences (```yaml)."

Save the AI's YAML output to output_path ( docker-compose.yml) under /root/openaiproject.

Function 2: analyze_networking(compose_path: str) -> str (The Analyst)

Read the entire content of the generated docker-compose.yml file.

Call the OpenAI API a second time using a different system prompt: "You are a network engineer. Read this Docker Compose file. In a single paragraph, explain how the web service can connect to the db service (mentioning service discovery names) and why the db port does not need to be exposed to the host machine."

The AI must respond with a single paragraph and nothing else.

Return that paragraph as a string.

Main Execution:

Call generate_compose('app_spec.txt', 'docker-compose.yml').

Call analyze_networking('docker-compose.yml').

print() the final networking explanation.


Notes:

Ensure you are working in the /root/openaiproject directory.

Your API credentials will be provided under /root/.bash_profile.

The script must create docker-compose.yml and then read from it during the second AI call.

The final output must be only the raw single-paragraph explanation.

Use temperature=0.0 for the YAML generation (Call 1) and temperature=0.5 & max_tokens = 300 for the networking analysis (Call 2).

Use hardcoded values for api_key and base_url when initializing the OpenAI client or read them from environment variables via os.environ.get('OPENAI_API_KEY') and os.environ.get('OPENAI_API_BASE').

Before running docker_stack.py, create and activate a virtual environment, then install OpenAI using:

python3 -m venv venv && source venv/bin/activate && pip install openai

You are allowed a maximum of 10 requests. After this, you may encounter a rate limiter error, so use your calls wisely.

Answer:
We’ll build the lab in `/root/openaiproject` with a two-stage Python workflow:

1. DevOps Architect: Reads `app_spec.txt`, calls the OpenAI API using `gpt-5.6-luna` at temperature `0.0`, and saves the raw YAML to `docker-compose.yml`.
2. Network Analyst: Reads the generated Compose file, makes a second API call at temperature `0.5` with `max_tokens=300`, and prints a single-paragraph networking explanation.

We’ll use environment variables for API credentials, preserve the required service dependency on `db` and `cache`, and avoid unnecessary API calls. The script will make exactly two model requests when both stages succeed.

## Step 1: Open the project and activate a virtual environment

Run these commands in your terminal:

bash
```
cd /root/openaiproject

source /root/.bash_profile

python3 -m venv venv
source venv/bin/activate

pip install openai
```

If you already have a virtual environment, you can reuse it instead of recreating it.

## Step 2: Verify the API credentials and app specification

Run:

bash
```
cd /root/openaiproject
source /root/.bash_profile

test -n "$OPENAI_API_KEY" && echo "API key is set" || echo "API key is missing"
test -n "$OPENAI_API_BASE" && echo "API base is set" || echo "API base is missing"

ls -l app_spec.txt
cat app_spec.txt
```

Do not print or share the actual API key. If either variable is missing, check `/root/.bash_profile` and ensure the variables are exported under the expected names.

## Step 3: Create `docker_stack.py`

Run the following command from `/root/openaiproject`. It creates the complete script with both required API calls.

bash
````

cat > docker_stack.py <<'PY'
import os
from pathlib import Path
from openai import OpenAI

# Always run the workflow from the project directory.
PROJECT_DIR = Path(__file__).resolve().parent
os.chdir(PROJECT_DIR)

API_KEY = os.environ.get("OPENAI_API_KEY")
BASE_URL = os.environ.get("OPENAI_API_BASE")

if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set.")
if not BASE_URL:
    raise RuntimeError("OPENAI_API_BASE is not set.")

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

MODEL = "gpt-5.6-luna"

def generate_compose(spec_path: str, output_path: str) -> None:
    """Generate a Docker Compose YAML file from the application spec."""
    spec_file = Path(spec_path)
    output_file = Path(output_path)

    app_spec = spec_file.read_text(encoding="utf-8")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a DevOps Architect. Based on this app spec, "
                    "write a complete, valid docker-compose.yml file. "
                    "The web service must depend on db and cache. "
                    "Use environment variables for the Postgres password. "
                    "Respond ONLY with the raw YAML, with no Markdown "
                    "fences (```yaml)."
                ),
            },
            {
                "role": "user",
                "content": app_spec,
            },
        ],
        temperature=0.0,
    )

    yaml_content = response.choices[0].message.content
    if not yaml_content:
        raise RuntimeError("The Architect returned an empty YAML response.")

    output_file.write_text(yaml_content.strip() + "\n", encoding="utf-8")

def analyze_networking(compose_path: str) -> str:
    """Analyze internal service communication in the generated Compose file."""
    compose_file = Path(compose_path)
    compose_content = compose_file.read_text(encoding="utf-8")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a network engineer. Read this Docker Compose "
                    "file. In a single paragraph, explain how the web "
                    "service can connect to the db service (mentioning "
                    "service discovery names) and why the db port does not "
                    "need to be exposed to the host machine."
                ),
            },
            {
                "role": "user",
                "content": compose_content,
            },
        ],
        temperature=0.5,
        max_tokens=300,
    )

    explanation = response.choices[0].message.content
    if not explanation:
        raise RuntimeError("The Analyst returned an empty explanation.")

    return " ".join(explanation.split())

if __name__ == "__main__":
    generate_compose("app_spec.txt", "docker-compose.yml")
    explanation = analyze_networking("docker-compose.yml")
    print(explanation)
PY
````

This implementation reads the generated file back from disk before making the second request. It also ensures that the script prints only the networking explanation, not the YAML or additional status messages.

## Step 4: Run the workflow

Make sure you are in the project directory and your virtual environment is active:

bash
```
cd /root/openaiproject
source /root/.bash_profile
source venv/bin/activate

python docker_stack.py
```

If the script succeeds, its terminal output will be the single-paragraph networking explanation.

## Step 5: Verify the generated Compose file

After the script finishes, open a separate terminal command or run these commands after the script has completed:

bash
```
cd /root/openaiproject

ls -l docker_stack.py docker-compose.yml
cat docker-compose.yml
```

If Docker Compose is installed, validate the generated configuration:

bash
```
docker compose config
```

Check that the YAML contains:

- A `web` service with `depends_on` entries for `db` and `cache`.
- A `db` service with its PostgreSQL password supplied through an environment variable, ideally using `${POSTGRES_PASSWORD}`.
- A `cache` service.
- No unnecessary host port mapping for PostgreSQL.

## Step 6: Understand the expected networking explanation

The Analyst should explain the following concepts in its own generated paragraph:

- Service discovery: Docker Compose provides DNS-based discovery between services on the same network. The web application can connect to the database using the hostname `db` and PostgreSQL's internal port, typically `5432`.
- Internal networking: The web service does not need to connect through the host machine's IP address.
- Port exposure: PostgreSQL does not need a host port mapping such as `5432:5432` for communication between Compose services. Host port publishing is only necessary if clients outside the Docker network need direct access.

## Step 7: Troubleshooting

- Missing API credentials: Re-source `/root/.bash_profile` and verify that both expected environment variables are set.
- Authentication or connection error: Check the API key, base URL, and network connectivity.
- Model error: Confirm that `gpt-5.6-luna` is available through the configured API endpoint and supports the Chat Completions interface and requested parameters.
- Invalid YAML: Inspect `docker-compose.yml` and validate it with `docker compose config`. The script requests raw YAML, but you should still validate the model's output.

Completion checklist

- [ ]Virtual environment created and activated.
- [ ]OpenAI package installed.
- [ ]`docker_stack.py` created.
- [ ]First API call generated `docker-compose.yml` at temperature `0.0`.
- [ ]Second API call read that file and used temperature `0.5` and `max_tokens=300`.
- [ ]Final output is one paragraph printed by `print(explanation)`.

Once these checks pass, the lab's two-stage workflow is complete.