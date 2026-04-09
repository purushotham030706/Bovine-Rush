import json, os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# --- Load Data ---
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
                st.warning(f"Skipped {filename} — reason: {e}")
    return all_sessions

sessions = load_sessions("../data")
df = pd.DataFrame(sessions)
df["wheat_per_second"] = (df["wheat_collected"] / df["time_survived"]).round(3)
df["score_per_second"] = (df["score"] / df["time_survived"]).round(3)
df["jump_rate"] = (df["jumps"] / df["time_survived"]).round(3)

# --- Title ---
st.title("🐄 Bovine Rush — Analytics Dashboard")
st.markdown("Analytics pipeline built by Gaurang | 2nd Year CSE | SJEC")

# --- Raw Data ---
st.header("📋 Raw Session Data")
st.dataframe(df)

# --- Charts ---
st.header("📊 Visualizations")

# Chart 1
fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.hist(df["score"], bins=8, color="steelblue", edgecolor="white")
ax1.axvline(df["score"].mean(), color="red", linestyle="--", label="Mean Score")
ax1.set_title("Score Distribution Across Sessions")
ax1.set_xlabel("Score")
ax1.set_ylabel("Number of Sessions")
ax1.legend()
st.pyplot(fig1)
plt.close()

# Chart 2
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.scatter(df["time_survived"], df["score"], color="steelblue", alpha=0.7, s=80)
ax2.set_title("Score vs Time Survived")
ax2.set_xlabel("Time Survived (seconds)")
ax2.set_ylabel("Score")
st.pyplot(fig2)
plt.close()

# Chart 3
colors = df["caught"].map({True: "red", False: "green"})
fig3, ax3 = plt.subplots(figsize=(10, 6))
ax3.scatter(df["jump_rate"], df["time_survived"], c=colors, alpha=0.7, s=80)
ax3.set_title("Jump Rate vs Time Survived\n(Red=Caught, Green=Escaped)")
ax3.set_xlabel("Jump Rate (jumps per second)")
ax3.set_ylabel("Time Survived (seconds)")
st.pyplot(fig3)
plt.close()

# Chart 4
caught_avg = df.groupby("caught")[["score", "time_survived",
    "wheat_collected"]].mean().round(2)
x = range(len(caught_avg.columns))
width = 0.35
fig4, ax4 = plt.subplots(figsize=(10, 6))
escaped_vals = caught_avg.loc[False].values
caught_vals = caught_avg.loc[True].values
ax4.bar([i - width/2 for i in x], escaped_vals, width, label="Escaped", color="green", alpha=0.7)
ax4.bar([i + width/2 for i in x], caught_vals, width, label="Caught", color="red", alpha=0.7)
ax4.set_title("Escaped vs Caught — Average Metrics")
ax4.set_xticks(list(x))
ax4.set_xticklabels(["Avg Score", "Avg Time Survived", "Avg Wheat Collected"])
ax4.legend()
st.pyplot(fig4)
plt.close()

# Chart 5
fig5, ax5 = plt.subplots(figsize=(10, 6))
ax5.hist(df["wheat_per_second"], bins=8, color="goldenrod", edgecolor="white")
ax5.axvline(df["wheat_per_second"].mean(), color="red", linestyle="--", label="Mean Efficiency")
ax5.set_title("Wheat Collection Efficiency Distribution")
ax5.set_xlabel("Wheat per Second")
ax5.set_ylabel("Number of Sessions")
ax5.legend()
st.pyplot(fig5)
plt.close()

# --- Insights ---
st.header("💡 Key Insights")

insights = [
    "1. Players who escaped scored ~80 points higher on average. Surviving longer allows more wheat collection, which is the primary score driver — evasion and endurance are the core skills that determine performance.",
    "2. Players with higher jump rates survived significantly less time (correlation: -0.777). Excessive jumping causes mistimed landings and obstacle collisions. Controlled, deliberate jumping is a key skill.",
    "3. Wheat collection is the strongest predictor of score (correlation: 0.755). Players who focused on collecting wheat consistently outscored others.",
    "4. Session_011 achieved the highest wheat efficiency at 0.467 wheat/sec — the benchmark for optimal play.",
    "5. Score distribution is uniform with mean ≈ median, suggesting game difficulty is reasonably balanced across sessions.",
    "6. Caught players scored lower, survived less, and collected less wheat across all metrics. Being caught is a symptom of poor overall performance, not bad luck."
]

for insight in insights:
    st.markdown(f"- {insight}")
