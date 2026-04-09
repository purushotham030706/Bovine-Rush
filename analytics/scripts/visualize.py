import json, os
import pandas as pd
import matplotlib.pyplot as plt

def load_sessions(data_folder):
    all_sessions = []
    files = os.listdir(data_folder)
    for filename in files:
        if filename.endswith(".json"):
            filepath = os.path.join(data_folder, filename)
            try:
                with open(filepath, "r") as f:
                    session = json.load(f)
                    all_sessions.append(session)
            except Exception as e:
                print(f"Skipped {filename} — reason: {e}")
    return all_sessions

sessions = load_sessions("../data")
df = pd.DataFrame(sessions)
df["wheat_per_second"] = (df["wheat_collected"] / df["time_survived"]).round(3)
df["score_per_second"] = (df["score"] / df["time_survived"]).round(3)
df["jump_rate"] = (df["jumps"] / df["time_survived"]).round(3)
os.makedirs("../charts", exist_ok=True)

# Chart 1: Score Distribution
plt.figure(figsize=(10, 6))
plt.hist(df["score"], bins=8, color="steelblue", edgecolor="white")
plt.title("Score Distribution Across Sessions", fontsize=14)
plt.xlabel("Score")
plt.ylabel("Number of Sessions")
plt.axvline(df["score"].mean(), color="red", linestyle="--", label="Mean Score")
plt.legend()
plt.tight_layout()
plt.savefig("../charts/score_distribution.png")
plt.close()
print("Chart 1 saved")

# Chart 2: Score vs Time Survived
plt.figure(figsize=(10, 6))
plt.scatter(df["time_survived"], df["score"], color="steelblue", alpha=0.7, s=80)
plt.title("Score vs Time Survived", fontsize=14)
plt.xlabel("Time Survived (seconds)")
plt.ylabel("Score")
plt.tight_layout()
plt.savefig("../charts/score_vs_time.png")
plt.close()
print("Chart 2 saved")

# Chart 3: Jump Rate vs Time Survived
colors = df["caught"].map({True: "red", False: "green"})
plt.figure(figsize=(10, 6))
plt.scatter(df["jump_rate"], df["time_survived"], c=colors, alpha=0.7, s=80)
plt.title("Jump Rate vs Time Survived\n(Red=Caught, Green=Escaped)", fontsize=14)
plt.xlabel("Jump Rate (jumps per second)")
plt.ylabel("Time Survived (seconds)")
plt.tight_layout()
plt.savefig("../charts/jumprate_vs_survival.png")
plt.close()
print("Chart 3 saved")

# Chart 4: Caught vs Escaped Comparison
caught_avg = df.groupby("caught")[["score", "time_survived",
    "wheat_collected"]].mean().round(2)
x = range(len(caught_avg.columns))
width = 0.35
fig, ax = plt.subplots(figsize=(10, 6))
escaped_vals = caught_avg.loc[False].values
caught_vals = caught_avg.loc[True].values
bars1 = ax.bar([i - width/2 for i in x], escaped_vals, width,
               label="Escaped", color="green", alpha=0.7)
bars2 = ax.bar([i + width/2 for i in x], caught_vals, width,
               label="Caught", color="red", alpha=0.7)
ax.set_title("Escaped vs Caught — Average Metrics", fontsize=14)
ax.set_xticks(list(x))
ax.set_xticklabels(["Avg Score", "Avg Time Survived", "Avg Wheat Collected"])
ax.legend()
plt.tight_layout()
plt.savefig("../charts/caught_vs_escaped.png")
plt.close()
print("Chart 4 saved")

# Chart 5: Wheat Efficiency Distribution
plt.figure(figsize=(10, 6))
plt.hist(df["wheat_per_second"], bins=8, color="goldenrod", edgecolor="white")
plt.title("Wheat Collection Efficiency Distribution", fontsize=14)
plt.xlabel("Wheat per Second")
plt.ylabel("Number of Sessions")
plt.axvline(df["wheat_per_second"].mean(), color="red",
            linestyle="--", label="Mean Efficiency")
plt.legend()
plt.tight_layout()
plt.savefig("../charts/wheat_efficiency.png")
plt.close()
print("Chart 5 saved")

print("\nAll 5 charts saved to charts/ folder!")
