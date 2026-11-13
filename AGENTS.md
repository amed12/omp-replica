# OMP replica: instructions for installation agents

Goal: reproduce the captured OMP setup, not invent a preferred setup. Communicate in Indonesian. Read README.md, docs/INSTALL.md, docs/ASSETS.md, and manifest.json before acting. docs/AGENT-PROMPT.md is the user-facing handoff prompt.

## Contract

1. Inventory OS/architecture, Bun, Python, Node/npm/npx, OMP, existing config, skills and plugins. Compare versions against manifest.json. Snapshot source was macOS x64; do not install its platform-specific native package on another architecture.
2. Never import credentials, auth databases, sessions, history, cookies, browser profiles, logs, caches, personal memory or install IDs. Never print secrets. The 9router key is replaced with an environment-variable reference; ask the user to supply it privately.
3. Run `python3 scripts/replica.py plan` first. This previews local changes only. It does not install software or contact providers.
4. Do not overwrite differing existing files. Back up/reconcile conflicts with the user outside this repo; do not delete their files to make the installer pass. Do not change unrelated shell/runtime setup.
5. Install runtime explicitly using `bash scripts/install-runtime.sh` only after prerequisites. Apply payload with `python3 scripts/replica.py apply`. The payload is SHA-256 checked; it is not a sandbox or cryptographic proof of publisher identity. Do not modify the manifest to disguise corruption.
6. Complete external dependency installation, plugin registration, OAuth login and browser handoffs from docs/INSTALL.md. A copied skill is not an installed runtime dependency. Do not substitute a model/provider because the captured one is inaccessible.
7. Verify file parity with `python3 scripts/replica.py verify`, then inspect OMP version, effective settings, discovered skills/plugin, actual provider response and an isolated browser scenario. Report each manual/auth/network gate separately. Never claim full parity based only on hashes.
8. Current built-in approval mode is `yolo` (auto-approves tools). Explain this before starting model-driven work. Do not silently harden or broaden it: changed security behavior is not an exact replica.
9. Auto-update is enabled in the snapshot; Chrome DevTools MCP uses `@latest`. Explain drift. Keep the captured values unless the user opts for a documented divergence.
10. Native browser relay and Chrome DevTools MCP are separate. Never open personal tabs, export cookies, enable desktop control, restart Chrome, or grant OS permissions without explicit permission. Login/MFA and extension installation require human interaction.

## Maintenance and checks

- Standard-library Python restorer, Bash runtime installer; no Python package install required.
- Narrow safety checks: `python3 -m unittest discover -s tests -v`.
- After intentional snapshot changes regenerate file hashes, inspect for secrets and update provenance/change notes. Do not commit machine state.
- No GitHub publishing without the user's permission. Keep the repository private by default if publishing is requested without a visibility choice; skill/license provenance must remain attached.
