from flask import Blueprint, request, jsonify
import json
import os

api = Blueprint("api", __name__)

DATA_FILE = "cars.json"

def load_cars():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_cars(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@api.route("/")
def home():
    return jsonify({"message": "API fungerar!"})

@api.route("/cars", methods=["GET"])
def get_cars():
    cars = load_cars()
    return jsonify(list(cars.values()))

@api.route("/cars", methods=["POST"])
def add_car():
    data = request.get_json()
    if not data or "reg" not in data:
        return jsonify({"error": "Regnummer saknas"}), 400

    cars = load_cars()
    reg = data["reg"].upper()

    if reg in cars:
        return jsonify({"error": "Bil finns redan"}), 400

    data["reg"] = reg
    cars[reg] = data
    save_cars(cars)

    return jsonify(data), 201

@api.route("/cars/<reg>", methods=["GET"])
def get_car(reg):
    cars = load_cars()
    reg = reg.upper()

    if reg not in cars:
        return jsonify({"error": "Bil hittades inte"}), 404

    return jsonify(cars[reg]), 200

@api.route("/cars/<reg>", methods=["PUT"])
def update_car(reg):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Skicka JSON-body"}), 400

    cars = load_cars()
    reg = reg.upper()

    if reg not in cars:
        return jsonify({"error": "Bil hittades inte"}), 404

    data["reg"] = reg
    cars[reg] = data
    save_cars(cars)

    return jsonify(data), 200

@api.route("/cars/<reg>", methods=["DELETE"])
def delete_car(reg):
    cars = load_cars()
    reg = reg.upper()

    if reg not in cars:
        return jsonify({"error": "Bil hittades inte"}), 404

    deleted = cars.pop(reg)
    save_cars(cars)

    return jsonify({"deleted": deleted}), 200