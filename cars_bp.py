from flask import Blueprint, request, jsonify
import json
import os

cars_bp = Blueprint("cars_bp", __name__)

# Så den är oberoende av vart den startar
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "cars.json")


def load_cars():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if content == "":
            return {}
        return json.loads(content)


def save_cars(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def normalize_reg(reg: str) -> str:
    return str(reg).strip().upper()


@cars_bp.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API fungerar!"}), 200


@cars_bp.route("/cars", methods=["GET"])
def get_cars():
    cars = load_cars()
    return jsonify(list(cars.values())), 200


@cars_bp.route("/cars/<reg>", methods=["GET"])
def get_car(reg):
    cars = load_cars()
    reg = normalize_reg(reg)

    if reg not in cars:
        return jsonify({"error": "Bil hittades inte"}), 404

    return jsonify(cars[reg]), 200


@cars_bp.route("/cars", methods=["POST"])
def add_car():
    data = request.get_json(silent=True)
    if not data or "reg" not in data:
        return jsonify({"error": "Regnummer saknas"}), 400

    cars = load_cars()
    reg = normalize_reg(data["reg"])

    if reg in cars:
        return jsonify({"error": "Bil finns redan"}), 409

    data["reg"] = reg
    cars[reg] = data
    save_cars(cars)

    return jsonify(data), 201


@cars_bp.route("/cars/<reg>", methods=["PUT"])
def update_car(reg):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Skicka JSON-body"}), 400

    cars = load_cars()
    reg = normalize_reg(reg)

    if reg not in cars:
        return jsonify({"error": "Bil hittades inte"}), 404

    data["reg"] = reg
    cars[reg] = data
    save_cars(cars)

    return jsonify(data), 200


@cars_bp.route("/cars/<reg>", methods=["DELETE"])
def delete_car(reg):
    cars = load_cars()
    reg = normalize_reg(reg)

    if reg not in cars:
        return jsonify({"error": "Bil hittades inte"}), 404

    deleted = cars.pop(reg)
    save_cars(cars)

    return jsonify({"deleted": deleted}), 200