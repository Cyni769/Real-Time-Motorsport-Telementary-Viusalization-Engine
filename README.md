# F1 Race Replay — Single-Session Demo

A stripped-down, single-session sample of the F1 Race Replay project.

- **One race only:** 2026 Formula 1 Australian Grand Prix (Season Round 1, Race)
- **Original default visualization:** the classic look — circle cars, colored HUD,
  no dark theme, no new UI updates, DRS zones, safety car animation, tyre info,
  leaderboard, weather, progress bar, race controls
- **Instant open:** all data is pre-cached, no downloads on launch

## How to run

```bash
/home/rel/Documents/projects/f1-race-replay/venv/bin/python main.py
```

This project reuses the venv from the full project — it has all dependencies
(fastf1, arcade, PySide6, etc.) already installed.

## Controls (original)

- **Space** — pause / resume
- **← / →** — rewind / fast-forward (hold)
- **↑ / ↓** — playback speed (0.1x → 256x)
- **1–4** — set speed directly (0.5x / 1x / 2x / 4x)
- **R** — restart replay
- **D** — toggle DRS zones
- **B** — toggle progress bar
- **L** — toggle driver labels on track
- **H / click Help** — show controls popup
- **Click a driver on the leaderboard** — select / shift+click multi-select
- **Esc** — close

## Where the data lives

| Path | What it is |
|------|-----------|
| `.fastf1-cache/` | raw fastf1 cache for the Australian GP (offline-capable) |
| `computed_data/*.pkl` | precomputed 25fps frame telemetry (loads instantly) |

Delete `computed_data/*.pkl` (or run `main.py --refresh-data`) to force a
recompute from the cached fastf1 data. Delete the fastf1 cache too and the
app will re-download from the web (requires network).

> **Note (clone from GitHub):** the caches above are excluded from git
> (`computed_data/` and `.fastf1-cache/` are gitignored) because the telemetry
> pickle is ~300 MB. On a fresh clone, run `main.py --refresh-data` once and it
> will rebuild the cache from the fastf1 API (requires network).

## What was trimmed from the full project

- All other Grands Prix (only Round 1 remains in the caches)
- GUI race-selection menu (PySide6) — launches straight into the replay
- Auto-launching Insights menu & telemetry viewer subprocess
- The recent UI/UX work is NOT applied: this is the pre-update default look
- One functional fix was kept: the Wayland/pyglet `maximize()`-at-startup crash
  fix, so the demo window opens cleanly on this machine

## Files

- `main.py` — entry point, hardcoded to Round 1 Australian GP
- `src/interfaces/race_replay.py` — Arcade replay renderer
- `src/ui_components.py` — HUD components
- `src/f1_data.py` — data pipeline (fastf1 → frames → pkl cache)
- `src/bayesian_tyre_model.py`, `src/tyre_degradation_integration.py` — tyre model
- `src/services/stream.py` — telemetry broadcaster (disabled in demo)
- `images/` — control / tyre / weather / tyre-strategy texture assets