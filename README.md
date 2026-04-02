# UPIBR-automation

Automates the SRF Unified Patch Integrated Build & Release (UPIBR) process using GitHub Actions.

## Runner

All workflows use a **self-hosted runner** with the `node16` label:
```
runs-on: [self-hosted, node16]
```

## Workflows

| Workflow | Description |
|---|---|
| `SRF-Exp-UP-build.yml` | Experimental UP patch build |
| `SRF-Debug-UP.yml` | Debug UP patch build |
| `json-reader.yml` | Reads JSON milestone/entry criteria files |
| `kerberos-setup.yml` | Sets up Kerberos authentication |
| `user-switch-new.yml` | Handles user switching during build |
| `test-runner.yml` | Runs validation tests |

## How to Run

1. Go to the **Actions** tab
2. Select the desired workflow
3. Click **Run workflow** and fill in the inputs

## Maintainer

[@PrathyushaKummara23](https://github.com/PrathyushaKummara23)