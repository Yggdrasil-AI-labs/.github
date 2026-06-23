# Yggdrasil AI Labs

Self-hosted AI operations & signals (SIGINT) tooling — open-source tools that turn real-world RF into clean, structured data, on gated CI/CD.

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

## AI Ops

Yggdrasil AI Labs is a self-hosted lab for applied AI engineering: building local-first systems end to end, then running them hard enough to find the limits. The feeders above turn real-world RF into structured data. The lab itself is operated by a fleet of around twenty small, single-purpose agents that handle the work a person would otherwise do by hand, so the engineering effort goes into building and stress-testing, not babysitting.

The design is local-first. Agents run inference on local GPUs and only fall back to a hosted model when a task needs it, which keeps recurring work cheap and on-prem. Each agent is a small, dependency-light service that writes its own state and journal, fails safe, and reports to a shared dashboard, so the fleet stays observable and any one piece can be reasoned about in isolation.

**Do the work:** Seer (image understanding + OCR), Scribe (speech-to-text), Janitor (knowledge-base hygiene), Librarian (canonical writing + cross-linking), Secretary (documentation-coverage audit), Recruiter (proposes a new agent when recurring work justifies one), Triage (classifies + routes incoming notes), Researcher (drains a research queue into synthesis notes).

**Run the lab:** Heimdall (job orchestrator with concurrency limits + priorities), Doctor (scheduled health checks with safe auto-fixes), Forseti (the local model that reasons over Doctor's findings), Probe (integration smoke tests across every component), Vidar (remote-host + mesh-node reachability with an expected-offline allowlist).

**Watch the lab:** Bursar (per-agent cost + local-vs-cloud routing), Quartermaster (local model + GPU-fit management), Evaluator (a fixed eval set that gates local-model quality over time), Sentinel (defensive posture checks on the lab's own surfaces), Norn (configuration-drift detection against a declared baseline), Herald (a daily rollup brief), Cartographer (regenerates the live architecture map from real state).

Together they form a loop: workers do tasks on the local-first tier, everything writes to a shared state layer, and the watchers read it back to keep the fleet cheap, correct, and current. Same discipline as the feeders: small single-responsibility services, local-first compute, gated changes, no telemetry.
