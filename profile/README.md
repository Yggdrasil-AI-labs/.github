# Yggdrasil AI Labs

Self-hosted AI & SIGINT tooling. Home of the **WDGoWars feeder family** — Norse-named
tools that turn real-world captures (aircraft, Wi-Fi, LoRa mesh) into
[WDGoWars](https://wdgwars.pl) leaderboard score.

## The feeder family

| Repo | Codename | Feeds |
|---|---|---|
| [adsb-to-wdgwars](https://github.com/Yggdrasil-AI-labs/adsb-to-wdgwars) | **Muninn** | ADS-B aircraft (dump1090/readsb, tar1090, Beast, GDL-90, …) |
| [wigle-to-wdgwars](https://github.com/Yggdrasil-AI-labs/wigle-to-wdgwars) | — | WiGLE Wi-Fi / BLE wardrive CSVs |
| [meshcore-to-wdgwars](https://github.com/Yggdrasil-AI-labs/meshcore-to-wdgwars) | **Heimdall** | MeshCore LoRa mesh nodes |
| [gungnir](https://github.com/Yggdrasil-AI-labs/gungnir) | — | Shared HMAC transport (retry, cooldown, silent-drop detection) |
| [wdgwars-api-tester](https://github.com/Yggdrasil-AI-labs/wdgwars-api-tester) | — | API-surface probe / outage + 404 fingerprinting |

## How it's built

- **One transport, many feeders** — `gungnir` signs every upload with an HMAC envelope; the feeders just parse and hand off.
- **Same core, CLI + browser** — Muninn and Heimdall ship one parser as both a Python CLI and an in-browser Pyodide build.
- **Gated CI/CD on every repo** — pytest + coverage → SonarCloud quality gate → Snyk SCA → release artifact. Scanned before anything ships.
- **MIT-licensed, no telemetry.**
