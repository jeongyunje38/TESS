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
# Define true skills for 8 agents.
# The higher the value, the better the true skill.
# Agents are ranked from 1 (best) to 8 (worst) in terms of true ability.
# -----------------------------------------------------------------------------
true_skills = {
    "A1": 8,
    "A2": 7,
    "A3": 6,
    "A4": 5,
    "A5": 4,
    "A6": 3,
    "A7": 2,
    "A8": 1
}

def assign_true_skills(
        agents: list, 
        true_skills_dict: dict
):
    """
    Assigns the true_skill attribute to each agent based on the provided dictionary.
    
    Args:
        agents (list): List of Agent objects.
        true_skills_dict (dict): Mapping from agent id to true skill value.
    """
    for agent in agents:
        # Attach true_skill as an attribute (even if Agent class doesn't explicitly define it)
        agent.true_skill = true_skills_dict[agent.id]

def compute_team_true_avg(
        agents: list
):
    """
    Computes the average true skill of a team.
    
    Args:
        agents (list): List of Agent objects with a true_skill attribute.
        
    Returns:
        float: The average true skill.
    """
    return sum(agent.true_skill for agent in agents) / len(agents)

def determine_match_outcome(
        team_A_agents: list, 
        team_B_agents: list, 
        d: float = 1.0
):
    """
    Determines the outcome of a match between two teams based on their true skills.
    
    Uses a logistic function to compute the probability of Team A winning:
        P(win) = 1 / (1 + 10^((opp_avg - team_avg) / d))
    
    Args:
        team_A_agents (list): List of Agent objects for Team A.
        team_B_agents (list): List of Agent objects for Team B.
        d (float): Scale parameter for the logistic function.
        
    Returns:
        MatchOutcome: Outcome for Team A (WIN or LOSS).
    """
    avg_A = compute_team_true_avg(team_A_agents)
    avg_B = compute_team_true_avg(team_B_agents)

    # Compute win probability using a logistic formula
    p_win = 1.0 / (1 + 10 ** ((avg_B - avg_A) / d))

    return MatchOutcome.WIN if random.random() < p_win else MatchOutcome.LOSS

def assign_individual_rankings(
        agents: list
):
    """
    Assigns in-team rankings based on the agents' true skills.
    
    Agents with higher true_skill get better (lower number) ranks.
    
    Args:
        agents (list): List of Agent objects.
        
    Returns:
        dict: Mapping from agent id to their ranking (1 is best).
    """
    # Sort agents in descending order of true_skill (best first)
    sorted_agents = sorted(agents, key=lambda a: a.true_skill, reverse=True)

    # Assign rank: 1 for best, 2 for second, etc.
    return {agent.id: rank for rank, agent in enumerate(sorted_agents, start=1)}

def simulate_matches(
        num_matches: int = 1000, 
        d: float = 1.0
):
    """
    Simulates a series of matches between two teams formed by random partitioning 
    of 8 agents, and updates Elo ratings using the TESS system.
    
    Each match:
      - Randomly partitions 8 agents into Team A (4 agents) and Team B (4 agents).
      - Determines match outcome based on the teams' average true skills.
      - Assigns individual rankings within each team based on true skills.
      - Updates Elo ratings using the TESS update_game method.
    
    Args:
        num_matches (int): Number of matches to simulate (default is 1000).
        d (float): Scale parameter for logistic win probability.
    """
    # Create 8 agents with initial Elo ratings (default 1500)
    agent_ids = list(true_skills.keys())
    agents = [Agent(agent_id) for agent_id in agent_ids]

    # Assign true skill values to agents
    assign_true_skills(agents, true_skills)

    # Initialize the TESS system with default parameters (K=32, alpha=0.5, scale=400)
    tess = TESSCore()

    # Run the simulation for the specified number of matches
    for match in range(num_matches):
        # Randomly shuffle agents and split into two teams of 4
        random.shuffle(agents)
        team_A_agents = agents[:4]
        team_B_agents = agents[4:]

        # Determine match outcome based on true skills
        team_A_outcome = determine_match_outcome(team_A_agents, team_B_agents, d)

        # Assign individual rankings within each team (lower rank = better performance)
        rankings_A = assign_individual_rankings(team_A_agents)
        rankings_B = assign_individual_rankings(team_B_agents)

        # Create Team instances for TESS update
        team_A = Team(team_A_agents)
        team_B = Team(team_B_agents)

        # Create a MatchResult instance with the outcome and rankings
        match_result = MatchResult(team_A_outcome, rankings_A, rankings_B)

        # Update Elo ratings for both teams based on the match result
        tess.update_game(team_A, team_B, match_result)
    
    # After all matches, print the final Elo ratings for each agent.
    print("Final Elo ratings after", num_matches, "matches:")
    # Sort agents by Elo rating in descending order
    agents_sorted_by_elo = sorted(agents, key=lambda a: a.rating, reverse=True)
    for agent in agents_sorted_by_elo:
        print(f"Agent {agent.id} (True Skill: {agent.true_skill}) - Elo: {agent.rating:.2f}")

if __name__ == "__main__":
    # Simulate 1000 matches and observe the final Elo ratings.
    simulate_matches(num_matches=1000, d=1.0)
