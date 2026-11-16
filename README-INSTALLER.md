# CYD Aquarium — one-click web installer kit

This folder is a **drop-in addition** to a fork of https://github.com/Lagerpun/esp32-cyd-aquarium. It does not include the original source code or prebuilt binaries. GitHub Actions compiles the original firmware and publishes the site.

## Install in your fork

1. On GitHub, **Fork** `Lagerpun/esp32-cyd-aquarium` (keep the `main` branch).
2. Copy these three paths into the **root** of your fork, preserving folders:
   - `.github/workflows/aquarium-web-installer.yml`
   - `scripts/prepare_web_installer.py`
   - `web-installer/index.html`
3. Commit/push to `main`.
4. In **Settings → Pages → Build and deployment**, set **Source = GitHub Actions**.
5. Open **Actions → Build firmware and deploy browser installer**. If the commit did not run automatically, click **Run workflow**.
6. When the run succeeds, open `https://YOUR-USERNAME.github.io/esp32-cyd-aquarium/`.

## What it does

- Runs `pio run -e esp32-2432s028r` in GitHub Actions.
- Takes `bootloader.bin`, `partitions.bin`, `firmware.bin`, and Arduino's `boot_app0.bin` from the build environment.
- Generates `web-installer/manifest.json` and copies build files to `web-installer/firmware/`.
- Deploys `web-installer/` to GitHub Pages with GitHub's official Pages actions.
- Updates the website on every push to `main` and on manual workflow runs.

## Important limitations

- The workflow has **not been executed or hardware-tested** as part of this kit; run it in your fork and test on a standard ESP32-2432S028R before sharing.
- The app uses the **default** `esp32dev` Arduino partition configuration because the current `platformio.ini` does *not* set `board_build.partitions = partitions_custom.csv`. The four offsets are the standard ESP32 Arduino layout; if you change the board, framework, or partition scheme, update and verify the script.
- The project's optional `include/WifiSecrets.h` must not be committed to a public repo; the public build runs without Wi-Fi credentials.
- Installing may erase the board's existing software and user data.
- If a Pages deployment fails, open its Actions log for the concrete failure. Your repository may have organization-level Actions or Pages restrictions.
- The original firmware is AGPL-3.0. Keep its license, notice, source availability, and attribution when distributing binaries.

## Local optional validation

With PlatformIO installed, from the aquarium source repository root:

```sh
pio run -e esp32-2432s028r
python scripts/prepare_web_installer.py
```

Then inspect the generated manifest and binaries in `web-installer/`. HTTPS (GitHub Pages) is required for the production browser flasher.
