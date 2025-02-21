"""
TESS (Team-based Elo Scoring System)
======================================

A Python library for managing Elo ratings in team-based games.
"""

__version__ = "0.1.0"

# Import key classes to expose them as part of the package API.
from .agent import Agent
from .match_outcome import MatchOutcome
from .match_result import MatchResult
from .team import Team
from .tess_core import TESSCore

# Optionally, define __all__ to specify the public API.
__all__ = [
    "Agent",
    "MatchOutcome",
    "MatchResult",
    "Team",
    "TESSCore",
]
