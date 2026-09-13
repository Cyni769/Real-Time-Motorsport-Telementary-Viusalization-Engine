import argparse
import logging
import os
import sys

from src.f1_data import (
    get_race_telemetry,
    enable_cache,
    get_circuit_rotation,
    load_session,
)
from src.run_session import run_arcade_replay

SAMPLE_YEAR = 2026
SAMPLE_ROUND = 1  # Australian Grand Prix
SAMPLE_SESSION = 'R'


def main(year=SAMPLE_YEAR, round_number=SAMPLE_ROUND, session_type=SAMPLE_SESSION,
         playback_speed=1, visible_hud=True):
    print(f"Loading F1 {year} Round {round_number} Session '{session_type}'")

    enable_cache()

    session = load_session(year, round_number, session_type)
    print(f"Loaded session: {session.event['EventName']} - {session.event['RoundNumber']} - {session_type}")

    race_telemetry = get_race_telemetry(session, session_type=session_type)

    example_lap = None
    try:
        print("Attempting to load qualifying session for track layout...")
        quali_session = load_session(year, round_number, 'Q')
        if quali_session is not None and len(quali_session.laps) > 0:
            fastest_quali = quali_session.laps.pick_fastest()
            if fastest_quali is not None:
                quali_telemetry = fastest_quali.get_telemetry()
                if 'DRS' in quali_telemetry.columns:
                    example_lap = quali_telemetry
                    print(f"Using qualifying lap from driver {fastest_quali['Driver']} for DRS Zones")
    except Exception as e:
        print(f"Could not load qualifying session: {e}")

    if example_lap is None:
        fastest_lap = session.laps.pick_fastest()
        if fastest_lap is not None:
            example_lap = fastest_lap.get_telemetry()
            print("Using fastest race lap (DRS detection may use speed-based fallback)")
        else:
            print("Error: No valid laps found in session")
            return

    drivers = session.drivers
    circuit_rotation = get_circuit_rotation(session)

    session_info = {
        'event_name': session.event.get('EventName', ''),
        'circuit_name': session.event.get('Location', ''),
        'country': session.event.get('Country', ''),
        'year': year,
        'round': round_number,
        'date': session.event.get('EventDate', '').strftime('%B %d, %Y') if session.event.get('EventDate') else '',
        'total_laps': race_telemetry['total_laps'],
        'circuit_length_m': float(example_lap["Distance"].max()) if example_lap is not None and "Distance" in example_lap else None,
    }

    run_arcade_replay(
        frames=race_telemetry['frames'],
        track_statuses=race_telemetry['track_statuses'],
        example_lap=example_lap,
        drivers=drivers,
        playback_speed=playback_speed,
        driver_colors=race_telemetry['driver_colors'],
        title=f"{session.event['EventName']} - {'Sprint' if session_type == 'S' else 'Race'}",
        total_laps=race_telemetry['total_laps'],
        circuit_rotation=circuit_rotation,
        visible_hud=visible_hud,
        session_info=session_info,
        session=session,
        enable_telemetry=False,
        race_control_messages=race_telemetry.get('race_control_messages', [])
    )


if __name__ == "__main__":
    if "--verbose" not in sys.argv:
        logging.getLogger("fastf1").setLevel(logging.CRITICAL)

    parser = argparse.ArgumentParser(description="F1 Race Replay - sample (one session)")
    parser.add_argument("--playback-speed", type=float, default=1.0, help="Initial playback speed")
    parser.add_argument("--no-hud", action="store_true", help="Launch with HUD hidden")
    parser.add_argument("--round", type=int, default=SAMPLE_ROUND, help=f"Season round (default {SAMPLE_ROUND})")
    args = parser.parse_args()

    main(
        playback_speed=args.playback_speed,
        visible_hud=not args.no_hud,
        round_number=args.round,
    )