# g0

## Overview
The **g0** project automates contribution tracking by fetching commits from a target repository and aggregating them into local data that can be queried or reported. The automation is designed to run locally or on a schedule in CI so contribution metadata stays current without manual bookkeeping.

## Prerequisites
- Python 3.11 or later.
- `git` command-line tools for cloning and manipulating repositories.
- A GitHub personal access token (PAT) with appropriate scopes (see [docs/pat-scopes.md](docs/pat-scopes.md)).

## Setup

### Environment variables
The automation reads configuration from environment variables or a `.env` file located at the repository root.

| Variable | Required | Description |
| --- | --- | --- |
| `TARGET_REPO` | Yes | Fully qualified `<owner>/<repo>` name of the contribution source repository. |
| `CONTRIB_PAT` | Yes | GitHub PAT used to authenticate against the target repository and GitHub API. |

### Installation
1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install project dependencies:
   ```bash
   pip install -U pip
   pip install -e .
   ```

### Configure `.env`
Create a `.env` file at the project root to store secrets securely for local development:
```dotenv
TARGET_REPO=octo-org/example
CONTRIB_PAT=ghp_exampletoken
```
Ensure the `.env` file is excluded from version control (see `.gitignore`).

### Expected repository layout
During execution the automation clones and caches the target repository at `.cache/contribution_repo`. The cache directory is reused across runs to reduce network overhead; delete it if you need a clean clone.

## Running locally
Execute the contribution adder module directly. Common options include:
```bash
python -m contribution_adder \
    --seed main \
    --worktree latest
```

- `--seed` sets the branch or commit that seeds the aggregation (defaults to the default branch when omitted).
- `--worktree` controls which worktree (or tag) is updated in the cache. Provide unique names to maintain multiple snapshots.

Run `python -m contribution_adder --help` for the full CLI reference.

## Testing
Run unit tests with `pytest`:
```bash
pytest
```
Ensure tests pass before opening a pull request or merging changes.

## Continuous Integration
Once the scheduled GitHub Actions workflow is added, it should:
1. Install dependencies and hydrate secrets (`TARGET_REPO`, `CONTRIB_PAT`).
2. Execute the contribution aggregation task on a fixed cadence (for example, daily via `schedule` triggers).
3. Publish updates or artifacts as needed based on workflow outputs.

Configure the workflow to retry transient failures and surface detailed logs to simplify troubleshooting.

## Troubleshooting
- **Git authentication errors:** Verify that `CONTRIB_PAT` is valid, has the required scopes, and is not expired. Regenerate the token if authentication continues to fail.
- **Retry loop failures:** The automation retries transient fetch or API errors. Persistent failures usually indicate permission issues or incorrect repository names. Clear `.cache/contribution_repo` and re-run locally to rule out stale worktrees.
- **Missing environment variables:** Confirm that both `TARGET_REPO` and `CONTRIB_PAT` are exported in your shell or defined in `.env`.

For detailed guidance on PAT scopes, refer to [docs/pat-scopes.md](docs/pat-scopes.md).
