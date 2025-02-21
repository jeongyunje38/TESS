from enum import Enum


class MatchOutcome(Enum):
    """
    Enum representing possible match outcomes in a team-based Elo system.
    
    Attributes:
        WIN (float): Represents a win with a value of 1.0.
        DRAW (float): Represents a draw with a value of 0.5.
        LOSS (float): Represents a loss with a value of 0.0.
    """
    WIN = 1.0  # Winning team gets a score of 1.0
    DRAW = 0.5  # Both teams receive 0.5 in case of a draw
    LOSS = 0.0  # Losing team gets a score of 0.0
