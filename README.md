# Experimental Patch Build Automation

This repository automates the experimental debug patch build process for SRF unified patches.

## Overview

This automation replaces the manual process of building experimental debug patches by:
- Automatically generating experimental versions from baseline versions
- Creating and modifying configuration files
- Running the build process with proper error handling
- Managing manual CSS signing steps
- Validating build outputs

## Usage

### Running the Workflow

1. Go to the **Actions** tab in GitHub
2. Select **"Experimental Debug Patch Build"**
3. Click **"Run workflow"**
4. Fill in the required parameters:
   - **Baseline version**: e.g., `830003A3`
   - **OCODE path**: Full path to the OCODE file
   - **Requester name**: Your name
   - **Description**: Optional custom description
   - **Additional changes**: Optional JSON for other code changes
   - **Enable notifications**: Check to enable email notifications

# Testing Node 16 runner fix
