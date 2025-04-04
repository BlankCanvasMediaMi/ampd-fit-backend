import json
import os
from datetime import datetime

def get_badges_for_user(user_id):
    with open("data/user_badges.json", encoding="utf-8") as f:
        user_data = json.load(f)

    with open("data/badges.json", encoding="utf-8") as f:
        all_badges = json.load(f)

    unlocked = user_data.get(str(user_id), [])
    return [badge for badge in all_badges if badge["id"] in unlocked]

def award_badges(user_id, genre, bpm):
    user_id = str(user_id)

    # Load or create badge data
    if os.path.exists("data/user_badges.json"):
        with open("data/user_badges.json", encoding="utf-8") as f:
            user_badges = json.load(f)
    else:
        user_badges = {}

    current = set(user_badges.get(user_id, []))
    new_badges = set()

    # Badge 1: First workout
    if len(current) == 0:
        new_badges.add(1)

    # Genre-specific badges
    genre_badge_map = {
        "country": 5,
        "punk": 6
    }

    genre = genre.lower()
    if genre in genre_badge_map:
        new_badges.add(genre_badge_map[genre])

    # Merge + save
    updated = list(current.union(new_badges))
    user_badges[user_id] = updated

    with open("data/user_badges.json", "w", encoding="utf-8") as f:
        json.dump(user_badges, f, indent=2)

    # Log the workout
    log_user_workout(user_id, genre, bpm)

    return get_badges_for_user(user_id)

def log_user_workout(user_id, genre, bpm):
    user_id = str(user_id)

    # Load or start workout log
    if os.path.exists("data/user_workouts.json"):
        with open("data/user_workouts.json", encoding="utf-8") as f:
            all_logs = json.load(f)
    else:
        all_logs = {}

    # Create entry if needed
    if user_id not in all_logs:
        all_logs[user_id] = []

    # Add new workout
    all_logs[user_id].append({
        "timestamp": datetime.now().isoformat(),
        "genre": genre,
        "bpm": bpm
    })

    # Save it
    with open("data/user_workouts.json", "w", encoding="utf-8") as f:
        json.dump(all_logs, f, indent=2)
