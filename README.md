# TESS: Team-based Elo Scoring System

TESS is a Python library designed for managing Elo ratings in team-based games. It extends the classic Elo rating system to handle not only team outcomes but also individual performance within teams, ensuring a zero-sum update over time.

## Overview

The traditional Elo system is zero-sum: any points gained by a winner are exactly lost by the loser. However, when applying Elo to team games—especially those that incorporate individual performance rankings—this balance can be lost, causing ratings to drift upward (or downward) over repeated matches.

TESS addresses this by splitting the rating update into two components:
1. **Team Component:** Reflects the overall team outcome.
2. **Individual Component:** Reflects the player's in-team ranking performance.

The individual component is adjusted to be zero-sum across the team, ensuring that the total points exchanged in a match match the team-based component.

## The Modified Elo Update Formula

TESS updates each agent's rating (\( \Delta R_i \)) by combining:

### 1. Team Component
Each agent receives an equal share of the team's outcome update:
\[
\text{team\_delta} = \frac{K \cdot \alpha \cdot (\text{outcome\_value} - E_{\text{team}})}{n}
\]
- **\(K\):** Elo adjustment factor.
- **\(\alpha\):** Weight for team performance.
- **\(\text{outcome\_value}\):** 1.0 (win), 0.5 (draw), or 0.0 (loss).
- **\(E_{\text{team}}\):** Expected team win probability.
- **\(n\):** Number of agents in the team.

### 2. Individual Component
For each agent \( i \):
- **Preliminary individual update:**
  \[
  \delta_i^{\text{indiv}} = K \cdot (1-\alpha) \cdot (S_i - E_i)
  \]
  - **\(S_i\):** Actual performance score based on in-team ranking (normalized so that best = 1, worst = 0).
  - **\(E_i\):** Expected performance score calculated via pairwise comparisons with teammates.
- **Zero-sum Adjustment:**
  Compute the average individual update:
  \[
  \overline{\delta^{\text{indiv}}} = \frac{1}{n}\sum_{i=1}^{n} \delta_i^{\text{indiv}}
  \]
  Adjust each individual delta:
  \[
  \delta_i^{\text{final, indiv}} = \delta_i^{\text{indiv}} - \overline{\delta^{\text{indiv}}}
  \]

### Final Update
Each agent's rating is updated by:
\[
\Delta R_i = \text{team\_delta} + \delta_i^{\text{final, indiv}}
\]
This ensures the total update is zero-sum across the team.

## Installation

To install TESS, clone the repository and install using pip:

```bash
git clone <repository-url>
cd TESS
pip install .
