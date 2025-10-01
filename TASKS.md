# Task Plan for GitHub Contribution Adder

1. **Project scaffolding and dependency setup**
   - **GUID:** b5d75779-bb72-42ff-8288-2bc0a206a27a
   - **Intent:** Prepare the repository with Python packaging, configuration handling, and baseline tooling required for the contribution adder service.
   - **Prompt for Coding Agent:**
     Set up the Python project structure under `/workspace/g0` using a `src/` layout. Create `pyproject.toml` configured for `setuptools` with dependencies `GitPython`, `python-dotenv` (optional), and `pytest`. Initialize the `src/contribution_adder/` package with `__init__.py` and add `config.py` that loads `TARGET_REPO` and `CONTRIB_PAT` from environment variables, raising a descriptive `RuntimeError` if missing. Ensure the repo-level `.gitignore` excludes virtual environments, caches, and the cloned working repo under `.cache/`. Confirm the project can install via `pip install -e .`.
   - **Expected Output:**
     `pyproject.toml`, `src/contribution_adder/__init__.py`, `src/contribution_adder/config.py`, updated `.gitignore`, and supporting packaging files (e.g., `src/contribution_adder/__main__.py` placeholder if needed) committed to the repo.
   - **Acceptance Criteria:**
     Running `pip install -e .` succeeds; `config.load_settings()` (or equivalent) returns an object containing both env vars or raises `RuntimeError` when missing; `.gitignore` covers `__pycache__/`, `.venv/`, `.cache/`, and build artifacts.
   - **Dependencies:** []
   - **Subtasks:**
     1.1. **Python package scaffold**
        - **GUID:** 6cd2153c-357b-4393-8563-f7da615b965f
        - **Intent:** Create the base `src/` package layout and packaging metadata.
        - **Prompt for Coding Agent:**
          Generate `pyproject.toml` using setuptools with `name="contribution-adder"` (or similar) and editable install support. Add `src/contribution_adder/__init__.py` exporting package metadata. Ensure project structure aligns with repository instructions in `AGENTS.md`.
        - **Expected Output:** `pyproject.toml`, `src/contribution_adder/__init__.py`.
        - **Acceptance Criteria:** `pip install -e .` resolves dependencies without errors; package imports succeed.
        - **Dependencies:** []

     1.2. **Configuration loader**
        - **GUID:** 4edaa69b-19a6-45c0-a165-b73e669bd187
        - **Intent:** Provide robust environment configuration management.
        - **Prompt for Coding Agent:**
          Implement `src/contribution_adder/config.py` with a dataclass `AppConfig` holding `target_repo: str` and `token: str`. Provide a function `load_config()` that reads `TARGET_REPO` and `CONTRIB_PAT` from `os.environ`, optionally loading from `.env` if present, and raises `RuntimeError` with actionable messaging when values are missing.
        - **Expected Output:** `src/contribution_adder/config.py` with dataclass, loader function, and docstrings.
        - **Acceptance Criteria:** `load_config()` returns `AppConfig` when env vars set; raises `RuntimeError` with message mentioning missing variable names otherwise; includes unit-test-friendly design (no side effects at import time).
        - **Dependencies:** ["6cd2153c-357b-4393-8563-f7da615b965f"]

     1.3. **Repository ignores and cache layout**
        - **GUID:** f25780e9-b2c3-43c9-8e50-56cc33331768
        - **Intent:** Ensure git ignores local environments and cached repos.
        - **Prompt for Coding Agent:**
          Update `.gitignore` to include `.venv/`, `*.egg-info`, `__pycache__/`, `.cache/`, and other common Python artifacts. Document the purpose for ignoring `.cache/` in a comment.
        - **Expected Output:** Updated `.gitignore` reflecting the required patterns.
        - **Acceptance Criteria:** `.gitignore` lists required patterns with clear comment; no conflicting entries.
        - **Dependencies:** ["6cd2153c-357b-4393-8563-f7da615b965f"]

2. **Prime selection utility implementation**
   - **GUID:** 87c28e1d-2b8f-4696-8d86-85c2d7185b62
   - **Intent:** Provide deterministic prime selection logic with reproducible randomness.
   - **Prompt for Coding Agent:**
     Build `src/contribution_adder/primes.py` offering functions to pick two primes under 30 and sum them, with optional seeding for deterministic testing.
   - **Expected Output:** `src/contribution_adder/primes.py` with documented functions, potential helper constants, and unit-test-ready design.
   - **Acceptance Criteria:** `pick_two_primes(seed)` yields the same ordered pair when called repeatedly with the same seed; functions raise `ValueError` when internal prime list is empty; includes type annotations.
   - **Dependencies:** ["b5d75779-bb72-42ff-8288-2bc0a206a27a"]
   - **Subtasks:**
     2.1. **Prime module skeleton**
        - **GUID:** 99285875-1bcb-4e89-930f-27502462c3a7
        - **Intent:** Create module with constants and basic structure.
        - **Prompt for Coding Agent:**
          Create `src/contribution_adder/primes.py` defining the constant tuple of primes under 30 and module docstring explaining purpose.
        - **Expected Output:** New module with primes constant and placeholder functions.
        - **Acceptance Criteria:** Module imports cleanly; primes list matches actual primes under 30.
        - **Dependencies:** ["4edaa69b-19a6-45c0-a165-b73e669bd187"]

     2.2. **Prime selection functions**
        - **GUID:** 6716a301-018c-4c6c-b5b4-03da586914e6
        - **Intent:** Implement the logic for selecting and summing primes.
        - **Prompt for Coding Agent:**
          Implement `pick_two_primes(random_seed: int | None = None) -> tuple[int, int]` using `random.Random` with optional seed. Ensure two distinct primes are returned. Provide `sum_primes(prime_pair: tuple[int, int]) -> int`. Include error handling and docstrings.
        - **Expected Output:** Completed functions with tests-ready logic.
        - **Acceptance Criteria:** Deterministic output when seed provided; raises `ValueError` if prime pool is empty; type hints present.
        - **Dependencies:** ["99285875-1bcb-4e89-930f-27502462c3a7"]

3. **Contribution orchestration script with Git integration**
   - **GUID:** dd63d981-43aa-4ec4-b6cf-d81d563cca4e
   - **Intent:** Automate cloning/updating the target repo and creating commits based on prime sum.
   - **Prompt for Coding Agent:**
     Develop `src/contribution_adder/contribution_runner.py` containing a `ContributionRunner` class responsible for loading config, cloning/pulling the repo into `.cache/contribution_repo`, generating the commit count via prime utilities, creating commits by appending to `contribution-log.txt`, and pushing changes with retry logic. Add CLI entry point in `src/contribution_adder/__main__.py`.
   - **Expected Output:** Fully implemented runner module and CLI entry point.
   - **Acceptance Criteria:** `ContributionRunner.run()` performs workflow with logging and retryable push attempts; uses HTTPS remote with PAT; idempotent when rerun; handles exceptions gracefully.
   - **Dependencies:** ["87c28e1d-2b8f-4696-8d86-85c2d7185b62"]
   - **Subtasks:**
     3.1. **Repository management utilities**
        - **GUID:** b7d079cb-9244-416a-b409-53c526aa8a83
        - **Intent:** Provide helper methods for cloning and syncing repos.
        - **Prompt for Coding Agent:**
          Within `contribution_runner.py`, implement functions or class methods to prepare `.cache/contribution_repo`, clone if absent using GitPython, and pull latest changes. Ensure directory creation is safe and testable.
        - **Expected Output:** Helper logic for repo cloning/updating with logging.
        - **Acceptance Criteria:** Handles existing repo without errors; raises informative exceptions on failure; includes docstrings.
        - **Dependencies:** ["6716a301-018c-4c6c-b5b4-03da586914e6"]

     3.2. **Commit generation and push workflow**
        - **GUID:** 07b55a45-1a17-40d5-bcf5-d58009c1ea0d
        - **Intent:** Implement core run loop to create commits and push changes.
        - **Prompt for Coding Agent:**
          Complete `ContributionRunner.run()` to load config, call prime utilities, append timestamped entries to `contribution-log.txt`, create commits with descriptive messages, and push after all commits are created. Include retry/backoff (at least three attempts) around the push step.
        - **Expected Output:** Operational `ContributionRunner` class and CLI entry point invoking it.
        - **Acceptance Criteria:** Run method logs key steps, writes commits, and retries pushes; ensures git index is clean between iterations.
        - **Dependencies:** ["b7d079cb-9244-416a-b409-53c526aa8a83"]

4. **Automated scheduling via GitHub Actions**
   - **GUID:** c88f8c17-56c4-4d43-aab9-3cda9eeef2c7
   - **Intent:** Schedule daily execution of the contribution runner.
   - **Prompt for Coding Agent:**
     Create `.github/workflows/contribution-adder.yml` configured to run daily at 00:05 UTC and via manual dispatch, installing dependencies and executing the CLI. Use repository secrets `CONTRIB_PAT` and `TARGET_REPO`.
   - **Expected Output:** Workflow YAML with job covering checkout, Python setup, dependency install, and script invocation.
   - **Acceptance Criteria:** Workflow passes `act` syntax validation; secrets referenced without exposing values; environment variables passed to script.
   - **Dependencies:** ["dd63d981-43aa-4ec4-b6cf-d81d563cca4e"]
   - **Subtasks:**
     4.1. **Workflow definition**
        - **GUID:** 8451849c-0297-4298-9bcf-4a661db4ce44
        - **Intent:** Draft the GitHub Actions workflow file.
        - **Prompt for Coding Agent:**
          Author `.github/workflows/contribution-adder.yml` with schedule `5 0 * * *`, manual trigger, caching for pip, and steps to run `python -m contribution_adder` with appropriate env vars.
        - **Expected Output:** Workflow YAML committed to repo.
        - **Acceptance Criteria:** YAML passes `act -l` lint (if run); structure matches GitHub Actions schema; uses `${{ secrets.CONTRIB_PAT }}` securely.
        - **Dependencies:** ["07b55a45-1a17-40d5-bcf5-d58009c1ea0d"]

5. **Unit and integration tests**
   - **GUID:** abb9cc8a-6d9b-424d-9946-60f39913878c
   - **Intent:** Provide automated test coverage for prime utilities and contribution runner.
   - **Prompt for Coding Agent:**
     Write pytest-based tests covering deterministic prime selection and the contribution workflow using temporary repos/mocks. Configure pytest discovery if needed.
   - **Expected Output:** `tests/test_primes.py`, `tests/test_contribution_runner.py`, and `pytest.ini` or equivalent.
   - **Acceptance Criteria:** `pytest` passes without contacting remote services; tests simulate retries and confirm commit counts.
   - **Dependencies:** ["dd63d981-43aa-4ec4-b6cf-d81d563cca4e"]
   - **Subtasks:**
     5.1. **Prime utility tests**
        - **GUID:** 10aab9a8-5d26-4b1b-a140-74e655cfb882
        - **Intent:** Verify correctness of prime selection functions.
        - **Prompt for Coding Agent:**
          Implement tests asserting deterministic output with seeded RNG and that returned primes are valid. Include failure case for empty prime list via monkeypatching.
        - **Expected Output:** `tests/test_primes.py` with comprehensive coverage.
        - **Acceptance Criteria:** Tests pass; leverage fixtures/monkeypatch as needed; no external dependencies.
        - **Dependencies:** ["6716a301-018c-4c6c-b5b4-03da586914e6"]

     5.2. **Contribution runner tests**
        - **GUID:** 72176f88-2dd4-4ba9-8b5e-12cecf2a1b1a
        - **Intent:** Validate end-to-end commit workflow without hitting real remotes.
        - **Prompt for Coding Agent:**
          Create tests using `tempfile.TemporaryDirectory` and initializing a bare repo as remote, verifying the runner creates the expected number of commits and handles retry logic (mock push to fail first). Provide fixtures for config/env setup.
        - **Expected Output:** `tests/test_contribution_runner.py` and supporting fixtures/modules.
        - **Acceptance Criteria:** Tests pass reliably; no network calls; ensures log file content matches commit count.
        - **Dependencies:** ["07b55a45-1a17-40d5-bcf5-d58009c1ea0d"]

     5.3. **Pytest configuration**
        - **GUID:** 46b5ba28-7351-4b6a-8757-78ffc4c6a572
        - **Intent:** Ensure pytest discovers tests consistently.
        - **Prompt for Coding Agent:**
          Add `pytest.ini` (or `pyproject.toml` section) setting `testpaths = tests` and enabling any needed markers. Include configuration for log level if required.
        - **Expected Output:** Pytest configuration file at repo root.
        - **Acceptance Criteria:** `pytest` runs without additional CLI arguments; configuration comments explain choices.
        - **Dependencies:** ["10aab9a8-5d26-4b1b-a140-74e655cfb882", "72176f88-2dd4-4ba9-8b5e-12cecf2a1b1a"]

6. **Documentation and usage guide**
   - **GUID:** 6f7432b5-de30-4af7-9de8-a4453c29c551
   - **Intent:** Document setup, operation, and troubleshooting for the app and workflow.
   - **Prompt for Coding Agent:**
     Update `/workspace/g0/README.md` with project overview, setup steps, environment variable instructions, testing commands, and GitHub Actions schedule. Add any supporting docs under `docs/` if helpful.
   - **Expected Output:** Updated `README.md` (and optional docs) with clear instructions and references.
   - **Acceptance Criteria:** Documentation accurately reflects implementation; includes sections for configuration, running locally, testing, and CI overview; language is concise and actionable.
   - **Dependencies:** ["abb9cc8a-6d9b-424d-9946-60f39913878c", "c88f8c17-56c4-4d43-aab9-3cda9eeef2c7"]
   - **Subtasks:**
     6.1. **README overhaul**
        - **GUID:** e050b349-b6a2-4088-95bd-f2921ad27497
        - **Intent:** Provide primary project documentation.
        - **Prompt for Coding Agent:**
          Rewrite `README.md` to include sections: Overview, Features, Prerequisites, Setup (including environment variables and installation), Running locally, Testing, Deployment (GitHub Actions schedule), and Troubleshooting.
        - **Expected Output:** Comprehensive README covering the above sections.
        - **Acceptance Criteria:** README renders cleanly in Markdown; includes code blocks for commands; references secrets and workflow files accurately.
        - **Dependencies:** ["8451849c-0297-4298-9bcf-4a661db4ce44", "46b5ba28-7351-4b6a-8757-78ffc4c6a572"]

     6.2. **Additional configuration doc (optional)**
        - **GUID:** fdf26ac2-5875-4445-a556-3790b09b9ae8
        - **Intent:** Document PAT scopes and repository requirements if more detail needed.
        - **Prompt for Coding Agent:**
          If required, add `docs/CONFIG.md` summarizing Personal Access Token scopes, target repo setup, and safety considerations for automated commits.
        - **Expected Output:** `docs/CONFIG.md` detailing PAT configuration and security notes (optional if README sufficient).
        - **Acceptance Criteria:** Document exists only if additional detail is necessary; provides actionable guidance; cross-referenced from README.
        - **Dependencies:** ["e050b349-b6a2-4088-95bd-f2921ad27497"]
