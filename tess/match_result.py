from .match_outcome import MatchOutcome


class MatchResult:
    """
    Represents the outcome of a match between two teams, including their rankings.
    
    Attributes:
        _team_A_outcome (MatchOutcome): The outcome of team A (WIN, DRAW, LOSS).
        _team_B_outcome (MatchOutcome): The outcome of team B, determined automatically from team A's outcome.
        _rankings_A (dict): A dictionary mapping agent IDs to their rankings in team A.
        _rankings_B (dict): A dictionary mapping agent IDs to their rankings in team B.
    
    Methods:
        team_A_outcome (property): Returns the match outcome for team A.
        team_B_outcome (property): Returns the match outcome for team B.
        rankings_A (property): Returns the rankings of players in team A.
        rankings_B (property): Returns the rankings of players in team B.
    """

    def __init__(
            self, 
            team_A_outcome: MatchOutcome, 
            rankings_A: dict, 
            rankings_B: dict
    ):
        """
        Initializes a MatchResult instance with the outcomes and player rankings.

        Args:
            team_A_outcome (MatchOutcome): The outcome of team A.
            rankings_A (dict): A dictionary mapping agent IDs to rankings in team A (1 is highest).
            rankings_B (dict): A dictionary mapping agent IDs to rankings in team B (1 is highest).
        """
        self._team_A_outcome = team_A_outcome
        self._rankings_A = rankings_A
        self._rankings_B = rankings_B

        # Automatically determine team B's outcome based on team A's outcome
        if self._team_A_outcome == MatchOutcome.WIN:
            self._team_B_outcome = MatchOutcome.LOSS

        elif self._team_A_outcome == MatchOutcome.LOSS:
            self._team_B_outcome = MatchOutcome.WIN

        else:
            self._team_B_outcome = MatchOutcome.DRAW

    @property
    def team_A_outcome(
        self
    ) -> MatchOutcome:
        """
        Returns the outcome of team A.
        """
        return self._team_A_outcome

    @property
    def team_B_outcome(
        self
    ) -> MatchOutcome:
        """
        Returns the outcome of team B.
        """
        return self._team_B_outcome

    @property
    def rankings_A(
        self
    ) -> dict:
        """
        Returns the rankings of players in team A.
        """
        return self._rankings_A

    @property
    def rankings_B(
        self
    ) -> dict:
        """
        Returns the rankings of players in team B.
        """
        return self._rankings_B
