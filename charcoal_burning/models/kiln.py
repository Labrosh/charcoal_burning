import random

class Kiln:
    def __init__(self):
        self.status = "unbuilt"
        self.burn_time = 0
        self.COST = 10
    
    def build(self, resources):
        if self.status != "unbuilt":
            return False, "Already have a kiln"
        
        if resources.resources["wood"] >= self.COST:
            resources.resources["wood"] -= self.COST
            self.status = "built - unlit"
            return True, f"Used {self.COST} wood to build a kiln"
        return False, "Not enough wood"
    
    def light(self):
        if self.status != "built - unlit":
            return False, "Kiln not ready to light"
            
        self.burn_time = random.randint(6, 10)
        self.status = "built - lit"
        return True, "Kiln lit successfully"
    
    def progress(self):
        if self.status == "built - lit":
            self.burn_time -= 1
            if self.burn_time <= 0:
                self.status = "charcoal ready"
                return True, "Charcoal is ready to collect"
        return False, ""
