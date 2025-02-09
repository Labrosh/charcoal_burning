class ResourceManager:
    def __init__(self):
        self.resources = {
            "wood": 0,
            "charcoal": 0,
            "wood_limit": 10,
            "charcoal_limit": 5,
            "gold": 0,
            "gold_goal": 100
        }
    
    def add_wood(self, amount):
        space_left = self.resources["wood_limit"] - self.resources["wood"]
        added = min(amount, space_left)
        self.resources["wood"] += added
        return added, amount - added  # (added, wasted)
    
    def add_charcoal(self, amount):
        space_left = self.resources["charcoal_limit"] - self.resources["charcoal"]
        added = min(amount, space_left)
        self.resources["charcoal"] += added
        return added, amount - added  # (added, wasted)

    def upgrade_storage(self):
        cost = self.resources["wood_limit"]
        if self.resources["wood"] >= cost:
            self.resources["wood"] -= cost
            self.resources["wood_limit"] *= 2
            self.resources["charcoal_limit"] *= 2
            return True
        return False
