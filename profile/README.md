# Yggdrasil AI Labs

Self-hosted **AI operations** and **signals (SIGINT) tooling** — open-source tools that turn real-world RF (ADS-B aircraft, Wi-Fi/BLE, LoRa mesh) into clean, structured data, shipped on a gated CI/CD pipeline with supply-chain security.

## Open-source tools

| Repo | What it does |
|---|---|
| [adsb-to-wdgwars](https://github.com/Yggdrasil-AI-labs/adsb-to-wdgwars) | Normalizes 13 ADS-B receiver dialects into one JSON schema · CLI + in-browser (Pyodide/WASM) |
| [meshcore-to-wdgwars](https://github.com/Yggdrasil-AI-labs/meshcore-to-wdgwars) | LoRa / MeshCore mesh telemetry → normalized records |
| [wigle-to-wdgwars](https://github.com/Yggdrasil-AI-labs/wigle-to-wdgwars) | WiGLE Wi-Fi / BLE wardrive CSVs → structured records |
| [gungnir](https://github.com/Yggdrasil-AI-labs/gungnir) | Shared HMAC-signed transport client — integrity, retry, cooldown, silent-drop detection |
| [wdgwars-api-tester](https://github.com/Yggdrasil-AI-labs/wdgwars-api-tester) | Contract-testing harness for an undocumented HTTP API — probe quorum + 404 fingerprinting |

## How it's built

- **One transport, many tools** — signing, retry, and back-pressure live once in `gungnir`; the tools stay small and focused.
- **Local-first** — browser builds process data in-page (Pyodide/WASM); no server sees raw input.
- **Gated CI/CD on every repo** — pytest + coverage → SonarCloud quality gate (SAST) → Snyk SCA → release artifact, enforced by branch protection on `main`.
- **MIT-licensed, no telemetry.**
