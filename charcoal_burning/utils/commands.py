
class CommandSystem:
    def __init__(self, game):
        self.game = game
        self.commands = {
            "chop": {
                "function": self.game.chop_wood,
                "description": "Gather wood from nearby trees.",
                "showInHelp": True
            },
            # ...Add other existing commands...
        }
    
    def execute(self, command):
        """Execute a command if it exists"""
        if command in self.commands:
            self.commands[command]["function"]()
            return True
        return False
    
    def show_help(self):
        """Display available commands"""
        print("\nHere are the available commands:\n")
        for cmd, details in self.commands.items():
            if details.get("showInHelp", False):
                print(f"  {cmd}: {details['description']}")
