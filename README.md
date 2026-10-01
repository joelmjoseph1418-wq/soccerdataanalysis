# Soccer Match Statistics and Outcomes

An analysis of possession, shots, fouls, and match outcomes using Python and logistic regression.

## Dataset

[UEFA Euro Stats — Kaggle](https://www.kaggle.com/datasets/kaito510/uefa-euro-stats-possession-shots-on-goal-etc)

- **Original dataset:** 1,397 matches from 2002–2021
- **Cleaned dataset:** 1,127 matches
- **Cleaning rule:** Both teams must have positive possession values summing to 100%
- **Updated notebook:** [MStats_new.ipynb](MStats_new.ipynb)

## Key Findings

### Shots

Teams with larger shot advantages had higher observed win rates.

| Shot advantage | Matches | Win rate |
|---|---:|---:|
| 1–4 shots | 312 | 52.6% |
| 5–9 shots | 359 | 59.3% |
| 10+ shots | 414 | 77.3% |

The 42 equal-shot matches were excluded. Draws counted as non-wins.

### Possession

Teams with larger possession advantages had higher observed win rates.

| Possession advantage | Matches | Win rate |
|---|---:|---:|
| Under 10 percentage points | 287 | 44.3% |
| 10–under 20 percentage points | 272 | 57.4% |
| 20+ percentage points | 369 | 71.8% |

The 199 equal-possession matches were excluded. Draws counted as non-wins.

### Fouls

The lowest foul range had the highest observed win rate for both home and away teams.

| Fouls | Home win rate | Away win rate |
|---|---:|---:|
| 0–7 | 53.0% | 43.5% |
| 8–11 | 48.8% | 36.6% |
| 12–15 | 43.1% | 32.5% |
| 16–19 | 40.1% | 34.3% |
| 20+ | 31.9% | 25.8% |

These results do not support my original claim that 8–11 fouls was an ideal range.

**All findings describe associations, not causal effects.**

## Logistic Regression

The model classifies **home wins versus home non-wins** using:

- Home-team shots on target
- Home-team possession
- Home-team fouls

Draws and away wins count as home non-wins.

| Evaluation | Result |
|---|---:|
| Training matches, 2004–2016 | 845 |
| Testing matches, 2019–2021 | 282 |
| Model accuracy | 77.3% |
| Baseline accuracy | 53.5% |
| Home-win precision | 81% |
| Home-win recall | 66% |

The baseline always predicts home non-win, the most common training outcome.

**The model uses completed-match statistics. It does not predict outcomes before kickoff.**

## What I Learned

My original foul analysis counted total wins within each range. This was misleading because the ranges contained different numbers of matches. Calculating win percentages changed my conclusion.

I also replaced an arbitrary row cutoff with an explicit cleaning rule and tested the model on later-year matches.

## How to Run

1. Download or clone this repository.
2. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Keep `EuroAllMatchBoxData.csv` in the same folder as the notebook.
4. Open the updated notebook:

   ```bash
   jupyter notebook MStats_new.ipynb
   ```

5. Restart the kernel and run all cells.

## Limitations

- Listed home teams may not be playing in their own country, so the analysis does not establish home-field advantage.
- Competition stages and match coverage require verification.
- Excluding missing possession records may affect how representative the sample is.
- Other statistics may contain missing values requiring further checks.
- Team strength and match circumstances may influence the observed associations.
- Extra-time and penalty-shootout conventions require verification.
- Model probability calibration has not been evaluated.

## Tools

Python · pandas · NumPy · Matplotlib · scikit-learn
