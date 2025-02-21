import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from tess.agent import Agent
from tess.match_result import MatchResult
from tess.match_outcome import MatchOutcome
from tess.team import Team
from tess.tess_core import TESSCore


# --- Example Usage ---
if __name__ == "__main__":
    """
    This script demonstrates how to use the TESS (Team-based Elo Scoring System)
    by simulating a match between two teams, updating their ratings, and printing the results.
    """

    # Step 1: Create agents (players) for Team A and Team B
    agents_A = [Agent("A1"), Agent("A2"), Agent("A3")]
    agents_B = [Agent("B1"), Agent("B2"), Agent("B3")]

    # Step 2: Initialize teams with their respective agents
    team_A = Team(agents=agents_A)
    team_B = Team(agents=agents_B)

    # Step 3: Define player rankings within each team (1 is the highest rank)
    rankings_A = {"A1": 1, "A2": 2, "A3": 3}  # Team A rankings
    rankings_B = {"B1": 1, "B2": 2, "B3": 3}  # Team B rankings

    # Step 4: Simulate a match where Team A wins
    match_res = MatchResult(
        team_A_outcome=MatchOutcome.WIN, 
        rankings_A=rankings_A, 
        rankings_B=rankings_B
    )

    # Step 5: Create the TESS system instance
    tess = TESSCore()

    # Step 6: Update team ratings based on the match result
    tess.update_game(
        team_A=team_A, 
        team_B=team_B, 
        match_res=match_res
    )

    # Step 7: Print updated ratings for Team A
    print("Updated ratings for Team A:")
    for agent in team_A.agents:
        print(agent)

    # Step 8: Print updated ratings for Team B
    print("\nUpdated ratings for Team B:")
    for agent in team_B.agents:
        print(agent)
