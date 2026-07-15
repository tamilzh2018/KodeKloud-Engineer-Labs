# Lab Question:  AI Press Release Generator & Media Analyst

1. The devops AI Development Team is experimenting with how artificial intelligence can create expressive short poetry through automation. In this project, you will explore how AI can also simulate a real-world public-relations workflow using a two-stage reasoning pipeline.

2. Your task is to build a two-stage AI pipeline in pr_pipeline.pythat simulates a public relations workflow. Aproduct_brief.txtfile has been created for you.

    a. Initialize Client: Create theOpenAIclient using api_key&base_url.

    b. Function 1:generate_press_release(brief_path: str, output_path: str) (The PR Specialist)

        * Read the content of product_brief.txtpresent under/root/openaiproject.
        * Call the OpenAI API with a prompt: "You are a PR specialist. Based on this product brief, write an exciting, 150-word professional press release."
        * Save the AI's text response to the output_path (/root/openaiproject/press_release.txt).
    c. Function 2:analyze_press_release(pr_path: str) -> str (The Journalist)

        * Read the entire content of the file generated in Step 2 (press_release.txt).
        * Call the OpenAI API a second time with a different system prompt: "You are a cynical, skeptical tech journalist. Read the following press release. Identify the 'Top 3 Toughest Questions' a journalist would ask about this product. Return a JSON object with a single key tough_questions, which is a list of strings."
        * Your prompt must instruct the AI to return only the raw JSON object, with no additional text, explanations, or Markdown code fences.
        * Return the AI's JSON string response.
    d. Main Execution:

        * Call generate_press_release('product_brief.txt', 'press_release.txt').
        * Call analyze_press_release('press_release.txt').
        * print() the final JSON string from the analyst.

# Notes:

1. Ensure you are working in the /root/openaiproject directory.

2. Your API credentials will be provided under /root/.bash_profile.

3. The script must create a new file press_release.txt and then read from it.

4. The final output must be only the raw JSON string from the second API call.

5. Use temperature=0.7&max_tokens=200 for the generate press release (Call 1) and temperature=0.5& max_tokens=200 for the analysis (Call 2).
6. Use model="openai/gpt-4.1-mini"for both the Calls.

7. Use hardcoded values for api_keyandbase_url when initializing the OpenAI client or read them from environment variables via os.environ.get('OPENAI_API_KEY') and os.environ.get('OPENAI_API_BASE').

    * Correct Final output example:

    {
    " tough_questions": [
        "Question 1",
        "Question 2",
        "Question 3"
    ]
    }

8. Before running pr_pipeline.py, create and activate a virtual environment, then install OpenAI using:
    python3 -m venv venv && source venv/bin/activate && pip install openai

9. You are allowed a maximum of 10 requests. After this, you may encounter a rate limiter error. Therefore, use your requests judiciously.

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
*Update pr_pipeline.py*

import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE")
)

def generate_press_release(brief_path: str, output_path: str):
    base_dir = "/root/openaiproject"
    brief_full = os.path.join(base_dir, brief_path) if not os.path.isabs(brief_path) else brief_path
    out_full = os.path.join(base_dir, output_path) if not os.path.isabs(output_path) else output_path

    with open(brief_full, "r") as f:
        brief_content = f.read()

    prompt = f"You are a PR specialist. Based on this product brief, write an exciting, 150-word professional press release.\n\nBrief:\n{brief_content}"

    response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        temperature=0.7,
        max_tokens=200,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    pr_text = response.choices[0].message.content.strip()

    with open(out_full, "w") as out:
        out.write(pr_text)

def analyze_press_release(pr_path: str) -> str:
    base_dir = "/root/openaiproject"
    pr_full = os.path.join(base_dir, pr_path) if not os.path.isabs(pr_path) else pr_path

    with open(pr_full, "r") as f:
        pr_content = f.read()

    system_prompt = (
        "You are a cynical, skeptical tech journalist. Read the following press release. "
        "Identify the 'Top 3 Toughest Questions' a journalist would ask about this product. "
        "Return a JSON object with a single key tough_questions, which is a list of strings."
    )
    user_prompt = (
        f"{system_prompt}\n\n"
        f"Press Release:\n{pr_content}\n\n"
        "Return only the raw JSON object, with no additional text, explanations, or Markdown code fences."
    )

    response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        temperature=0.5,
        max_tokens=200,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    json_str = response.choices[0].message.content.strip()

    if json_str.startswith("```"):
        lines = json_str.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        json_str = "\n".join(lines).strip()

    return json_str

if __name__ == "__main__":
    os.chdir("/root/openaiproject")
    generate_press_release("product_brief.txt", "press_release.txt")
    result = analyze_press_release("press_release.txt")
    print(result)

**Step 6 — Execute the Script**

```
python pr_pipeline.py
```

**Step 7 — Verify Output**

{
  "tough_questions": [
    "How does Project-X ensure the privacy and security of users' sensitive email data when using AI to compose messages?",
    "What concrete evidence or independent benchmarks support the claim that Project-X is the fastest and most intuitive email assistant on the market?",
    "How does Project-X handle nuanced or complex email contexts where AI-generated responses might misinterpret tone or intent, potentially leading to miscommunication?"
  ]
}