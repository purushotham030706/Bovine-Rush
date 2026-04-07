import json
import os

def load_sessions(data_folder):

    all_sessions = []  # empty list, will collect all sessions here

    # Get all files in the data folder
    files = os.listdir(data_folder)

    for filename in files:

        # Only process .json files
        if filename.endswith(".json"):

            filepath = os.path.join(data_folder, filename)

            try:
                with open(filepath, "r") as f:
                    session = json.load(f)
                    all_sessions.append(session)
                    print(f"Loaded: {filename}")

            except Exception as e:
                print(f"Skipped {filename} — reason: {e}")

    print(f"\nTotal sessions loaded: {len(all_sessions)}")
    return all_sessions


# Run the loader
sessions = load_sessions("data")
