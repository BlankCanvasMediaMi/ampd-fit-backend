import json

def get_workout_by_genre_and_bpm(genre, bpm):
    with open("data/workouts.json", "r", encoding="utf-8") as f:
        all_workouts = json.load(f)

    matching_workouts = []

    for workout in all_workouts:
        if workout["genre"].lower() != genre.lower():
            continue

        # Parse bpm range like "150-170"
        try:
            low, high = map(int, workout["bpm_range"].split("-"))
            if low <= bpm <= high:
                matching_workouts.append(workout)
        except:
            continue  # skip malformed bpm ranges

    if not matching_workouts:
        return {"error": "No matching workout found."}

    # Optional: could randomize, or return best fit
    return matching_workouts[0]
