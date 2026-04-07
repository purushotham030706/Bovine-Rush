import json
import random
import os
from datetime import datetime, timedelta

# Create data folder if it doesn't exist
os.makedirs("data", exist_ok=True)

# Base timestamp - sessions spread over last 7 days
base_time = datetime.now() - timedelta(days=7)

for i in range(1, 21):  # 20 sessions

    # Simulate a realistic session
    time_survived = round(random.uniform(10.0, 120.0), 2)
    jumps = random.randint(5, 40)
    wheat_collected = random.randint(0, 20)
    obstacles_hit = random.randint(0, 10)
    score = (wheat_collected * 10) + int(time_survived * 2)
    caught = random.choice([True, False])

    # Build session timestamp
    session_time = base_time + timedelta(hours=i * 8)

    # Build the session dictionary
    session = {
        "session_id": f"session_{i:03d}",
        "timestamp": session_time.strftime("%Y-%m-%dT%H:%M:%S"),
        "score": score,
        "time_survived": time_survived,
        "jumps": jumps,
        "wheat_collected": wheat_collected,
        "obstacles_hit": obstacles_hit,
        "caught": caught
    }

    # Save to individual JSON file
    filename = f"data/session_{i:03d}.json"
    with open(filename, "w") as f:
        json.dump(session, f, indent=2)

    print(f"Created: {filename}")

print("\nDone! 20 mock sessions created.")
