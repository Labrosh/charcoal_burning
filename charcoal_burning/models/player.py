"""
Player class.
Responsibilities:
- Track player equipment (axe upgrades)
- Handle player actions (chopping, building, etc)
- Track player progress and achievements
"""

class Player:
    def __init__(self, game):
        self.game = game
        self.has_better_axe = False
        self.seen_trader_message = False
        self.declined_retirement = False
    
    def chop_wood(self):
        """Handle wood chopping action"""
        wood_options = self.game.config.BETTER_AXE_OPTIONS if self.has_better_axe else self.game.config.WOOD_OPTIONS
        return random.choice(wood_options)
    
    def can_retire(self):
        """Check if player can retire"""
        return self.game.resources.gold >= self.game.config.GOLD_GOAL
