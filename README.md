# Soccer Match Statistics and Outcomes

A Python project exploring associations between possession, shots, fouls, and soccer match outcomes, with an interactive Streamlit dashboard.

**[Explore the Live Dashboard](https://soccerdataanalysis.streamlit.app/)**

![Soccer statistics dashboard](dashboard.png)

## Project Overview

This project uses an existing public dataset to explore soccer match statistics and evaluate logistic regression models.

Questions explored:

- How do a team's recorded results vary across selected years?
- How does shot advantage relate to winning?
- How does possession advantage relate to winning?
- How do win percentages differ across foul ranges?
- Does possession add information beyond shots on target?

The dashboard lets visitors filter matches by year and team, explore team results, and view statistical findings and model comparisons.

## Dataset

**Source:** [UEFA Euro Stats by kaito510 — Kaggle](https://www.kaggle.com/datasets/kaito510/uefa-euro-stats-possession-shots-on-goal-etc)

| Dataset | Matches |
|---|---:|
| Original records, 2002–2021 | 1,397 |
| Retained after possession validation | 1,127 |
| Excluded | 270 |

Matches were retained when both teams had positive possession values summing to 100%. Legitimate zero values, such as zero shots on target, were not automatically removed.

The data was obtained from Kaggle, not collected by me. Refer to the source for its license and usage terms.

## Key Findings

### Shot Advantage

Teams with larger shot advantages had higher observed win percentages.

| Extra shots over opponent | Matches | Win percentage |
|---|---:|---:|
| 1–4 | 312 | 52.6% |
| 5–9 | 359 | 59.3% |
| 10+ | 414 | 77.3% |

The 42 equal-shot matches were excluded. Draws counted as non-wins.

### Possession Advantage

Teams with larger possession advantages had higher observed win percentages.

| Possession advantage | Matches | Win percentage |
|---|---:|---:|
| Under 10 percentage points | 287 | 44.3% |
| 10–under 20 percentage points | 272 | 57.4% |
| 20+ percentage points | 369 | 71.8% |

The 199 equal-possession matches were excluded. Draws counted as non-wins.

An advantage of 20 percentage points means, for example, 60% possession versus 40%.

### Fouls

The 0–7 foul range had the highest observed win percentage for both listed home and away teams.

| Fouls | Home win percentage | Away win percentage |
|---|---:|---:|
| 0–7 | 53.0% | 43.5% |
| 8–11 | 48.8% | 36.6% |
| 12–15 | 43.1% | 32.5% |
| 16–19 | 40.1% | 34.3% |
| 20+ | 31.9% | 25.8% |

These results did not support my original claim that 8–11 fouls was an ideal range.

**These findings describe associations, not causal effects.**

## Model Comparison

Logistic regression models classify **home wins versus home non-wins**. Draws and away wins count as home non-wins.

All models use the same chronological split:

- **Training:** 845 matches from 2004–2016.
- **Testing:** 282 matches from 2019–2021.

| Model | Test accuracy | Test log loss |
|---|---:|---:|
| Majority-class baseline | 53.5% | Not reported |
| Home-team shots on target, possession, and fouls | 77.3% | Not reported |
| Shots-on-target difference | 80.1% | 0.427 |
| Shots-on-target difference + possession difference | 81.6% | 0.423 |

The baseline always predicts home non-win, the most common training outcome. Difference-based inputs subtract the away-team statistic from the home-team statistic.

Adding possession difference improved accuracy by approximately **1.5 percentage points** and reduced log loss by approximately **0.004**. This was a small improvement on this test set; its reliability has not been established.

Accuracy measures correct classifications. Log loss evaluates predicted probabilities, with lower values indicating better performance under that metric.

**The models use completed-match statistics. They do not forecast outcomes before kickoff.**

## What I Learned

### Data Cleaning

An arbitrary row cutoff did not remove all records with missing statistics. Replacing it with an explicit possession-validity rule made the cleaning process clearer and reproducible.

I learned that dataset size alone does not determine data quality, and that excluding records may affect how representative the remaining sample is.

### Analysis Definitions

My initial foul analysis compared total wins across ranges containing different numbers of matches. Switching to win percentages changed my conclusion.

I also corrected bin boundaries, included large shot differences, and handled equal-shot and equal-possession matches explicitly. These choices changed which matches contributed to each calculation.

### Statistical Findings

Larger shot and possession advantages were associated with higher win percentages. However, those patterns did not establish causation: team strength and match circumstances could influence both statistics and outcomes.

### Model Evaluation

I evaluated models on later-year matches and compared them with a simple baseline. Comparing shots alone with shots plus possession helped me ask whether an additional input contributed useful information.

I learned that accuracy and log loss assess different aspects of predictions, and that a small improvement should be described cautiously.

### Presenting Results

Building the Streamlit dashboard gave me practice turning notebook analysis into an interactive application. I added year and team filters, outcome summaries, charts, and explanations.

I learned to make sample counts, outcome definitions, and limitations visible alongside the results.

## Project Work

The work presented here includes:

- Applying and documenting a data-cleaning rule.
- Revising statistical comparisons and visualizations.
- Training and evaluating logistic regression models.
- Comparing model inputs.
- Building and deploying a Streamlit dashboard.
- Documenting findings and limitations.

The analysis uses an existing public dataset. The deployed app is a way to explore the results; no substantial user adoption is claimed.

## Project Structure

```text
soccerdataanalysis/
├── app.py
├── data/
│   └── EuroAllMatchBoxData.csv
├── MStats.ipynb
├── README.md
├── requirements.txt
└── dashboard.png
```

## Run Locally

### Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Run the dashboard

From the repository's main folder:

```bash
streamlit run app.py
```

### Run the notebook

Keep the CSV at `data/EuroAllMatchBoxData.csv`, then open:

```bash
jupyter notebook MStats.ipynb
```

Restart the kernel and run all cells. The notebook should load the dataset using:

```python
df = pd.read_csv("data/EuroAllMatchBoxData.csv")
```

## Limitations

- Listed home teams may not be playing in their own country, so outcome differences do not establish home-field advantage.
- Competition stages and match coverage require verification against the source.
- Excluding invalid possession records may affect representativeness.
- Other statistics may contain missing values requiring further checks.
- Team strength and match circumstances may influence observed associations.
- Recorded goal totals determine outcomes; extra-time and penalty-shootout conventions require verification.
- Model probabilities have not been evaluated for calibration.
- The test set was used for exploratory model comparisons, so final performance needs independent validation.

## Tools

Python · pandas · NumPy · Matplotlib · scikit-learn · Streamlit
