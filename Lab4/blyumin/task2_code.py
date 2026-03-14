import rclpy
import json
import os
import turtle
import math
from rclpy.node import Node

class TurtleClient(Node):
    def __init__(self):
        super().__init__('turtlebot_client')
        
        # --- Step 14: Parameter Declaration ---
        # Declaring parameters allows us to change turtle attributes from the command line
        self.declare_parameter('turtleColor', 'green')
        self.declare_parameter('penSize', 10)
        
        # Initialize the Python Turtle Graphics window
        self.t = turtle.Turtle()
        self.t.shape("turtle")
        self.t.speed(0) # Set to fastest animation speed
        
        # Fetch parameter values and apply them to the turtle
        color = self.get_parameter('turtleColor').value
        size = self.get_parameter('penSize').value
        self.t.color(color)
        self.t.pensize(size)
        
        # --- Synchronization Timer ---
        # We check the shared state file every 0.1 seconds to bypass VM networking issues
        self.create_timer(0.1, self.update_visuals)
        self.get_logger().info(f"TurtleClient started with color: {color} and size: {size}")

    def update_visuals(self):
        """Reads the state from the server and updates the turtle's position/heading."""
        state_path = '/tmp/turtle_state.json'
        
        if os.path.exists(state_path):
            try:
                with open(state_path, 'r') as f:
                    data = json.load(f)
                
                # ROS 2 server calculates in Radians; Python Turtle uses Degrees
                # We convert here to ensure the turtle points the right way
                current_degrees = math.degrees(data['theta'])
                self.t.setheading(current_degrees)
                
                # Update position (scaled for visibility in the turtle window)
                self.t.goto(data['x'] * 10, data['y'] * 10)
                
                # Ensure the pen is down to draw the path
                self.t.pendown()
            except (json.JSONDecodeError, IOError):
                # Handle cases where the file is being written to while we try to read it
                pass

def main(args=None):
    rclpy.init(args=args)
    node = TurtleClient()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
