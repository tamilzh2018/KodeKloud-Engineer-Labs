# Lab Question:
**AI Code Gen & Security Review Pipeline:**
1. The devops AI Development Team is investigating how artificial intelligence can enhance software engineering workflows. You will leverage AI to generate code, perform code reviews, analyze implementation quality, and support automated development processes.

2. Your task is to build a two-stage AI pipeline in pipeline.py. The first stage generates code, and the second stage reviews it for security flaws. The requirements.txt file has been created under /root/openaiproject.

    a. Initialize Client: Create the OpenAI client using api_key& base_urlprovided under /root/.bash_profile.

    b. Function1:generate_code(requirements_path: str, output_path: str) (The Developer)

        * Read the content of /root/openaiproject/requirements.txtfile

        * Call the OpenAI API with a prompt: "Based on these requirements, write a Python script that scrapes all <h2> headlines from 'example.com' and prints them. Include imports and a main execution block. Respond ONLY with the raw Python code."

        * Save the AI's code response to the output_path (web_scraper.py) file under
        /root/openaiproject.

    c. Function 2: review_code(code_path: str) -> str (The Reviewer)

        * Read the entire content of the file generated inCall 1 (web_scraper.py) file.

        * Call the OpenAI API a second time with a different system prompt: "You are a senior security architect. Review the attached Python code for any security or best-practice vulnerabilities (e.g., missing 'User-Agent' headers, no error handling for HTTP 4xx/5xx requests). Output a JSON object with a single key 'findings', which is a list of strings, each string describing one vulnerability. If no issues, return an empty list."

        * Crucially, the prompt must also instruct the AI to only return the raw JSON, with no Markdown fences.

        * Return the AI JSON string response.

    d. Main Execution:

        * Call generate_code('requirements.txt', 'web_scraper.py').

        * Call review_code('web_scraper.py').

        * print() the final JSON string from the review.


# Notes:

1. Ensure you are working in the /root/openaiproject directory.

2. Your API credentials will be provided under /root/.bash_profile.

3. The script must create a new file web_scraper.py under /root/openaiproject & then read from it.

4. The final output must be only the raw JSON string from the second API call.

5. Use temperature=0.0 for the code generation (Call 1). Use model=openai/gpt-4.1-mini for the call.

6. Use temperature=0.5 for the review (Call 2).Use model=openai/gpt-4.1-mini for the call.

7. Use hardcoded values for api_key and base_url when initializing the OpenAI client or read them from environment variables via os.environ.get('OPENAI_API_KEY') and os.environ.get('OPENAI_API_BASE').

8. Before running pipeline.py, create and activate a virtual environment, then install OpenAI using:

    python3 -m venv venv && source venv/bin/activate && pip install openai

9. You are allowed a maximum of 10 requests. After this, you may encounter a rate limiter error. Therefore, use your requests judiciously.


# Soultions:
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
*Update pipeline.py file*

from openai import OpenAI
import os
import json

# Initialize OpenAI client
import os
from openai import OpenAI

# Initialize client - read from env (set via /root/.bash_profile)
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE")
)

def generate_code(requirements_path: str, output_path: str):
    base_dir = "/root/openaiproject"
    req_full = os.path.join(base_dir, requirements_path) if not os.path.isabs(requirements_path) else requirements_path
    out_full = os.path.join(base_dir, output_path) if not os.path.isabs(output_path) else output_path

    with open(req_full, "r") as f:
        requirements_content = f.read()

    prompt = f"{requirements_content}\n\nBased on these requirements, write a Python script that scrapes all <h2> headlines from 'example.com' and prints them. Include imports and a main execution block. Respond ONLY with the raw Python code."

    response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        temperature=0.0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    code_output = response.choices[0].message.content.strip()

    if code_output.startswith("```"):
        lines = code_output.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        code_output = "\n".join(lines)

    with open(out_full, "w") as out_f:
        out_f.write(code_output)

def review_code(code_path: str) -> str:
    base_dir = "/root/openaiproject"
    code_full = os.path.join(base_dir, code_path) if not os.path.isabs(code_path) else code_path

    with open(code_full, "r") as f:
        generated_code = f.read()

    system_prompt = (
        "You are a senior security architect. Review the attached Python code for any security "
        "or best-practice vulnerabilities (e.g., missing 'User-Agent' headers, no error handling for "
        "HTTP 4xx/5xx requests). Output a JSON object with a single key 'findings', which is a list of "
        "strings, each string describing one vulnerability. If no issues, return an empty list. "
        "Only return the raw JSON, with no Markdown fences."
    )

    user_content = f"Review this code:\n\n{generated_code}"

    response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        temperature=0.5,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]
    )
    json_response = response.choices[0].message.content.strip()

    if json_response.startswith("```"):
        lines = json_response.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        json_response = "\n".join(lines).strip()

    return json_response

if __name__ == "__main__":
    os.chdir("/root/openaiproject")
    generate_code("requirements.txt", "web_scraper.py")
    result = review_code("web_scraper.py")
    print(result)
**Step 6 — Execute the Script**

```
python pipeline.py
```

**Step 7 — Verify Output**

Expected format example:

{
  "findings": [
    "Missing 'User-Agent' header in the HTTP request, which may cause the request to be blocked or treated as suspicious by some servers.",
    "No handling for HTTP errors other than raise_for_status; while raise_for_status() raises exceptions on HTTP 4xx/5xx, there is no try-except block to gracefully handle these exceptions.",
    "The URL uses 'http' instead of 'https', which is insecure and susceptible to man-in-the-middle attacks."
  ]
}

---