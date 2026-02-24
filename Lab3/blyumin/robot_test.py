class Robot:
    def __init__(self, id_number, location):
        # Attributes
        self.id_number = id_number
        self.status = True  # Boolean flag: True for online, False for offline
        self.location = location  # String like 'A3'

    def moveBot(self, new_location):
        """Changes the location of the bot."""
        self.location = new_location
        print(f"Robot {self.id_number} moved to {self.location}.")

    def changeStatus(self):
        """Toggles the online/offline status."""
        self.status = not self.status
        state = "online" if self.status else "offline"
        print(f"Robot {self.id_number} is now {state}.")

    def __str__(self):
        """Provides a readable summary of the robot's current state."""
        state = "online" if self.status else "offline"
        return f"[Robot ID: {self.id_number}] | Status: {state} | Location: {self.location}"

# Verification Script
if __name__ == "__main__":
    # Create a robot instance
    my_bot = Robot(id_number=1234, location="A1")
    
    print("--- Initial State ---")
    print(my_bot)
    
    print("\n--- Testing Methods ---")
    my_bot.moveBot("B2")
    my_bot.changeStatus() # Toggle to offline
    
    print("\n--- Final Verification ---")
    print(my_bot)
