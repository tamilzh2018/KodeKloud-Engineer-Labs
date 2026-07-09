# Day 72: Jenkins Parameterized Builds

## Task Overview

Create a Jenkins job with multiple parameter types to understand parameterized build functionality. Parameterized builds enable jobs to accept runtime inputs, making them flexible and reusable across different scenarios and environments.

**Technical Specifications:**
- Job type: Freestyle parameterized project
- Parameters: String (text input) and Choice (dropdown selection)
- Build action: Execute shell script that echoes parameter values
- Test requirement: Build with Production environment selection

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Access Jenkins UI and log in

```
Username: admin
Password: Adm!n321
```

Open the Jenkins web interface and authenticate with administrator credentials. These credentials grant full access to create, configure, and manage Jenkins jobs. The Jenkins dashboard provides centralized control over all automation workflows, build history, and system configuration. This is the starting point for all Jenkins administrative tasks.

**Step 2:** Update plugins and restart Jenkins (if needed)

Navigate to Manage Jenkins > Manage Plugins > Updates tab

Check for available plugin updates, select all, and install. Choose "Restart Jenkins when installation is complete and no jobs are running"

Keeping Jenkins plugins updated ensures you have the latest features, bug fixes, and security patches. The restart ensures new plugin versions are loaded into memory. The graceful restart option waits for running builds to complete before restarting, preventing job interruption. After restart, refresh your browser to reload the Jenkins UI with updated components.

**Step 3:** Create a new freestyle job

Dashboard > New Item
- Name: parameterized-job
- Type: Freestyle project
- Click OK

The freestyle project is Jenkins' most flexible job type, suitable for simple to moderately complex automation tasks. Unlike pipeline jobs (which use code), freestyle jobs use a GUI configuration interface. The job name should be descriptive and follow your organization's naming conventions. Once created, you'll configure build parameters, triggers, build steps, and post-build actions through the web interface.

**Step 4:** Configure string parameter

In job configuration, check "This project is parameterized"

Click "Add Parameter" > "String Parameter"
- Name: Stage
- Default value: Build
- Description: Build stage to execute (Build, Test, Deploy)

String parameters accept free-form text input from users at build time. The parameter name becomes an environment variable (accessible as $Stage in shell scripts). The default value is pre-filled in the build form but can be overridden. The description helps users understand what the parameter controls. This parameter will allow users to specify different build stages like Build, Test, or Deploy when triggering the job.

**Step 5:** Configure choice parameter

Click "Add Parameter" > "Choice Parameter"
- Name: env
- Choices: (enter one per line)
  ```
  Development
  Staging
  Production
  ```
- Description: Target deployment environment

Choice parameters present a dropdown list of predefined options, ensuring users select only valid values. Unlike string parameters (which accept any text), choice parameters enforce controlled input. The first option (Development) is selected by default. Each choice should be on a separate line in the Choices field. The parameter name becomes an environment variable ($env in shell scripts). This restricts environment selection to known, valid values, preventing typos or invalid environments.

**Step 6:** Add build step to echo parameters

In Build section, click "Add build step" > "Execute shell"

Enter the shell script:
```sh
echo "Build Stage: $Stage"
echo "Environment: $env"
```

This build step demonstrates how to access parameter values in shell scripts. Jenkins automatically creates environment variables for each parameter, named exactly as defined (case-sensitive). The echo commands print the values to the build console output. In real scenarios, you'd use these parameters to control build logic, select configuration files, or determine deployment targets. The console output verifies that parameters are correctly passed to the build execution.

**Step 7:** Save and build the job

Click "Apply" and "Save"

To execute the job:
1. Dashboard > parameterized-job > Build with Parameters
2. Observe the parameter form with:
   - Stage text field (pre-filled with "Build")
   - env dropdown (showing Development, Staging, Production)

The "Build with Parameters" link appears because you enabled parameterization. This replaces the standard "Build Now" button. Jenkins displays a form collecting all parameter values before starting the build. Users can modify the default Stage value or select a different environment from the dropdown. This interactive approach makes jobs more user-friendly and reduces errors from incorrect parameter values.

**Step 8:** Execute build with Production environment

Modify parameters:
- Stage: Build (keep default)
- env: Production (select from dropdown)

Click "Build"

Monitor the console output - you should see:
```
Build Stage: Build
Environment: Production
```

Selecting Production from the dropdown and clicking Build triggers job execution with your specified parameters. Jenkins creates a new build number (e.g., #1, #2) and runs the shell script with your parameter values. The console output displays real-time execution logs. This build demonstrates that parameters correctly flow from user input through to script execution. The build must complete successfully with Production selected to meet the task requirements.

**Step 9:** Verify build history and parameters

Dashboard > parameterized-job > Build History

Click on build #1 (or your build number) > Parameters

Verify displayed parameters:
- Stage: Build
- env: Production

Jenkins records parameter values for every build in the build history. This creates an audit trail showing exactly what parameters were used for each execution. Click any build number to view its details, including parameters, console output, and build result (success/failure). This historical record is valuable for troubleshooting, compliance, and understanding what was deployed where and when.

---

## Key Concepts

**Parameterized Builds:**
- Purpose: Make jobs flexible and reusable across different contexts without duplicating job definitions
- Runtime Configuration: Collect user input at build time rather than hardcoding values in job configuration
- Dynamic Behavior: Change build logic, deployment targets, or configuration based on parameter values
- User Input: Interactive forms collect parameters before build execution, improving usability

**Parameter Types:**
- String: Free-form text input with optional default value (for version numbers, branch names, custom values)
- Choice: Dropdown list with predefined options (for environments, regions, build types)
- Boolean: Checkbox for true/false values (for feature flags, debug mode, skip steps)
- File: Upload file as parameter (for configuration files, certificates, test data)
- Password: Masked text input that hides the value in logs and UI (for credentials, API keys)

**Parameter Access in Builds:**
- Environment Variables: All parameters automatically become environment variables in the build
- Shell Scripts: Access via $PARAMETER_NAME syntax (e.g., $Stage, $env)
- Pipeline Scripts: Access via params.PARAMETER_NAME syntax (e.g., params.Stage)
- Build Triggers: Pass parameter values to downstream jobs that trigger after this job completes

**Best Practices:**
- Default Values: Provide sensible defaults that work for most common cases (reduces user error)
- Validation: Validate parameter values in build scripts before using them (check format, existence)
- Documentation: Use description fields to explain parameter purpose, format, and valid values
- Security: Use password parameters for sensitive data; never log password parameter values
- Naming: Use clear, descriptive parameter names following consistent conventions

---

## Validation

Test your solution using KodeKloud's automated validation.

Verify:
1. Job named "parameterized-job" exists
2. String parameter "Stage" with default "Build" is configured
3. Choice parameter "env" with Development, Staging, Production options exists
4. Build executes successfully with Production environment selected
5. Console output shows both parameter values

---

[← Day 71](day-71.md) | [Day 73 →](day-73.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
