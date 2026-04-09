insights = [
    "1. Players who escaped scored ~80 points higher on average. Surviving longer allows more wheat collection, which is the primary score driver — evasion and endurance are the core skills that determine performance.",
    "2. Players with higher jump rates survived significantly less time (correlation: -0.777). Excessive jumping causes mistimed landings and obstacle collisions. Controlled, deliberate jumping is a key skill.",
    "3. Wheat collection is the strongest predictor of score (correlation: 0.755). Players who focused on collecting wheat consistently outscored others.",
    "4. Session_011 achieved the highest wheat efficiency at 0.467 wheat/sec — the benchmark for optimal play.",
    "5. Score distribution is uniform with mean ≈ median, suggesting game difficulty is reasonably balanced across sessions.",
    "6. Caught players scored lower, survived less, and collected less wheat across all metrics. Being caught is a symptom of poor overall performance, not bad luck."
]

with open("../insights.txt", "w") as f:
    for insight in insights:
        f.write(insight + "\n\n")

print("Insights written to insights.txt!")
