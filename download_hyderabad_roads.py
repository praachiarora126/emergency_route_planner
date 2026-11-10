
from pathlib import Path
import osmnx as ox

# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Create backend/data folder
DATA_DIR = BASE_DIR / "backend" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Output file
OUTPUT_FILE = DATA_DIR / "hyderabad_roads.graphml"

print("Downloading Hyderabad road network from OpenStreetMap...")
print("This may take several minutes. Please wait.")

try:
    # Download the driving road network
    G = ox.graph_from_place(
        "Hyderabad, Telangana, India",
        network_type="drive",
        simplify=True,
        retain_all=True
    )

    # Save the road network
    ox.save_graphml(G, OUTPUT_FILE)

    print("\nDownload successful!")
    print("Number of road intersections:", len(G.nodes))
    print("Number of road connections:", len(G.edges))
    print("Saved to:", OUTPUT_FILE)

except Exception as e:
    print("\nDownload failed.")
    print("Error:", e)
