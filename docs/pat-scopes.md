# GitHub Personal Access Token Scopes

The contribution automation requires a GitHub personal access token (PAT) with scopes that permit cloning repositories and reading contribution data.

## Required scopes
| Scope | Why it is needed |
| --- | --- |
| `repo` (or `public_repo` for public repositories) | Grants access to clone the target repository and enumerate commits. |
| `workflow` (optional) | Allows the automation to dispatch workflows or read workflow logs if extended to trigger downstream jobs. |

The minimal scope for public repositories is `public_repo`. Use `repo` when the target repository is private.

## Creating the PAT
1. Navigate to [https://github.com/settings/tokens](https://github.com/settings/tokens).
2. Generate a **Fine-grained personal access token** with the scopes listed above.
3. Copy the token value and store it securely. Add it to your `.env` file as `CONTRIB_PAT` or configure it as a secret in CI.

Rotate the PAT regularly and revoke it immediately if it is exposed.
