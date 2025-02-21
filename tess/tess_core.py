from .match_result import MatchResult
from .team import Team


class TESSCore:
    """
    Team-based Elo Scoring System (TESS)
    
    This class manages Elo rating updates for team-based games by computing 
    expected win probabilities and applying rating adjustments based on 
    match results.

    Attributes:
        _K (float): Rating adjustment factor that controls the impact of a match on ratings.
        _alpha (float): Weight factor determining how much individual rankings affect the rating change.
        _scale (int): Scaling factor for Elo calculations (typically 400).
    
    Methods:
        _compute_team_expected(team_rating, opp_team_rating): 
            Computes the expected probability of a team winning based on ratings.
        update_game(team_A, team_B, match_res): 
            Updates the ratings of all players in two teams after a match.
    """

    def __init__(
            self, 
            K: float = 32, 
            alpha: float = 0.7, 
            scale: int = 400
    ):
        """
        Initializes the TESS system with Elo rating parameters.

        Args:
            K (float, optional): Elo rating adjustment factor (default: 32).
            alpha (float, optional): Weight for team vs. individual performance in rating updates (default: 0.5).
            scale (int, optional): Scaling factor for Elo calculations (default: 400).
        """
        self._K = K  # Elo adjustment factor
        self._alpha = alpha  # Weighting factor for team vs. individual performance
        self._scale = scale  # Scaling factor for Elo calculations

    @property
    def K(
        self
    ) -> float:
        """
        Returns the Elo rating adjustment factor (K-value).
        """
        return self._K

    @property
    def alpha(
        self
    ) -> float:
        """
        Returns the weight factor (alpha) for team vs. individual performance.
        """
        return self._alpha

    @property
    def scale(
        self
    ) -> int:
        """
        Returns the scaling factor used in the Elo rating calculations.
        """
        return self._scale

    def _compute_team_expected(
            self, 
            team_rating: float, 
            opp_team_rating: float
    ) -> float:
        """
        Computes the expected probability of a team winning against an opponent 
        based on their average ratings.

        Args:
            team_rating (float): The average rating of the team.
            opp_team_rating (float): The average rating of the opposing team.

        Returns:
            float: Expected probability of the team winning.
        """
        return 1.0 / (1 + 10 ** ((opp_team_rating - team_rating) / self._scale))

    def update_game(
            self, 
            team_A: Team, 
            team_B: Team,
            match_res: MatchResult
    ) -> None:
        """
        Updates the Elo ratings of all players in team A and team B based on the match result.

        Args:
            team_A (Team): The first team participating in the match.
            team_B (Team): The second team participating in the match.
            match_res (MatchResult): An object containing match outcomes and individual rankings.

        This function follows these steps:
        1. Compute the average ratings of both teams.
        2. Compute each team's expected probability of winning.
        3. Update each player's rating based on the team result and individual rankings.
        """
        # Step 1: Compute average team ratings
        avg_A = team_A.avg_rating()
        avg_B = team_B.avg_rating()

        # Step 2: Compute expected win probabilities for each team
        E_team_A = self._compute_team_expected(team_rating=avg_A, opp_team_rating=avg_B)
        E_team_B = self._compute_team_expected(team_rating=avg_B, opp_team_rating=avg_A)

        # Step 3: Update player ratings in each team
        team_A.update_ratings(
            E_team=E_team_A, 
            team_outcome=match_res.team_A_outcome, 
            rankings=match_res.rankings_A,
            K=self._K, 
            alpha=self._alpha, 
            scale=self._scale
        )
        team_B.update_ratings(
            E_team=E_team_B, 
            team_outcome=match_res.team_B_outcome, 
            rankings=match_res.rankings_B,
            K=self._K, 
            alpha=self._alpha, 
            scale=self._scale
        )
