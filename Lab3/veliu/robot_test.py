class Robot:
    def __init__(self, id_number, location, is_online=True):
        """
        Initializes the Robot with an ID, location, and status.
        is_online is a boolean flag as recommended.
        """
        self.id_number = id_number
        self.is_online = is_online
        self.location = location

    def moveBot(self, new_location):
        """Changes the location of the bot."""
        self.location = new_location

    def changeStatus(self):
        """Toggles the online/offline status."""
        self.is_online = not self.is_online

    def __str__(self):
        """Provides a readable summary of the Robot's state."""
        status_text = "online" if self.is_online else "offline"
        return f"Robot {self.id_number} is {status_text} at location {self.location}."
      
#Verification Script  
# 1. Create a new instance of the Robot
my_robot = Robot(id_number=86, location="A3")
print("Initial state:")
print(my_robot)

# 2. Change the location using moveBot
my_robot.moveBot("B5")
print("\nAfter moving:")
print(my_robot)

# 3. Toggle the status using changeStatus
my_robot.changeStatus()
print("\nAfter changing status:")
print(my_robot)

# 4. Verify attribute access
print(f"\nDirect attribute check - ID: {my_robot.id_number}")
