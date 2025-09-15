# Sensewave

A cross-platform computer vision prototype that connects a device camera to a Python backend running MiDaS AI for depth perception and hazard visualization.

## Structure
- `python/tests/` → Standalone Python scripts for testing camera + MiDaS depth.
- `python/server/` → Flask backend that receives frames from devices and returns overlays.
- `unity/` → Unity frontend C# script that streams camera frames to backend and displays depth feed.
- `docs/` → Setup instructions.

## Quick Start
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
