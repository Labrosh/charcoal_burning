"""
ASCII art collection.
Responsibilities:
- Store all ASCII art
- Provide methods to display art
- Handle art formatting and centering
"""

class AsciiArt:
    ART = {
        "chop": r"""
           ___
          /   \
         |  o o|
         |   ^  |   CHOP! CHOP!
         |  --- |
         \_____/
        """,
        # ...Add other existing ascii_art entries...
    }
    
    @staticmethod
    def show(key):
        """Display ASCII art for the given key"""
        art = AsciiArt.ART.get(key)
        if art:
            print(art)
        else:
            print("No art available for this action.")
