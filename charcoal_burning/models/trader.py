import random

class Trader:
    def __init__(self):
        self.available = False
        self.last_visit_day = 0
        self.VISIT_INTERVAL = 3
        self.personalities = ["grumpy", "cheerful", "mysterious", "talkative", "hurried"]
        self.current_personality = None
        
    def check_arrival(self, current_day):
        if not self.available and current_day >= self.last_visit_day + self.VISIT_INTERVAL:
            self.available = True
            self.current_personality = random.choice(self.personalities)
            return True
        return False
    
    def trade_charcoal(self, resources, amount):
        if not self.available:
            return False, "No trader available"
            
        if amount > resources.resources["charcoal"]:
            return False, "Not enough charcoal"
            
        price = random.randint(2, 5)
        total = price * amount
        resources.resources["charcoal"] -= amount
        resources.resources["gold"] += total
        self.available = False
        self.last_visit_day = current_day
        return True, (amount, total, price)
