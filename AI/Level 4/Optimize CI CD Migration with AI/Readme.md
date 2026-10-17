# Task
CI/CD Migration & Optimization Pipeline

The xfusion Automation Research Group is pushing the limits of how AI can autonomously modernize and optimize CI/CD workflows. After experimenting with AI-based deployment generators and container optimizers, the team is now exploring whether artificial intelligence can fully migrate legacy shell-based CI scripts into modern cloud-native pipelines and then improve their efficiency through iterative reasoning.

In this project, you will develop a three-stage AI pipeline that transforms an old build.sh script into a GitHub Actions workflow, enhances it by adding dependency caching, and then produces an AI-generated commit message summarizing the optimization.

Your task is to build this logic inside ci_pipeline.py.

Initialize Client: Create the OpenAI client (model: gpt-5.6-luna using the api_key&base_url.

Function 1: generate_workflow(script_content: str) -> str

Read the content of build.shpresent under /root/openaiproject.

Call OpenAI as a "DevOps Expert" to convert the build.sh script into a complete GitHub Actions workflow YAML (main.yml).

Save this YAML output to a new file named main.ymlunder /root/openaiproject

Return the YAML string.

Function 2: optimize_workflow(base_yaml_content: str) -> str

Take the YAML content from Function 1 as input.

Call OpenAI as a "CI/CD Performance Specialist" to add an actions/cache step before the 'pip install' step to cache dependencies.

Save this new, optimized YAML to a file named main-optimized.yml under /root/openaiproject.

Return the optimized YAML string.

Function 3: generate_commit(original_yaml: str, optimized_yaml: str) -> str

Take both the original and optimized YAML strings as input.

Call OpenAI as a "Tech Lead" to summarize the change between the two files in a single, one-line conventional commit message (e.g., ci: add caching for dependencies).

Return the single-line commit message.

Main Execution:

Orchestrate the full pipeline: Call 1 → Save File 1 → Call 2 → Save File 2 → Call 3.

print() the final one-line commit message from Function 3.


Notes:

Ensure you are working in the /root/openaiproject directory.

Your API credentials will be provided under /root/.bash_profile.

This is a 3-call chain that creates two new files (main.yml and main-optimized.yml) under /root/openaiproject.

The final output must be only the raw, single-line commit message.

Use temperature=0.0 for call 1,temperature=0.0 for call 2 &temperature=0.5 for call 3.

Use hardcoded values for api_key and base_url when initializing the OpenAI client or read them from environment variables via os.environ.get('OPENAI_API_KEY') and os.environ.get('OPENAI_API_BASE').

Before running ci_pipeline.py, create and activate a virtual environment, then install OpenAI using:

python3 -m venv venv && source venv/bin/activate && pip install openai

You are allowed a maximum of 10 requests. After this, you may encounter a rate limiter error, so use your calls wisely.

# Solution

from openai import OpenAI
import os
from pathlib import Path

from openai import OpenAI

PROJECT_DIR = Path("/root/openaiproject")

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE"),
)

MODEL = "gpt-5.6-luna"


def generate_workflow(script_content: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.0,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a DevOps Expert. Convert the supplied shell "
                    "build script into a complete, valid GitHub Actions "
                    "workflow YAML. Preserve the original build behavior, "
                    "use appropriate triggers and runner settings, and "
                    "include necessary setup steps. Return only YAML, "
                    "without Markdown fences or explanations."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Convert this build.sh script into main.yml:\n\n"
                    f"{script_content}"
                ),
            },
        ],
    )

    yaml_content = response.choices[0].message.content
    if not yaml_content:
        raise RuntimeError("Workflow generation returned empty content.")

    yaml_content = yaml_content.strip()
    (PROJECT_DIR / "main.yml").write_text(
        yaml_content + "\n", encoding="utf-8"
    )
    return yaml_content


def optimize_workflow(base_yaml_content: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.0,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a CI/CD Performance Specialist. Optimize "
                    "the supplied GitHub Actions workflow by adding an "
                    "actions/cache step before the pip install step. "
                    "Cache pip dependencies using a suitable cache path "
                    "and a dependency-file-based cache key with a "
                    "fallback restore key. Preserve all existing workflow "
                    "behavior. Return only complete YAML, without "
                    "Markdown fences or explanations."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Optimize this workflow:\n\n"
                    f"{base_yaml_content}"
                ),
            },
        ],
    )

    optimized_yaml = response.choices[0].message.content
    if not optimized_yaml:
        raise RuntimeError("Workflow optimization returned empty content.")

    optimized_yaml = optimized_yaml.strip()
    (PROJECT_DIR / "main-optimized.yml").write_text(
        optimized_yaml + "\n", encoding="utf-8"
    )
    return optimized_yaml


def generate_commit(original_yaml: str, optimized_yaml: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.5,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a Tech Lead. Compare the original and "
                    "optimized GitHub Actions workflows and produce "
                    "one concise, single-line conventional commit message. "
                    "Use an appropriate type such as ci:. Output only "
                    "the commit message, without quotes, Markdown, "
                    "or explanation."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Original workflow:\n"
                    f"{original_yaml}\n\n"
                    "Optimized workflow:\n"
                    f"{optimized_yaml}"
                ),
            },
        ],
    )

    commit_message = response.choices[0].message.content
    if not commit_message:
        raise RuntimeError("Commit message generation returned empty content.")

    return " ".join(commit_message.strip().splitlines()).strip()


def main() -> None:
    script_path = PROJECT_DIR / "build.sh"
    script_content = script_path.read_text(encoding="utf-8")

    original_yaml = generate_workflow(script_content)
    optimized_yaml = optimize_workflow(original_yaml)
    commit_message = generate_commit(original_yaml, optimized_yaml)

    print(commit_message)


if __name__ == "__main__":
    main()
