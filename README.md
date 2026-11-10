# Wayfinder — Hyderabad Emergency Route Planner

Interactive route planner backed by a Flask API and a real OpenStreetMap driving network for Hyderabad. The map tiles and address search use OpenStreetMap services; routing is calculated locally against the bundled GraphML dataset.

## Run on Windows

In one PowerShell window:

```powershell
.\.venv\Scripts\Activate.ps1
python backend\app.py
```

Then open `frontend\index.html` in a browser. The API listens on `http://127.0.0.1:5000`.

The frontend supports address search (Nominatim), current location, A*, Greedy Best-First, BFS, and DFS. Use the named Charminar/Apollo presets or enter coordinates as `latitude, longitude`. Real travel times, traffic, closures, and emergency vehicle permissions are not part of this road graph; the displayed drive time is a rough distance-based estimate.

## Data

`backend/data/hyderabad_roads.graphml` is the project's OpenStreetMap road network extract. To refresh it, run `python backend/scripts/download_hyderabad_roads.py` (requires internet access and a potentially long Overpass request).
