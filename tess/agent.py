class Agent:
    """
    Represents an individual player (agent) in the Elo rating system.
    
    Attributes:
        _id (str): A unique identifier for the agent.
        _rating (float): The current Elo rating of the agent (default: 1500).
    
    Methods:
        id (property): Returns the agent's unique identifier.
        rating (property): Returns the agent's current Elo rating.
        update_rating(delta: float): Adjusts the agent's rating by the given delta value.
        __repr__(): Returns a string representation of the agent.
    """

    def __init__(
            self, 
            id: str, 
            init_rating: float = 1500
    ):
        """
        Initializes an Agent with a unique identifier and an initial rating.
        
        Args:
            id (str): Unique identifier for the agent.
            init_rating (float, optional): Initial Elo rating (default: 1500).
        """
        self._id = id  # Unique agent ID
        self._rating = init_rating  # Initial Elo rating

    @property
    def id(
        self
    ) -> str:
        """
        Returns the agent's unique identifier.
        """
        return self._id

    @property
    def rating(
        self
    ) -> float:
        """
        Returns the agent's current Elo rating.
        """
        return self._rating

    def update_rating(
            self, 
            delta: float
    ) -> None:
        """
        Updates the agent's rating by applying the given delta.
        
        Args:
            delta (float): The amount by which to adjust the agent's rating.
        """
        self._rating += delta  # Adjust rating by the specified delta

    def __repr__(
            self
    ) -> str:
        """
        Returns a string representation of the agent.
        """
        return f"{self._id}: {self._rating:.2f}"  # Display agent ID and rating with two decimal places
