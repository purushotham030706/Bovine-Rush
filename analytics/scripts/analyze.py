import json
import os
import pandas as pd  # pd is the standard nickname everyone uses

# ---- Step 1: Load all sessions (same as before) ----

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


# ---- Step 2: Convert to DataFrame ----

sessions = load_sessions("data")
df = pd.DataFrame(sessions)

# ---- Step 3: Let's explore it ----

print("=== First 5 rows ===")
print(df.head())

print("\n=== Shape (rows, columns) ===")
print(df.shape)

print("\n=== Column names ===")
print(df.columns.tolist())

print("\n=== Data types ===")
print(df.dtypes)

print("\n=== Basic statistics ===")
print(df.describe())

# ---- Step 4: Data Cleaning ----

print("\n=== Missing Values ===")
print(df.isnull().sum())

print("\n=== Any impossible values? ===")
print("Negative time_survived:", (df["time_survived"] < 0).sum())
print("Negative score:", (df["score"] < 0).sum())
print("Negative jumps:", (df["jumps"] < 0).sum())

print("\n=== Caught column unique values ===")
print(df["caught"].unique())

# ---- Step 5: Feature Engineering ----

print("\n=== Feature Engineering ===")

# Wheat collection efficiency
df["wheat_per_second"] = df["wheat_collected"] / df["time_survived"]

# Scoring efficiency
df["score_per_second"] = df["score"] / df["time_survived"]

# Jump rate
df["jump_rate"] = df["jumps"] / df["time_survived"]

# Round all new features to 3 decimal places
df["wheat_per_second"] = df["wheat_per_second"].round(3)
df["score_per_second"] = df["score_per_second"].round(3)
df["jump_rate"] = df["jump_rate"].round(3)

print("New features created successfully!")
print("\n=== Updated DataFrame columns ===")
print(df.columns.tolist())

print("\n=== Sample of new features ===")
print(df[["session_id", "time_survived", "wheat_collected",
          "wheat_per_second", "score_per_second", "jump_rate"]].head(10))

# ---- Step 6: EDA ----

print("\n" + "="*50)
print("EXPLORATORY DATA ANALYSIS")
print("="*50)

# --- 6a: Basic distributions ---
print("\n--- Score Distribution ---")
print(f"Mean score:    {df['score'].mean():.2f}")
print(f"Median score:  {df['score'].median():.2f}")
print(f"Std deviation: {df['score'].std():.2f}")
print(f"Min score:     {df['score'].min()}")
print(f"Max score:     {df['score'].max()}")

print("\n--- Survival Time Distribution ---")
print(f"Mean survival:   {df['time_survived'].mean():.2f}s")
print(f"Median survival: {df['time_survived'].median():.2f}s")
print(f"Min survival:    {df['time_survived'].min():.2f}s")
print(f"Max survival:    {df['time_survived'].max():.2f}s")

# --- 6b: Caught vs Not Caught analysis ---
print("\n--- Caught vs Escaped Analysis ---")
caught_groups = df.groupby("caught")[
    ["score", "time_survived",
     "wheat_collected", "obstacles_hit"]
].mean().round(2)
print(caught_groups)

# --- 6c: Correlation analysis ---
print("\n--- Correlation Matrix ---")
corr = df.corr(numeric_only=True).round(3)
print(corr)

# --- 6d: Top and bottom performers ---
print("\n--- Top 3 Sessions by Score ---")
print(df[["session_id", "score",
          "time_survived", "wheat_collected",
          "caught"]].nlargest(3, "score"))

print("\n--- Bottom 3 Sessions by Score ---")
print(df[["session_id", "score",
          "time_survived", "wheat_collected",
          "caught"]].nsmallest(3, "score"))

# --- 6e: Wheat efficiency analysis ---
print("\n--- Wheat Efficiency (wheat_per_second) ---")
print(f"Average: {df['wheat_per_second'].mean():.3f}")
print(f"Most efficient session:")
best = df.loc[df['wheat_per_second'].idxmax()]
print(f"  {best['session_id']} — "
      f"{best['wheat_per_second']} wheat/sec")
