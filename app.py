from flask import Flask, request, jsonify
from flask_cors import CORS
from time import perf_counter

from graphdata import G, get_nearest_node, get_node_coordinates
from algorithms import find_path, path_distance

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Emergency Route Planner API is running"
    })

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "city": "Hyderabad", "nodes": len(G.nodes), "edges": len(G.edges), "source": "OpenStreetMap"})


@app.route("/api/route", methods=["POST"])
def calculate_route():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request data is missing"}), 400

        # Get starting and destination coordinates
        start_lat = float(data["start"]["lat"])
        start_lon = float(data["start"]["lon"])

        end_lat = float(data["end"]["lat"])
        end_lon = float(data["end"]["lon"])

        algorithm = data.get("algorithm", "astar").lower()

        # Find nearest road intersections
        start_node = get_nearest_node(start_lat, start_lon)
        end_node = get_nearest_node(end_lat, end_lon)

        # Run selected algorithm
        start_time = perf_counter()

        path = find_path(
            G,
            start_node,
            end_node,
            algorithm
        )

        execution_time = (perf_counter() - start_time) * 1000

        if not path:
            return jsonify({
                "error": "No route found between these locations"
            }), 404

        # Convert graph nodes into map coordinates
        route_coordinates = [
            get_node_coordinates(node)
            for node in path
        ]

        total_distance = path_distance(G, path)

        return jsonify({
            "algorithm": algorithm,
            "route": route_coordinates,
            "total_distance_km": round(total_distance / 1000, 3),
            "execution_time_ms": round(execution_time, 3),
            "nodes_in_path": len(path),
            "message": "Route calculated successfully"
        })

    except KeyError as e:
        return jsonify({
            "error": f"Missing required field: {e}"
        }), 400

    except (TypeError, ValueError) as e:
        return jsonify({
            "error": str(e)
        }), 400

    except Exception as e:
        app.logger.exception("Route calculation failed")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
