from pathlib import Path

import pandas as pd
import streamlit as st

st.title("Soccer Match Statistics Explorer")

st.markdown("""
Explore how possession, shots, and fouls are associated
with soccer match outcomes.

### Questions explored

- How do a team's results vary across selected years?
- How does shot advantage relate to win percentage?
- How does possession advantage relate to win percentage?
- How do observed win rates differ across foul ranges?
- Does adding possession improve a shots-based model?
""")

st.caption(
    "Analysis uses 1,127 matches retained after possession "
    "validation. Findings describe associations, not causal effects. "
    "Models use completed-match statistics."
)

# Find the CSV relative to app.py.
data_path = (
    Path(__file__).resolve().parent
    / "data"
    / "EuroAllMatchBoxData.csv"
)

df = pd.read_csv(data_path)

# Apply the same cleaning rule as the notebook.
valid_possession = (
    df["hPossesion"].between(1, 99)
    & df["aPossesion"].between(1, 99)
    & ((df["hPossesion"] + df["aPossesion"]) == 100)
)

subset_df = df.loc[valid_possession].copy()

st.sidebar.header("Explore matches")

year_range = st.sidebar.slider(
    "Select year range",
    min_value=int(subset_df["year"].min()),
    max_value=int(subset_df["year"].max()),
    value=(
        int(subset_df["year"].min()),
        int(subset_df["year"].max())
    )
)

filtered_df = subset_df.loc[
    subset_df["year"].between(year_range[0], year_range[1])
].copy()

# List teams appearing in the selected years.
teams = sorted(
    set(filtered_df["hname"])
    | set(filtered_df["aname"])
)

selected_team = st.sidebar.selectbox(
    "Select a team",
    options=["All teams"] + teams
)

# Keep matches where the selected team played on either side.
if selected_team != "All teams":
    filtered_df = filtered_df.loc[
        (filtered_df["hname"] == selected_team)
        | (filtered_df["aname"] == selected_team)
    ].copy()

st.metric("Selected matches", len(filtered_df))

if selected_team != "All teams":
    # Calculate goals from the selected team's perspective.
    is_home = filtered_df["hname"] == selected_team

    team_goals = filtered_df["hgoals"].where(
        is_home, filtered_df["agoals"]
    )
    opponent_goals = filtered_df["agoals"].where(
        is_home, filtered_df["hgoals"]
    )

    wins = int((team_goals > opponent_goals).sum())
    draws = int((team_goals == opponent_goals).sum())
    losses = int((team_goals < opponent_goals).sum())

    st.subheader(f"{selected_team}: selected matches")

    total_matches = len(filtered_df)

    win_percentage = (
        f"{wins / total_matches:.1%}"
        if total_matches > 0
        else "N/A"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Wins", wins)
    col2.metric("Draws", draws)
    col3.metric("Losses", losses)
    col4.metric("Win percentage", win_percentage)
    st.caption(
        f"Based on {total_matches} matches in the cleaned dataset "
        f"between {year_range[0]} and {year_range[1]}. "
        "Small samples can produce unstable win percentages."
    )
    results_chart = pd.DataFrame({
        "Outcome": ["Wins", "Draws", "Losses"],
        "Matches": [wins, draws, losses]
    }).set_index("Outcome")

    st.subheader("Match outcomes")

    if total_matches > 0:
        st.bar_chart(results_chart)
    else:
        st.info("No matches available for this selection.")
    st.dataframe(
        filtered_df,
        hide_index=True,
        use_container_width=True
    )



st.header("Shot Advantage and Winning")
st.caption(
    "All teams in the selected years. "
    "The team dropdown applies only to the team explorer above."
)

# Use the selected years, before filtering for a team.
shots_df = subset_df.loc[
    subset_df["year"].between(year_range[0], year_range[1])
].copy()

shots_df["shot_diff"] = (
    shots_df["hshots"] - shots_df["ashots"]
)

equal_shots = int((shots_df["shot_diff"] == 0).sum())
shots_df = shots_df.loc[shots_df["shot_diff"] != 0].copy()

shots_df["more_shots_team_won"] = (
    (
        (shots_df["shot_diff"] > 0)
        & (shots_df["hgoals"] > shots_df["agoals"])
    )
    | (
        (shots_df["shot_diff"] < 0)
        & (shots_df["agoals"] > shots_df["hgoals"])
    )
)

shots_df["shot_range"] = pd.cut(
    shots_df["shot_diff"].abs(),
    bins=[1, 5, 10, float("inf")],
    labels=["1–4", "5–9", "10+"],
    right=False
)

shot_summary = (
    shots_df.groupby("shot_range", observed=True)
    ["more_shots_team_won"]
    .agg(matches="count", win_rate="mean")
)

shot_summary["Win percentage"] = (
    shot_summary["win_rate"] * 100
)

if shots_df.empty:
    st.info("No unequal-shot matches available in these years.")
else:
    st.bar_chart(shot_summary[["Win percentage"]])

    st.dataframe(
        shot_summary[["matches", "Win percentage"]].round(1)
    )

st.caption(
    f"Shot advantage is the difference in total shots. "
    f"{equal_shots} equal-shot matches were excluded. "
    "Draws count as non-wins. These associations do not "
    "establish that taking more shots causes wins."
)

st.header("Possession Advantage and Winning")
st.caption(
    "All teams in the selected years. "
    "The team dropdown applies only to the team explorer above."
)

possession_df = subset_df.loc[
    subset_df["year"].between(year_range[0], year_range[1])
].copy()

possession_df["possession_diff"] = (
    possession_df["hPossesion"] - possession_df["aPossesion"]
)

equal_possession = int(
    (possession_df["possession_diff"] == 0).sum()
)

possession_df = possession_df.loc[
    possession_df["possession_diff"] != 0
].copy()

possession_df["more_possession_team_won"] = (
    (
        (possession_df["possession_diff"] > 0)
        & (possession_df["hgoals"] > possession_df["agoals"])
    )
    | (
        (possession_df["possession_diff"] < 0)
        & (possession_df["agoals"] > possession_df["hgoals"])
    )
)

possession_df["possession_range"] = pd.cut(
    possession_df["possession_diff"].abs(),
    bins=[0, 10, 20, float("inf")],
    labels=["Under 10", "10–under 20", "20+"],
    right=False
)

possession_summary = (
    possession_df.groupby("possession_range", observed=True)
    ["more_possession_team_won"]
    .agg(matches="count", win_rate="mean")
)

possession_summary["Win percentage"] = (
    possession_summary["win_rate"] * 100
)

if possession_df.empty:
    st.info("No unequal-possession matches available in these years.")
else:
    st.bar_chart(possession_summary[["Win percentage"]])

    st.dataframe(
        possession_summary[["matches", "Win percentage"]].round(1)
    )

st.caption(
    "Possession advantage is measured in percentage points: "
    "60% versus 40% gives a 20-point advantage. "
    f"{equal_possession} equal-possession matches were excluded. "
    "Draws count as non-wins. The results describe associations, "
    "not causal effects."
)

st.header("Fouls and Winning")
st.caption(
    "All teams in the selected years. "
    "The team dropdown applies only to the team explorer above."
)

side = st.selectbox(
    "Which side should the foul analysis use?",
    ["Home", "Away"]
)

fouls_df = subset_df.loc[
    subset_df["year"].between(year_range[0], year_range[1])
].copy()

if side == "Home":
    foul_column = "hfouls"
    fouls_df["won"] = (
        fouls_df["hgoals"] > fouls_df["agoals"]
    )
else:
    foul_column = "afouls"
    fouls_df["won"] = (
        fouls_df["agoals"] > fouls_df["hgoals"]
    )

fouls_df["foul_range"] = pd.cut(
    fouls_df[foul_column],
    bins=[0, 8, 12, 16, 20, float("inf")],
    labels=["0–7", "8–11", "12–15", "16–19", "20+"],
    right=False
)

foul_summary = (
    fouls_df.groupby("foul_range", observed=True)["won"]
    .agg(matches="count", win_rate="mean")
)

foul_summary["Win percentage"] = (
    foul_summary["win_rate"] * 100
)

if foul_summary.empty:
    st.info("No foul data available for this selection.")
else:
    st.bar_chart(foul_summary[["Win percentage"]])

    st.dataframe(
        foul_summary[["matches", "Win percentage"]].round(1)
    )

st.caption(
    "Draws count as non-wins. Win percentages account for "
    "different numbers of matches in each foul range. "
    "These results do not establish an ideal number of fouls "
    "or show that reducing fouls causes more wins."
)


st.header("Model Comparison")

st.write(
    "Can possession difference add useful information "
    "beyond shots-on-target difference?"
)

model_results = pd.DataFrame({
    "Model": [
        "Majority-class baseline",
        "Home-team shots on target, possession, and fouls",
        "Shots-on-target difference",
        "Shots-on-target + possession differences"
    ],
    "Test accuracy (%)": [53.5, 77.3, 80.1, 81.6],
    "Log loss": [None, None, 0.427, 0.423]
})

st.dataframe(
    model_results,
    hide_index=True,
    use_container_width=True
)

st.write(
    "Adding possession difference increased accuracy from "
    "80.1% to 81.6% and reduced log loss from 0.427 to 0.423. "
    "This was a small improvement on this test set; "
    "its reliability has not been established."
)

with st.expander("How were the models evaluated?"):
    st.markdown("""
- **Training:** 845 matches from 2004–2016.
- **Testing:** 282 matches from 2019–2021.
- **Target:** Home win versus home non-win.
- **Home non-win:** Draw or away win.
- **Baseline:** Always predicts home non-win.
- **Accuracy:** Percentage of correctly classified matches.
- **Log loss:** Evaluates predicted probabilities; lower is better.
- **Missing log-loss entries:** Not reported in the notebook.
""")

st.caption(
    "Fixed results from the notebook; year and team filters "
    "do not change this table. All models use completed-match "
    "statistics and do not forecast outcomes before kickoff."
)



st.header("What I Learned")

st.markdown("""
- **Data quality matters:** An explicit possession-validity
  rule retained 1,127 of the original 1,397 matches.

- **Counts and rates answer different questions:** Comparing
  win percentages instead of total wins changed my original
  conclusion about an ideal foul range.

- **Analysis definitions matter:** I corrected bin boundaries
  and handled equal-shot and equal-possession matches explicitly.

- **Models need comparisons:** I evaluated models on later-year
  matches against a majority-class baseline.

- **More inputs do not guarantee large improvements:** Adding
  possession to shots-on-target difference produced only a
  small improvement on the test set.
""")

with st.expander("Data source and limitations"):
    st.markdown("""
**Data source:** [UEFA Euro Stats on Kaggle](https://www.kaggle.com/datasets/kaito510/uefa-euro-stats-possession-shots-on-goal-etc)

- Findings describe associations, not causal effects.
- Listed home teams may not be playing in their own country.
- Competition coverage and other missing statistics require checking.
- Excluding invalid possession records may affect representativeness.
- Recorded goal totals determine outcomes; penalty-shootout
  conventions require verification.
- Model probability calibration has not been evaluated.
""")