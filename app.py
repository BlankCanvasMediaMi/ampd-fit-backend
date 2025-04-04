from flask import Flask, request, jsonify
from flask_cors import CORS
from workout_selector import get_workout_by_genre_and_bpm
from badge_logic import get_badges_for_user, award_badges
import json
import os

app = Flask(__name__)
CORS(app)  # ✅ ALLOW frontend to access backend routes

@app.route('/get_workout')
def get_workout():
    genre = request.args.get('genre')
    bpm = request.args.get('bpm')

    if not genre or not bpm:
        return jsonify({"error": "Genre and BPM are required"}), 400

    try:
        bpm = int(bpm)
    except ValueError:
        return jsonify({"error": "BPM must be a number"}), 400

    workout = get_workout_by_genre_and_bpm(genre, bpm)
    return jsonify(workout)

@app.route('/get_badges')
def get_badges():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    badges = get_badges_for_user(user_id)
    return jsonify(badges)

@app.route('/complete_workout')
def complete_workout():
    user_id = request.args.get('user_id')
    genre = request.args.get('genre')
    bpm = request.args.get('bpm')

    if not user_id or not genre or not bpm:
        return jsonify({"error": "user_id, genre, and bpm are required"}), 400

    try:
        bpm = int(bpm)
    except ValueError:
        return jsonify({"error": "BPM must be a number"}), 400

    updated_badges = award_badges(user_id, genre, bpm)
    return jsonify(updated_badges)

@app.route('/get_user_workouts')
def get_user_workouts():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    try:
        with open("data/user_workouts.json", encoding="utf-8") as f:
            all_logs = json.load(f)
            history = all_logs.get(str(user_id), [])
            return jsonify(history)
    except FileNotFoundError:
        return jsonify([])

@app.route('/get_move_demo')
def get_move_demo():
    move_name = request.args.get('name')
    if not move_name:
        return jsonify({"error": "Move name is required"}), 400

    try:
        with open("data/move_demos.json", encoding="utf-8") as f:
            all_moves = json.load(f)
            move = all_moves.get(move_name)
            if move:
                return jsonify(move)
            else:
                return jsonify({"error": f"No demo found for '{move_name}'"}), 404
    except FileNotFoundError:
        return jsonify({"error": "Demo file not found"}), 500

if __name__ == '__main__':
    app.run(debug=True)
