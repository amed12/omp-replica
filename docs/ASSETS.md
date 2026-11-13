# Captured assets and runtime dependencies

This inventory describes the local source snapshot, not an upstream checkout or a promise that external registries will retain these releases. Static assets were copied without rewriting their contents. No runtime installations were performed during capture; command syntax was inspected through local help and installed package metadata.

## Payload provenance

| Destination | Local source | Captured content |
| --- | --- | --- |
| `payload/.agents/skills/` | `~/.agents/skills/` | All 10 directories, 117 files, 649,545 bytes, including hidden `.graphify_version`, every reference/rule, examples and scripts. |
| `payload/.omp/browser-relay/extension/` | `~/.omp/browser-relay/extension/` | All 5 files, 19,588 bytes: `background.js`, `manifest.json`, `options.html`, `options.js`, `LICENSE`. |
| `payload/.omp/plugins/vendor/graphify-pi/` | `~/.omp/plugins/node_modules/graphify-pi/` | Dereferenced `index.ts` and `package.json`, 9,797 bytes; the source was a symlink into the installed Graphify Python package. Three supplied legal notices are additionally retained. |

The plugin's source target was `~/.local/share/graphify-venv/lib/python3.12/site-packages/graphify/pi/`. The copy is ordinary files, not a symlink back to the capturing machine. No Python virtual environment or `node_modules` tree is bundled.

### Skills

- `captain`
- `feature-sprint`
- `graphify` — local `.graphify_version`: `0.9.102`
- `herdr`
- `omp-browser`
- `playwright-cli`
- `reverse-engineer-anything` — frontmatter metadata version: `59`
- `systematic-debugging`
- `test-driven-development`
- `vercel-react-best-practices` — metadata version: `1.0.0`, Vercel Engineering, January 2026

These are the user's actual installed instructions, including local adaptations. Upstream references do not establish that the snapshot is identical to an upstream release. No upstream commit IDs were supplied by these source directories.

## Licenses and attribution actually available

- **OMP relay extension:** supplied MIT `LICENSE` is copied unchanged. It credits Mario Zechner (2025), Can Bölük (2025–2026), and Stencil Labs, Inc. (2026). The manifest names Stencil Labs, Inc. and <https://omp.sh>.
- **Graphify skill and bridge:** installed `graphifyy==0.9.102` metadata declares Apache-2.0 and links <https://github.com/Graphify-Labs/graphify>, <https://graphify.com>, and <https://docs.graphify.com>. The bridge's `package.json` independently declares Apache-2.0. The installed distribution supplies `LICENSE`, `LICENSE-MIT`, and `NOTICE`; these are retained in the vendored bridge directory and apply to the captured Graphify material. `NOTICE` credits Safi Shamsi and the Graphify contributors (2026), and explains that earlier MIT contributions retain their original terms. The bridge manifest has no independent version field; its provenance is the containing `graphifyy` release.
- **Vercel skill:** `SKILL.md` declares MIT. The supplied README credits @shuding at Vercel. No standalone license text was present in this skill directory; none has been invented or substituted.
- **Playwright skill:** no license declaration or standalone license file was present in the copied skill directory. The separately installed runtime `@playwright/cli==0.1.23` declares Apache-2.0, Microsoft Corporation, and <https://github.com/microsoft/playwright-cli>. That runtime declaration alone does not establish the copied skill's exact provenance or license.
- **REA skill:** its references link to <https://github.com/morluto/rea>; no standalone license text or license declaration was present in the copied skill directory. The instructions mention the separately acquired `rea-agents` npm package, but no version is established by the captured skill.
- **captain, feature-sprint, herdr, omp-browser, systematic-debugging, test-driven-development:** no standalone license files or explicit license declarations were present in their source directories. Preserve the supplied files and establish permission before redistributing them outside the intended replica use; absence of a license is not a grant of rights.

The repository's own license, if any, must not be treated as relicensing these third-party or user-provided assets.

## Sensitive-data and portability inspection

The source asset inventory contained only the intended static instructions, references, examples, extension code and bridge code. It contained no symlinks within the skills tree, caches, keys, browser profiles, authentication files, databases or session/history files. The plugin directory symlink was explicitly dereferenced.

Text inspection found no concrete credential, private-key marker, or capturing-user absolute home path in the copied assets. One credential-like literal in `playwright-cli/references/request-mocking.md` was classified locally as a documentation mock-token example; its value was not disclosed during capture. These observations are scoped to these assets and are not a guarantee against all possible secret formats. References to API-key environment-variable names, example authentication/storage-state workflows, generic `/absolute/path/...` placeholders, and local loopback URLs remain unchanged because they are instructions, not copied credentials.

The relay code defaults to `ws://127.0.0.1:9224/ext` and an empty token. Any token, instance identifier or browser-session identifier is read/generated in Chrome storage at runtime, not embedded in these files. Chrome extension storage and browser profiles were not copied. The extension requests debugger, tabs, tabGroups, storage, alarms, scripting, downloads, and `<all_urls>` permissions; enabling it grants real browser-control capability. It reports tab metadata to the local relay. Use a browser/profile and tabs that the operator explicitly authorizes, and configure any token locally without committing it.

## Runtime setup

These commands are for a fresh destination account after installing the replica's static payload. They intentionally install fresh runtime packages, rather than copying the source machine's binaries, virtual environment, browser state or caches. Existing installations should be preserved or explicitly reconciled, not silently replaced. Network package availability and fresh installation have not been tested by this capture.

### Graphify 0.9.102

Observed runtime: Python **3.12.13**, package **graphifyy 0.9.102**, venv `~/.local/share/graphify-venv`, command exposed through `~/.local/bin/graphify`. Package metadata requires Python `>=3.10`; use Python 3.12.13 to match the observed setup. The local CLI help lists `pi guard path`, and that command returned the bridge directory used above.

Create a new venv with a configured Python 3.12 interpreter (the source account uses an asdf-managed Python). If an asdf shim reports that no version is selected, select the installed Python version for your shell/project first; do not copy the original account's interpreter path.

```sh
python3.12 -m venv "$HOME/.local/share/graphify-venv"
"$HOME/.local/share/graphify-venv/bin/python" -m pip install \
  'pip==25.0.1' 'graphifyy==0.9.102' \
  'networkx==3.7' 'numpy==2.5.4' 'PyYAML==6.0.3' 'RapidFuzz==3.14.6' \
  'tree-sitter==0.25.2' 'tree-sitter-bash==0.25.1' \
  'tree-sitter-c==0.24.2' 'tree-sitter-c-sharp==0.23.5' \
  'tree-sitter-cpp==0.23.4' 'tree-sitter-elixir==0.3.5' \
  'tree-sitter-fortran==0.6.0' 'tree-sitter-go==0.25.0' \
  'tree-sitter-groovy==0.1.2' 'tree-sitter-java==0.23.5' \
  'tree-sitter-javascript==0.25.0' 'tree-sitter-json==0.24.8' \
  'tree-sitter-julia==0.23.1' 'tree-sitter-kotlin==1.1.0' \
  'tree-sitter-lua==0.5.0' 'tree-sitter-objc==3.0.2' \
  'tree-sitter-php==0.24.1' 'tree-sitter-powershell==0.26.4' \
  'tree-sitter-python==0.25.0' 'tree-sitter-ruby==0.23.1' \
  'tree-sitter-rust==0.24.2' 'tree-sitter-scala==0.26.4' \
  'tree-sitter-sql==0.3.11' 'tree-sitter-swift==0.7.4' \
  'tree-sitter-typescript==0.23.2' 'tree-sitter-verilog==1.0.3' \
  'tree-sitter-zig==1.1.2'
mkdir -p "$HOME/.local/bin"
ln -s "$HOME/.local/share/graphify-venv/bin/graphify" "$HOME/.local/bin/graphify"
export PATH="$HOME/.local/bin:$PATH"
```

The pinned arguments above are the complete installed-distribution inventory observed in that venv, not a regenerated cross-platform lockfile. `tree-sitter-sql` was present in addition to Graphify's base requirements. No semantic-provider, MCP, PDF, video, database-client or other optional extras were installed there. Native wheel availability can differ on other operating systems, architectures or Python versions.

The vendored `graphify-pi` extension imports only Node built-ins and needs no npm dependency installation of its own. Its guard invokes `graphify hook-guard search` or `graphify hook-guard read`; the CLI is found through an **absolute PATH entry outside the current project**. Ensure `~/.local/bin` is expanded when assigning `PATH`, and register the vendored bridge through the replica's OMP plugin setup. Do not run `graphify install` merely to restore these skills: the payload already contains the exact local skill, and a fresh installation could replace it. `graphify pi guard install` targets the separate Pi host rather than OMP and is not necessary here.

Code-only graph construction needs no provider key. The skill describes host-agent semantic extraction when Gemini keys are absent; CLI semantic-provider modes and optional content types have additional dependencies/credentials, acquired separately only when needed. No provider credentials are included or required to restore this snapshot.

Evidence inspected: `graphify --help`, `graphify pi guard path`, Python `--version`, `python -m venv --help`, `python -m pip install --help`, installed `METADATA`, license files, and distribution names/versions from `importlib.metadata`.

### Playwright CLI 0.1.23

Observed entry point: `~/.local/bin/playwright-cli`, a symlink to `~/.local/lib/node_modules/@playwright/cli/playwright-cli.js`.

Installed package metadata:

- `@playwright/cli`: **0.1.23**
- `playwright`: **1.65.0-alpha-2026-10-30**
- `playwright-core`: **1.65.0-alpha-2026-10-30**
- Node engine requirement: **>=18**
- License: **Apache-2.0**

```sh
npm install --global --prefix "$HOME/.local" '@playwright/cli@0.1.23'
export PATH="$HOME/.local/bin:$PATH"
# Only when using a separately managed Chromium browser:
playwright-cli install-browser chromium
```

The CLI package pins both Playwright dependencies to the exact versions above. Browser downloads are not bundled. An existing Chrome or an explicitly selected browser may instead be used according to CLI help. Do not copy browser profiles, cookies, Playwright session storage or saved authentication state from the source account.

Do not run `playwright-cli install --skills` to restore these instructions: that command installs/replaces a skill, whereas the payload already preserves the actual local skill and every reference. `playwright-cli install` is a workspace initializer, not a prerequisite for copying the skill.

Evidence inspected: installed `@playwright/cli/package.json`, `playwright-cli --help`, `playwright-cli install-browser --help`, `playwright-cli install --help`, and `npm install --help`.

### OMP relay extension version distinction

The source OMP installation is **18.20.0**, but the source extension's manifest has `version: "0.1.0"` and **`version_name: "18.19.0"`**. Its JavaScript also embeds `OMP_INSTALL_VERSION = "18.19.0"`. Both are intentionally preserved. This is the actual installed extension snapshot, not a silently upgraded/rebuilt 18.20.0 extension. If OMP later refreshes the extension, that is a separate runtime change.

The extension is plain shipped JavaScript/HTML with no npm imports or build requirement. Load it unpacked in a compatible Chrome/Chromium browser after placing the payload, and configure the local relay connection through its options page. Port defaults to 9224. The matching OMP relay executable and startup procedure belong to the OMP installation/setup guide, not to this static extension directory. No relay process or browser was started during capture.

### Herdr and captain: optional, not bundled

A separate x86_64 macOS `herdr` executable was present at `~/.local/bin/herdr`; it is not copied, and its version/license/distribution source is not established by these skill files. No installer command has been guessed. Install Herdr separately from a trusted source only if these workflows are needed.

Both skills remain useful as instructions, but actual Herdr control requires a Herdr-managed pane and `HERDR_ENV=1`. The captain skill additionally requires OMP and the operator's own configured Google Gemini Flash access; no model credentials or provider authorization state are included. Skills alone do not create these capabilities.

### Other instruction-only dependencies

`reverse-engineer-anything` requires a separately supplied REA CLI/MCP server and, for relevant targets, analysis providers such as Java/Ghidra, IDA, JADX, Frida, or other tools described in its references. Copying the skill does not install or register any of them. Its unpinned `npx ...@latest` examples remain unchanged as part of the exact source skill; they are not evidence of an installed or reproducibly pinned REA runtime here. Follow the skill's authorization and provider-specific setup boundaries rather than installing every mentioned tool.

`feature-sprint`, `systematic-debugging`, `test-driven-development`, and `vercel-react-best-practices` are instruction/reference assets. Their example programs and task-specific development tools are not global runtime prerequisites. The Vercel skill's README includes a contributor build workflow whose project tooling is not supplied by this captured instruction directory; it need not be run to use the skill.
