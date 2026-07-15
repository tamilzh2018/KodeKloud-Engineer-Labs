# Lab Question:  AI Strategy Debate & Synthesis

1. The devops AI Development Team is investigating how artificial intelligence can support executive decision-making through role-based analysis. In this project, you will leverage AI to think like a business leader, evaluate opportunities and challenges, and generate strategic recommendations based on the provided business context.

2. Your task is to build a three-stage AI pipeline in strategy_debate.py to simulate a high-level business strategy meeting. A business_problem.txt file has been created for you.

    a. Initialize Client: Create the OpenAI client using api_key& base_url.

    b. Read Problem: Read the content of business_problem.txt provided under /root/openaiproject.

    c. Call 1 (The "CMO"): — Define the function:

    def get_cmo_args(problem: str) -> str:
    """Generates the CMO's (pro–e-commerce)  arguments."""

    * Call the OpenAI API with a system prompt: "You are a Chief Marketing Officer. You are ambitious and focused on growth. Argue for the e-commerce platform in three concise bullet points."

    * Use the business problem as the user prompt. Store the AI's response (the 3 bullets) in a variable.

    d. Call 2 (The "CFO"): — Define the function:

    def get_cfo_args(problem: str) -> str:
    """Generates the CFO's (pro–physical stores) arguments."""

    Call the OpenAI API a second time with a different system prompt: "You are a Chief Financial Officer. You are cautious and risk-averse. Argue for modernizing the physical stores in three concise bullet points."

    Use the business problem as the user prompt. Store the AI's response in a second variable.

    e. Call 3 (The "CEO"): — Define the function:

    def get_ceo_decision(problem: str, cmo_args: str, cfo_args: str) -> str:
    """Synthesizes arguments from both sides and produces the CEO's final decision."""

    * Construct a new, large prompt that includes:

    1) The original business problem,
    2) The CMO's arguments, and
    3) The CFO's arguments.

    * Call the OpenAI API a third time with a final system prompt: "You are the CEO. Review the business problem and the conflicting advice from your CMO and CFO. Make a final decision and write a one-paragraph executive summary explaining your reasoning and the chosen path."

    d. Final Output: print() only the final one-paragraph executive summary from the CEO.


# Notes:

1. Ensure you are working in the /root/openaiproject directory.

2. Your API credentials will be provided under /root/.bash_profile.

3. This script will make three separate calls to the OpenAI API.

4. The input for Call 3 must contain the outputs from Call 1 and Call 2.

5. The final printed output should be only the CEO's summary.

6. Use temperature=0.5 & max_tokens=150 for CMO, CFO and temperature=0.7& max_tokens=200for CEO.
7. Use model="openai/gpt-4.1-mini" for all the calls.

8. Use hardcoded values for api_key and base_url when initializing the OpenAI client or read them from environment variables via os.environ.get('OPENAI_API_KEY') and os.environ.get('OPENAI_API_BASE').

9. Before running strategy_debate.py, create and activate a virtual environment, then install OpenAI using:

    python3 -m venv venv && source venv/bin/activate && pip install openai

10. You are allowed a maximum of 10 requests. After this, you may encounter a rate limiter error. Therefore, use your requests judiciously.

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
*Update strategy_debate.py*
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE")
)

def get_cmo_args(problem: str) -> str:
    """Generates the CMO's (pro-e-commerce) arguments."""
    response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        temperature=0.5,
        max_tokens=150,
        messages=[
            {"role": "system", "content": "You are a Chief Marketing Officer. You are ambitious and focused on growth. Argue for the e-commerce platform in three concise bullet points."},
            {"role": "user", "content": problem}
        ]
    )
    return response.choices[0].message.content.strip()

def get_cfo_args(problem: str) -> str:
    """Generates the CFO's (pro-physical stores) arguments."""
    response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        temperature=0.5,
        max_tokens=150,
        messages=[
            {"role": "system", "content": "You are a Chief Financial Officer. You are cautious and risk-averse. Argue for modernizing the physical stores in three concise bullet points."},
            {"role": "user", "content": problem}
        ]
    )
    return response.choices[0].message.content.strip()

def get_ceo_decision(problem: str, cmo_args: str, cfo_args: str) -> str:
    """Synthesizes arguments from both sides and produces the CEO's final decision."""
    combined_prompt = (
        f"Business Problem:\n{problem}\n\n"
        f"CMO Arguments (pro e-commerce):\n{cmo_args}\n\n"
        f"CFO Arguments (pro physical stores):\n{cfo_args}\n\n"
        "Based on the above, make your decision."
    )

    response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        temperature=0.7,
        max_tokens=200,
        messages=[
            {"role": "system", "content": "You are the CEO. Review the business problem and the conflicting advice from your CMO and CFO. Make a final decision and write a one-paragraph executive summary explaining your reasoning and the chosen path."},
            {"role": "user", "content": combined_prompt}
        ]
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    os.chdir("/root/openaiproject")

    with open("business_problem.txt", "r") as f:
        problem = f.read()

    cmo_args = get_cmo_args(problem)
    cfo_args = get_cfo_args(problem)
    ceo_decision = get_ceo_decision(problem, cmo_args, cfo_args)

    print(ceo_decision)

**Step 6 — Execute the Script**

```
python strategy_debate.py

```

**Step 7 — Verify Output**
# Final output: only the one-paragraph CEO executive summary
After carefully weighing the arguments, I have decided to allocate the entire $50M capital to building a world-class e-commerce platform. While modernizing our physical stores offers incremental improvements and lower immediate risk, the rapidly shifting consumer preference toward online shopping and the scalability of e-commerce present a far greater opportunity for sustainable growth and market expansion. Investing in a robust digital infrastructure will enable us to capture new customer segments globally, leverage data-driven personalization, and stay competitive in an increasingly digital retail landscape. This strategic move aligns with long-term industry trends and future-proofs our business, whereas incremental store upgrades risk falling behind evolving consumer behaviors. We will ensure disciplined project management to mitigate risks and plan for future store enhancements once our e-commerce platform solidifies its revenue base.