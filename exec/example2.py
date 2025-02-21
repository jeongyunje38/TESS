import os
import random
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from tess.agent import Agent
from tess.match_result import MatchResult
from tess.match_outcome import MatchOutcome
from tess.team import Team
from tess.tess_core import TESSCore


# -----------------------------------------------------------------------------
# Define discrete ranking probability distributions for each agent.
# The distribution is defined as a list of weights for ranks 1 through 5.
# For example, for agent A1 the weights [0.3, 0.25, 0.2, 0.15, 0.1] mean:
#   - 30% chance to get rank 1 (best)
#   - 25% chance to get rank 2
#   - 20% chance to get rank 3
#   - 15% chance to get rank 4
#   - 10% chance to get rank 5 (worst)
# -----------------------------------------------------------------------------
ranking_probs_A = {
    "A1": [0.3, 0.25, 0.2, 0.15, 0.1],
    "A2": [0.2, 0.3, 0.25, 0.15, 0.1],
    "A3": [0.25, 0.25, 0.2, 0.15, 0.15],
    "A4": [0.2, 0.2, 0.3, 0.2, 0.1],
    "A5": [0.15, 0.25, 0.3, 0.2, 0.1]
}

ranking_probs_B = {
    "B1": [0.3, 0.25, 0.2, 0.15, 0.1],
    "B2": [0.2, 0.3, 0.25, 0.15, 0.1],
    "B3": [0.25, 0.25, 0.2, 0.15, 0.15],
    "B4": [0.2, 0.2, 0.3, 0.2, 0.1],
    "B5": [0.15, 0.25, 0.3, 0.2, 0.1]
}

def sample_rank(
        agent_id: str, 
        ranking_probs: dict
) -> int:
    """
    Samples a ranking for an agent based on the agent's discrete probability distribution.
    
    Args:
        agent_id (str): The unique ID of the agent.
        ranking_probs (dict): A dictionary mapping agent IDs to a list of weights for ranks 1-5.
        
    Returns:
        int: A sampled rank (1 to 5, where 1 is the highest).
    """
    ranks = [1, 2, 3, 4, 5]
    weights = ranking_probs[agent_id]

    # random.choices returns a list; extract the first (and only) element.
    return random.choices(ranks, weights=weights, k=1)[0]

def simulate_games(
        num_games: int = 1000
) -> None:
    """
    Simulates a series of games between Team A and Team B and prints the final Elo ratings.
    
    Game Details:
      - Team A wins with a 60% probability.
      - Each team has 5 agents.
      - In each game, each agent's ranking is sampled from its defined discrete distribution.
      - The TESS system updates the ratings based on team outcome and individual rankings.
      
    Args:
        num_games (int): Number of games to simulate (default is 1000).
    """
    # Create agents for Team A and Team B
    agents_A = [Agent("A1"), Agent("A2"), Agent("A3"), Agent("A4"), Agent("A5")]
    agents_B = [Agent("B1"), Agent("B2"), Agent("B3"), Agent("B4"), Agent("B5")]

    # Initialize teams with the created agents
    team_A = Team(agents_A)
    team_B = Team(agents_B)

    # Initialize the TESS system with default parameters (K=32, alpha=0.5, scale=400)
    tess = TESSCore()

    # Repeat the simulation for the specified number of games
    for game in range(num_games):
        # Determine match outcome: Team A wins with 60% probability.
        if random.random() < 0.6:
            team_A_outcome = MatchOutcome.WIN
        else:
            team_A_outcome = MatchOutcome.LOSS

        # For each team, sample rankings for each agent based on their probability distributions.
        rankings_A = {agent.id: sample_rank(agent.id, ranking_probs_A) for agent in agents_A}
        rankings_B = {agent.id: sample_rank(agent.id, ranking_probs_B) for agent in agents_B}

        # Create a MatchResult instance for the current game.
        match_result = MatchResult(team_A_outcome, rankings_A, rankings_B)

        # Update the game ratings using the TESS system.
        tess.update_game(team_A, team_B, match_result)

    # After all games, print the final Elo ratings for each agent in Team A.
    print("Final Elo ratings for Team A:")
    for agent in team_A.agents:
        print(agent)

    # Print the final Elo ratings for each agent in Team B.
    print("\nFinal Elo ratings for Team B:")
    for agent in team_B.agents:
        print(agent)

if __name__ == "__main__":
    # Run the simulation with a specified number of games
    simulate_games(num_games=1000)
