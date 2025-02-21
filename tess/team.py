from typing import List, Dict

from .agent import Agent
from .match_outcome import MatchOutcome


class Team:
    """
    Represents a team in the Elo rating system, managing agents (players) and their rating updates.

    Attributes:
        _agents (List[Agent]): A list of agents (players) in the team.
    
    Methods:
        agents (property): Returns the list of agents in the team.
        average_rating(): Computes the team's average Elo rating.
        _computE_indiv_expected(agent, scale): Computes the expected score for an individual within the team.
        update_ratings(E_team, team_outcome, rankings, K, alpha, scale): Updates the ratings of all team members.
    """

    def __init__(
            self, 
            agents: List[Agent]
    ):
        """
        Initializes a Team with a list of agents (players).

        Args:
            agents (List[Agent]): List of Agent objects representing the team members.
        """
        self._agents = agents  # List of agents in the team

    @property
    def agents(
        self
    ) -> List[Agent]:
        """
        Returns the list of agents (players) in the team.
        """
        return self._agents

    def _computE_indiv_expected(
            self, 
            agent: Agent, 
            scale: int
    ) -> float:
        """
        Computes the expected score of an individual agent within the team using pairwise comparisons.

        Args:
            agent (Agent): The agent whose expected score is being calculated.
            scale (int): The Elo scale factor.

        Returns:
            float: The expected score of the agent within the team.
        """
        n = len(self.agents)
        total = 0.0

        for other in self.agents:
            if other.id == agent.id:
                continue  # Skip self-comparison

            # Compute expected probability of winning against another team member
            total += 1.0 / (1 + 10 ** ((other.rating - agent.rating) / scale))

        return total / (n - 1) if n > 1 else 0.0

    def avg_rating(
            self
    ) -> float:
        """
        Computes the average rating of the team.

        Returns:
            float: The average rating of all agents in the team.
        """
        if not self.agents:
            return 0.0  # Return 0 if the team has no players

        return sum(agent.rating for agent in self.agents) / len(self.agents)

    def update_ratings(
            self, 
            E_team: float, 
            team_outcome: MatchOutcome, 
            rankings: Dict[str, int],
            K: float, 
            alpha: float, 
            scale: int = 400
    ) -> None:
        """
        Updates the Elo ratings for all agents in the team, ensuring that the individual
        component is zero-sum.
        
        Args:
            E_team (float): The team's expected win probability.
            team_outcome (MatchOutcome): The actual outcome for the team.
            rankings (Dict[str, int]): Mapping from agent IDs to their in-team rankings (1 is best).
            K (float): The Elo rating adjustment factor.
            alpha (float): Weight given to team performance vs. individual performance.
            scale (int): The Elo scaling factor.
            
        Procedure:
            1. Compute a common team component (team_delta) distributed equally.
            2. Compute preliminary individual adjustments for each agent.
            3. Adjust the individual components to be zero-sum within the team.
            4. Update each agent's rating with the sum of the team component and adjusted individual component.
        """
        n = len(self.agents)
        outcome_value = team_outcome.value

        # If there's only one agent in the team, use a simplified update.
        if n < 2:
            for agent in self.agents:
                delta = K * (outcome_value - E_team)
                agent.update_rating(delta)

            return

        # Step 1: Compute the team component (distributed equally)
        team_delta = K * alpha * (outcome_value - E_team) / n

        # Step 2: Compute preliminary individual adjustments for each agent
        indiv_deltas = []
        for agent in self.agents:
            rank = rankings.get(agent.id)
            if rank is None:
                raise ValueError(f"Rank information missing for agent {agent.id}.")

            # S_indiv: actual performance based on ranking (normalized: best=1, worst=0)
            S_indiv = (n - rank) / (n - 1)
            # E_indiv: expected performance computed from pairwise comparisons
            E_indiv = self._computE_indiv_expected(agent, scale)
            indiv_delta = K * (1 - alpha) * (S_indiv - E_indiv)
            indiv_deltas.append(indiv_delta)

        # Step 3: Adjust individual deltas to be zero-sum
        avg_indiv_delta = sum(indiv_deltas) / n
        adjusted_indiv_deltas = [delta - avg_indiv_delta for delta in indiv_deltas]

        # Step 4: Update each agent's rating with the combined delta
        for i, agent in enumerate(self.agents):
            final_delta = team_delta + adjusted_indiv_deltas[i]
            agent.update_rating(final_delta)
