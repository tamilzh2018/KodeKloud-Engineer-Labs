# Terraform DevSecOps & FinOps Auditor

The datacenter Automation Research Group is pushing the boundaries of AI-driven infrastructure governance. After previous breakthroughs in autonomous CI/CD pipelines and Ansible playbook linting, the team is now exploring whether AI can perform DevSecOps and FinOps auditing on Infrastructure-as-Code — identifying vulnerabilities and cost inefficiencies, and even auto-fixing them.

In this challenge, you will build a three-stage AI auditing system that performs both security and cost scanning on a Terraform configuration file (main.tf) and then intelligently rewrites it to ensure compliance and efficiency.

Your goal is to automate what a human DevOps engineer and cloud architect might do during a production review — detect risky network configurations and costly compute resources, then apply the appropriate remediations.

Your implementation will be in tf_auditor.py.

**Initialize Client:** Create the OpenAI client using (gpt-5.6-luna) api_key& base_url.

**Function 1:** security_scan(tf_content: str) -> str

* Call OpenAI as a Security Linter. Identify issues such as open SSH ports (0.0.0.0/0) or missing encryption.

* Return a JSON list of issues.

**Function 2:** cost_scan(tf_content: str) -> str

* Call OpenAI as a FinOps Analyst. Identify expensive resources (e.g., m5.2xlarge) and suggest cheaper, equivalent alternatives (like t3.micro).

* Return a JSON list of issues.

**Function 3:** apply_fixes(tf_content: str, sec_issues: str, cost_issues: str)

* Call OpenAI as a Senior SRE. Provide the original Terraform along with both JSON reports.

* Ask it to rewrite the entire main.tf file, addressing all identified issues.

* Save the corrected file as fixed_main.tfunder /root/openaiproject.

**Main Execution:**

* Read main.tf.

* Run both scans (security and cost).

* Apply the generated fixes using both reports.

* print() a confirmation message once the fixed Terraform file is successfully generated.


**Notes:**

* Ensure you are working in the /root/openaiproject directory.

* Your API credentials will be provided under /root/.bash_profile.

* You must successfully chain three API calls.

* The main.tf file is present under /root/openaiproject.

* The final output file fixed_main.tf must contain valid HCL with the specific fixes applied (changing the instance type and locking down the security group).

* Use temperature=0.0for Function 1,temperature=0.0 for Function 2&temperature=0.0forFunction 3.

* Use hardcoded values for api_key and base_url when initializing the OpenAI client or read them from environment variables via os.environ.get('OPENAI_API_KEY') and os.environ.get('OPENAI_API_BASE').

* Before running tf_auditor.py, create and activate a virtual environment, then install OpenAI using:

python3 -m venv venv && source venv/bin/activate && pip install openai

* You are allowed a maximum of 10 requests. After this, you may encounter a rate limiter error, so use your calls wisely.

# Answer:
You can solve this lab by creating `tf_auditor.py` in `/root/openaiproject`, implementing three sequential OpenAI API calls, and verifying that `fixed_main.tf` contains the required Terraform security and cost fixes.

I'll walk you through the setup, code, execution, and validation. You can do this entirely in your terminal.

## Step 1: Navigate to the project directory

bash
```
cd /root/openaiproject
ls -la
```

Confirm that `main.tf` exists:

bash
```
cat main.tf
```

Look for the issues mentioned in the lab, such as an expensive EC2 instance type or a security group that allows SSH from `0.0.0.0/0`.

## Step 2: Set up the virtual environment

Run the requested commands:

bash
```
python3 -m venv venv
source venv/bin/activate
pip install openai
```

Verify the installation:

bash
```
python -c "import openai; print(openai.__version__)"
```

## Step 3: Load your API credentials

The lab says your credentials are in `/root/.bash_profile`. Inspect the relevant variable names without printing their secret values:

bash
```
grep -nE 'OPENAI_API_KEY|OPENAI_API_BASE' /root/.bash_profile
```

Load the profile:

bash
```
source /root/.bash_profile
```

Check that both variables are set:

bash
```
python -c "import os; print('API key configured:', bool(os.environ.get('OPENAI_API_KEY'))); print('API base configured:', bool(os.environ.get('OPENAI_API_BASE')))"
```

If either value is missing, configure it according to the credentials provided by your lab. Do not share your API key in the terminal output or chat.

## Step 4: Create `tf_auditor.py`

Open the file in a terminal editor:

bash
```
nano tf_auditor.py
```

Paste the following implementation. It uses the three required functions and chains the security report and cost report into the final rewrite call.

python
````

import json
import os
from pathlib import Path

from openai import OpenAI

# Lab-provided API credentials are loaded from environment variables.
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE"),
)

PROJECT_DIR = Path("/root/openaiproject")
INPUT_FILE = PROJECT_DIR / "main.tf"
OUTPUT_FILE = PROJECT_DIR / "fixed_main.tf"

def security_scan(tf_content: str) -> str:
    """Scan Terraform for security and compliance issues."""
    response = client.chat.completions.create(
        model="gpt-5.6-luna",
        temperature=0.0,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a Terraform DevSecOps security linter. "
                    "Identify concrete security issues, including SSH or other "
                    "sensitive ports exposed to 0.0.0.0/0, overly permissive "
                    "ingress rules, and missing encryption where applicable. "
                    "Return ONLY a valid JSON array of issues. Each issue "
                    "should contain resource, issue, severity, and recommendation. "
                    "If there are no issues, return []. Do not use Markdown fences."
                ),
            },
            {
                "role": "user",
                "content": "Audit this Terraform configuration:\n\n" + tf_content,
            },
        ],
    )
    result = response.choices[0].message.content
    if not result:
        raise ValueError("Security scan returned an empty response.")
    json.loads(result)
    return result

def cost_scan(tf_content: str) -> str:
    """Scan Terraform for cost optimization opportunities."""
    response = client.chat.completions.create(
        model="gpt-5.6-luna",
        temperature=0.0,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a cloud FinOps analyst auditing Terraform. "
                    "Identify unnecessarily expensive resources and recommend "
                    "lower-cost alternatives when appropriate. For example, "
                    "consider t3.micro instead of m5.2xlarge only if it suits "
                    "the workload. Return ONLY a valid JSON array of issues. "
                    "Each issue should contain resource, current_configuration, "
                    "issue, and recommendation. If there are no issues, return []. "
                    "Do not use Markdown fences."
                ),
            },
            {
                "role": "user",
                "content": "Audit this Terraform configuration for cost:\n\n"
                + tf_content,
            },
        ],
    )
    result = response.choices[0].message.content
    if not result:
        raise ValueError("Cost scan returned an empty response.")
    json.loads(result)
    return result

def apply_fixes(
    tf_content: str,
    sec_issues: str,
    cost_issues: str,
) -> str:
    """Rewrite the complete Terraform file using both audit reports."""
    # Validate both reports before sending them to the model.
    json.loads(sec_issues)
    json.loads(cost_issues)

    response = client.chat.completions.create(
        model="gpt-5.6-luna",
        temperature=0.0,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior SRE and Terraform expert. Rewrite the "
                    "entire supplied Terraform configuration, applying the "
                    "security and cost fixes identified in the reports. "
                    "Preserve unrelated resources and necessary functionality. "
                    "Restrict SSH ingress to an explicitly approved trusted CIDR "
                    "rather than 0.0.0.0/0. Do not invent a trusted IP: if none "
                    "is provided, use a clearly marked placeholder such as "
                    "REPLACE_WITH_TRUSTED_CIDR/32 and explain it in a Terraform "
                    "comment. Apply the recommended instance type where suitable. "
                    "Return ONLY the complete valid HCL source code, with no "
                    "Markdown fences or explanatory prose."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Original main.tf:\n\n"
                    + tf_content
                    + "\n\nSecurity report (JSON):\n"
                    + sec_issues
                    + "\n\nCost report (JSON):\n"
                    + cost_issues
                    + "\n\nRewrite the entire main.tf with the fixes applied."
                ),
            },
        ],
    )

    fixed_content = response.choices[0].message.content
    if not fixed_content or not fixed_content.strip():
        raise ValueError("Fix generation returned an empty response.")

    fixed_content = fixed_content.strip()

    # Remove Markdown fences if the model unexpectedly adds them.
    if fixed_content.startswith("```"):
        lines = fixed_content.splitlines()
        if lines[-1].strip() == "```":
            fixed_content = "\n".join(lines[1:-1]).strip()
        elif lines[0].startswith("```"):
            fixed_content = "\n".join(lines[1:]).strip()

    if not fixed_content:
        raise ValueError("Generated Terraform content is empty.")

    OUTPUT_FILE.write_text(fixed_content + "\n", encoding="utf-8")
    return str(OUTPUT_FILE)

def main():
    if not INPUT_FILE.is_file():
        raise FileNotFoundError(f"Terraform file not found: {INPUT_FILE}")

    tf_content = INPUT_FILE.read_text(encoding="utf-8")

    print("Stage 1/3: Running security scan...")
    sec_issues = security_scan(tf_content)
    print("Security scan completed.")
    print(sec_issues)

    print("\nStage 2/3: Running cost scan...")
    cost_issues = cost_scan(tf_content)
    print("Cost scan completed.")
    print(cost_issues)

    print("\nStage 3/3: Applying fixes...")
    output_path = apply_fixes(tf_content, sec_issues, cost_issues)

    print(f"\nSuccess: Fixed Terraform file generated at {output_path}")

if __name__ == "__main__":
    main()
````

Save and exit Nano with `Ctrl+O`, Enter, then `Ctrl+X`.

Important: The example uses the model identifier exactly as your lab specifies, `gpt-5.6-luna`. If your lab's API endpoint does not recognize it, confirm the exact model identifier with the lab instructions or administrator rather than substituting a model arbitrarily.

## Step 5: Run the auditor

First make sure the virtual environment is active and the credentials are available:

bash
```
cd /root/openaiproject
source venv/bin/activate
source /root/.bash_profile
```

Then execute:

bash
```
python tf_auditor.py
```

The expected sequence is:

1. Security scan — returns a JSON array of security issues.
2. Cost scan — returns a JSON array of cost optimization issues.
3. Fix generation — submits the original Terraform and both reports, then writes the complete result to `fixed_main.tf`.

The script makes three model API requests if all stages succeed.

## Step 6: Verify the generated Terraform

Check that the output exists and inspect it:

bash
```
ls -l /root/openaiproject/fixed_main.tf
cat /root/openaiproject/fixed_main.tf
```

Check for the required remediations:

bash
```
grep -nE 'instance_type|cidr_blocks|from_port|to_port|protocol' fixed_main.tf
```

You should verify that:

- The expensive EC2 instance type has been changed to the recommended cheaper type, such as `t3.micro`, if appropriate for the workload.
- SSH port 22 is no longer exposed to `0.0.0.0/0`.
- Unrelated Terraform resources and required configuration have been preserved.
- Any placeholder CIDR is replaced with your actual approved trusted CIDR before deployment.

A model-generated file is not automatically guaranteed to be valid HCL. If Terraform is installed, validate the result:

bash
```
terraform fmt -check fixed_main.tf
terraform init -backend=false
terraform validate
```

Run `terraform init` and `terraform validate` from the project directory. If the project has modules or providers requiring initialization, resolve any initialization errors before interpreting validation results.

## Step 7: Troubleshooting

| Error | What to check |
| --- | --- |
| `AuthenticationError` | Confirm `OPENAI_API_KEY` is loaded and valid. |
| Connection or base URL error | Verify `OPENAI_API_BASE` matches the lab endpoint. |
| Model not found | Confirm the exact supported model identifier. |
| Rate limit error | Avoid repeatedly rerunning all three stages; inspect the error and retry only when appropriate. |
| Invalid JSON from a scan | The script will raise a JSON parsing error; inspect the model response before retrying. |
| Terraform validation failure | Inspect the generated HCL and fix syntax or provider-specific errors. |

### Final checklist

- [ ]`tf_auditor.py` is in `/root/openaiproject`.
- [ ]Virtual environment created and activated.
- [ ]OpenAI Python package installed.
- [ ]API credentials loaded from the shell environment.
- [ ]Both scans return valid JSON arrays.
- [ ]The third call receives the original Terraform and both reports.
- [ ]`fixed_main.tf` is generated at `/root/openaiproject/fixed_main.tf`.
- [ ]The instance type and security group are corrected.
- [ ]Terraform formatting and validation checks pass.

One final point: do not deploy the generated file just because the script prints success. Review the SSH CIDR, instance sizing, and HCL validation first. The script confirms that the file was written; it does not prove that the configuration is production-ready.