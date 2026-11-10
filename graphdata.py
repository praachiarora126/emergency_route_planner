import os
import osmnx as ox
import numpy as np

# Location of the downloaded Hyderabad road network
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GRAPH_FILE = os.path.join(BASE_DIR, "data", "hyderabad_roads.graphml")


def load_graph():
    """Load the Hyderabad road network from the GraphML file."""
    if not os.path.exists(GRAPH_FILE):
        raise FileNotFoundError(
            f"Road network not found: {GRAPH_FILE}"
        )

    graph = ox.load_graphml(GRAPH_FILE)
    print(f"Hyderabad road network loaded: {len(graph.nodes)} nodes")
    return graph


# Load once when the backend starts
G = load_graph()

# Cache coordinate arrays once. This avoids OSMnx's optional scikit-learn
# dependency for each individual nearest-intersection lookup.
_NODE_IDS = list(G.nodes)
_NODE_LATS = np.fromiter((float(G.nodes[n]["y"]) for n in _NODE_IDS), dtype=float)
_NODE_LONS = np.fromiter((float(G.nodes[n]["x"]) for n in _NODE_IDS), dtype=float)


def get_nearest_node(latitude, longitude):
    """Find the nearest road intersection to given coordinates."""
    # Hyderabad is compact enough for a vectorized haversine scan, and this
    # works with the project's existing NumPy install even without scikit-learn.
    lat, lon = np.radians(float(latitude)), np.radians(float(longitude))
    node_lats = np.radians(_NODE_LATS)
    node_lons = np.radians(_NODE_LONS)
    dlat = node_lats - lat
    dlon = node_lons - lon
    hav = np.sin(dlat / 2) ** 2 + np.cos(lat) * np.cos(node_lats) * np.sin(dlon / 2) ** 2
    return _NODE_IDS[int(np.argmin(hav))]


def get_node_coordinates(node):
    """Return latitude and longitude of a graph node."""
    data = G.nodes[node]
    return {
        "lat": float(data["y"]),
        "lon": float(data["x"])
    }
