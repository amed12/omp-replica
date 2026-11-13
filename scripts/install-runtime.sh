#!/usr/bin/env bash
set -euo pipefail
# Explicitly invoked network installer. Never run this from plan/verify.
BUN_VERSION=1.4.4
OMP_VERSION=18.20.0
if ! command -v bun >/dev/null 2>&1; then
  echo 'Install Bun 1.4.4 first: https://bun.sh/docs/installation (release bun-v1.4.4)' >&2
  exit 1
fi
if [[ "$(bun --version)" != "$BUN_VERSION" ]]; then
  echo "Expected Bun $BUN_VERSION; refusing to replace your existing runtime." >&2
  exit 1
fi
if command -v omp >/dev/null 2>&1; then
  if [[ "$(omp --version)" != "omp/$OMP_VERSION" ]]; then
    echo "Existing OMP differs from $OMP_VERSION; reconcile manually, not overwritten." >&2
    exit 1
  fi
  echo "OMP $OMP_VERSION already available."
  exit 0
fi
bun add --global "@oh-my-pi/pi-coding-agent@$OMP_VERSION" "@oh-my-pi/pi-natives@$OMP_VERSION"
export PATH="$HOME/.bun/bin:$PATH"
[[ "$(omp --version)" == "omp/$OMP_VERSION" ]]
echo "Installed OMP $OMP_VERSION. Ensure \$HOME/.bun/bin is on PATH."
