---
name: blazium-games-deploy
description: Ship game builds to Blazium Games from CI or the command line. Issues rotated deploy keys, registers a build and uploads its zipped files and Breakpad symbols with the chauffeur CLI (or the upload API), and wires the build_id into crash reporting. Use when the user wants to deploy, upload, publish a build, upload symbols or store images, or set up GitHub Actions or GitLab CI for Blazium Games.
license: MIT
---

# Blazium Games: Deploy Builds

Register a build, upload its files, and keep the returned `build_id` for crash reporting. Builds and symbols only upload through the chauffeur CLI or the upload API with the game's deploy key. Store images upload through chauffeur or the game's edit page on the website. MCP can list and delete them but never uploads.

## Invoke This Skill When

- "Deploy my game to Blazium Games", "upload a build", "set up CI for Blazium Games"
- "Upload my debug symbols", "upload my screenshots"
- The user has a built game folder and a Blazium Games store page
- A CI job needs `BLAZIUM_ACCESS_TOKEN` / `BLAZIUM_SECRET_KEY`

## Prerequisites

- The `blazium-games` MCP server is connected with write access (see `blazium-games-get-started`)
- A store page exists. If not, run `blazium-games-store-page` first
- The game owner's email is verified. Uploads for an unverified owner fail with code `4096`. Check with `get_account` (`email_verified`); if needed, call `request_email_code`, ask the human for the code, and call `verify_email`. A game admin cannot verify for the owner
- chauffeur, from `https://cdn.blazium.online/tools/chauffeur/<platform>/latest/archive/default` where `<platform>` is `windows-amd64`, `linux-amd64`, `linux-arm64`, `darwin-amd64`, or `darwin-arm64`. The zip contains the `chauffeur` binary

## 1. Read deploy info

Call `get_deploy_info` with the game's `uid` or vanity name. It returns (no secrets):

| Field | Use |
|-------|-----|
| `endpoints.upload_build` | `https://api.blazium.online/api/v1/tool/upload/build` |
| `endpoints.crash_ingest` | Crash reporter endpoint |
| `endpoints.events_ingest` | Events endpoint |
| `builds[]`, `latest_build_id` | Existing builds and their `build_id` |
| `keys[]` | Prefixes of existing deploy keys |
| `env` | Env var names to set in CI (`BLAZIUM_ACCESS_TOKEN`, `BLAZIUM_SECRET_KEY`, `BLAZIUM_API_URL`, `BLAZIUM_UPLOAD_URL`) plus `BLAZIUM_GAMES_APP_ID` and the latest `BLAZIUM_GAMES_BUILD_ID` for crash reporting |

## 2. Get deploy credentials

If the user already has an access token and secret stored in CI, skip this step.

Issuing a key needs developer mode on the account; `4105` means the human must turn it on at https://blazium.games/settings first.

Otherwise **warn first**: `request_deploy_key` immediately invalidates every previous deploy key for that game, which breaks any pipeline still using an old key. After the user confirms, call `request_deploy_key` with the `uid`. It returns `access_token` and `secret_key` once.

Tell the user to store them as CI secrets (for example GitHub Actions secrets `BLAZIUM_ACCESS_TOKEN` and `BLAZIUM_SECRET_KEY`) or in their shell environment. Do not write them into files that are committed. Do not repeat them after they are stored, and don't pass the secret with `--secret` (other processes can see it).

## 3a. Upload with chauffeur (recommended)

chauffeur reads `BLAZIUM_ACCESS_TOKEN` and `BLAZIUM_SECRET_KEY` from the environment (or `--access` and `--secret-stdin`). `chauffeur info` confirms which game the key belongs to.

1. Generate `build.yml` once: `chauffeur genbuild --version 1.0.0`
2. Optionally add changelog entries: `chauffeur addchangelog --title "..." --description "..."`
3. Register the build: `chauffeur build --asset build.yml --os windows --arch x86_64`. It prints `BLAZIUM_GAMES_APP_ID` and `BLAZIUM_GAMES_BUILD_ID`
4. Generate `addfiles.yml`: `chauffeur setfiles --version 1.0.0 --os windows --arch x86_64 --files ./export/windows`
5. Upload the files, and symbols if the user has them: `chauffeur addfiles --asset addfiles.yml --symbols ./symbols`

`addfiles` reuses the build with the same version, type, OS, arch, and channel (keeping its notes), zips the files, checksums them, and uploads them, in 16 MB chunks that resume after a dropped connection when over 64 MB. Keep `version` the same in both YAML files.

Example `build.yml`:

```yaml
version: v1
spec: build
asset:
  title: "1.0.0"
  type: "game"
  description: "First release"
  version: 1.0.0
  engine_version: "4.3"
  platforms:
    - os: windows
      arch: x86_64
      channel: stable
  changelog:
    - title: "Launch"
      description: "First public build"
```

Set `engine_version` so mods can show whether they work with the build.

### Several apps (dedicated server, editor, launcher)

A project can ship more than one app, each with its own builds and channels. Add an `app` block to both YAML files, or pass `--app server --app-name "Dedicated Server"` to `build`, `addfiles`, `genbuild`, and `setfiles`:

```yaml
asset:
  app:
    id: server
    name: Dedicated Server
```

`id` is 1-32 lowercase letters, digits, or dashes; leave the block out for the main app. The store page groups downloads by app, and clean files of a non-main app are stored as `<game>-<app>-<channel>-<os>-<arch>.zip`. A build is only reused within its own app.

Other chauffeur commands:

| Task | Command |
|------|---------|
| Symbols for an existing build | `chauffeur symbols --build-id <build_id> ./symbols` (`upload_symbols_info` returns it) |
| Store images | `chauffeur media cover art/cover.png`, `chauffeur media thumbnail art/thumb.png`, `chauffeur media add shots/*.png`, `chauffeur media list` |
| List builds, files, and symbol counts | `chauffeur builds list` |
| Machine-readable output | Add `--json`; exit codes are 0 ok, 1 usage, 2 API error, 3 network |

Errors print the API code with a hint. See https://docs.blazium.games/docs/cli/troubleshooting

## 3b. Upload API directly

Use this only when chauffeur can't run.

1. `POST https://api.blazium.online/api/v1/tool/upload/build` with headers `X-Access-Token` and `X-Secret-Key` and JSON:

   ```json
   { "version": "1.0.0", "build_type": "game", "os": "windows", "arch": "x86_64",
     "channel": "stable", "title": "1.0.0", "description": "First release",
     "changelog_items": [{ "title": "Launch", "description": "First public build" }] }
   ```

   The same version, type, OS, arch, and channel update one build instead of creating another, replacing its title, description, and changelog. The response includes `build_id`.

2. `POST https://uploader.blazium.online/api/v1/tool/upload/files` (multipart, same headers) with fields `build_id`, `os`, `arch`, `channel`, `checksum` (SHA-256 hex of the zip), and `file` (a `.zip`, max 5 GB). Folders inside the zip are kept.

   - `os`: `windows`, `macos`, `linux`, `android`, `ios`, or `web`
   - `arch`: `x86_64`, `x86`, `arm64`, `arm32`, `arm`, `universal`, `wasm32`, or `wasm`
   - `channel`: lowercase letters, digits, `-`, `_`; starts with a letter or digit; up to 32 characters
   - `app` (optional, on both calls): the app id for a second app such as a dedicated server, with `app_name` for its display name

3. For large files, open a session first: `POST https://uploader.blazium.online/api/v1/tool/upload/sessions` (same headers, form fields `filename`, `total_size`, `checksum`, `os`, `arch`, `channel`, and `build_id`). The `201` response has `session_id`, `expected_size`, `current_size`, and `expires_at` (6 hours). Send the chunks in order to `/tool/upload/files` as multipart `file` parts with `X-Upload-Session-ID` and `Content-Range: bytes <start>-<end>/<total>`. Each returns `202` until the last one finishes the upload. On an error, resume from its `current_size`.

| Error code | Meaning |
|------------|---------|
| `4020`-`4023` | Missing, unknown, or revoked deploy key headers |
| `4026` | Missing or too-long field on build registration |
| `4037` | Missing `file`, or a form that could not be read |
| `4038` | Missing build identification on file upload |
| `4039` | Build not found (register it first) |
| `4041` | Invalid `checksum`, `os`, `arch`, or `channel`, or the file is not a `.zip` |
| `4043` | Over 5 GB, or larger than the chunk's `Content-Range` (`413`) |
| `4044` | Missing or invalid session headers, or a chunk that doesn't continue the session (resume from `current_size`) |
| `4045` | Upload session not found or expired; open a new one |
| `4046` | Checksum mismatch; recompute the SHA-256 of the zip |
| `4047` | Another chunk for this session is still uploading; wait and retry |
| `4096` | The project owner must verify their email before uploading |
| `4290` / `4291` | Too many uploads or open sessions for this game; wait and retry |

Uploaded build files are private. Players download them through short-lived links after verifying their email, and paid games also need a license.

## 4. GitHub Actions

```yaml
name: Deploy to Blazium Games
on:
  push:
    tags: ["v*"]
jobs:
  deploy:
    runs-on: ubuntu-latest
    env:
      BLAZIUM_ACCESS_TOKEN: ${{ secrets.BLAZIUM_ACCESS_TOKEN }}
      BLAZIUM_SECRET_KEY: ${{ secrets.BLAZIUM_SECRET_KEY }}
    steps:
      - uses: actions/checkout@v4
      - name: Install chauffeur
        run: |
          curl -fsSL -o chauffeur.zip https://cdn.blazium.online/tools/chauffeur/linux-amd64/latest/archive/default
          unzip -o chauffeur.zip chauffeur && chmod +x chauffeur
      - name: Register build
        run: ./chauffeur build --asset build.yml --os linux --arch x86_64 --json > build.json
      # Export your game into ./export/linux here, with the build_id from build.json
      # (jq -r '.builds[0].build_id' build.json) in the crash reporter settings.
      - name: Upload files and symbols
        run: |
          ./chauffeur setfiles --version "${GITHUB_REF_NAME#v}" --os linux --arch x86_64 --files ./export/linux
          ./chauffeur addfiles --asset addfiles.yml --symbols ./symbols
```

`build.yml` must use the tag's version without the `v`. For several platforms use a matrix, and for GitLab CI see https://docs.blazium.games/docs/cli/ci

## 5. Hand off to crash reporting

Give the new `build_id` to the crash reporter as `X-Build-Id`: in Blazium Engine, write it into the export's `application/crash_reporter/build_id` project setting. `chauffeur build` prints it as `BLAZIUM_GAMES_BUILD_ID` so CI can pass it to the export step; `list_game_builds` and `get_deploy_info` return it too. Continue with `blazium-games-crash-reporting`, which also adds the standard launch events.

## Docs

- https://docs.blazium.games/docs/deploy
- https://docs.blazium.games/docs/cli
