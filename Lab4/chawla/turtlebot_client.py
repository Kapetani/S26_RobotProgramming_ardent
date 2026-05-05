import math
import tkinter as tk
import turtle

import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor

from turtle_interfaces.msg import TurtleMsg
from turtle_interfaces.srv import SetColor


def get_yaw_from_quaternion(x, y, z, w):
    """Extracts only the yaw (Z-axis rotation) from a quaternion."""
    return math.atan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))


class RefactoredTurtleClient(Node):

    def __init__(self):
        super().__init__('turtlebot_client')
        
        # State storage
        self.latest_turtle_data = TurtleMsg()

        # Initialization sequence
        self._setup_parameters()
        self._setup_ros()
        self._setup_gui()

    def _setup_parameters(self):
        """Declares and retrieves ROS 2 parameters."""
        self.declare_parameters(
            namespace='',
            parameters=[
                ('turtleColor', 'blue', ParameterDescriptor(description='Initial turtle color')),
                ('penSize', 3, ParameterDescriptor(description='Initial pen size'))
            ]
        )
        
        # Extract values into class attributes
        self.config_color = self.get_parameter('turtleColor').get_parameter_value().string_value
        self.config_pen_size = self.get_parameter('penSize').get_parameter_value().integer_value

    def _setup_ros(self):
        """Configures ROS 2 publishers, subscribers, and services."""
        # Subscribe to turtle state
        self.state_sub = self.create_subscription(
            TurtleMsg, 
            'turtleState', 
            self._state_callback, 
            10
        )

        # Sync color with the server
        self.color_client = self.create_client(SetColor, 'set_color')
        self._sync_color()

    def _sync_color(self):
        """Waits for the color service and sends the initial color asynchronously."""
        while not self.color_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Color service not available, waiting...')

        request = SetColor.Request(color=self.config_color)
        future = self.color_client.call_async(request)
        
        # Attach a callback instead of polling in the update loop
        future.add_done_callback(self._on_color_sync_complete)

    def _on_color_sync_complete(self, future):
        """Callback triggered when the server successfully registers the color."""
        self.get_logger().info(f"Successfully synced color '{self.config_color}' with the server.")

    def _setup_gui(self):
        """Initializes Tkinter and the Turtle canvas."""
        self.tk_root = tk.Tk()
        self.tk_root.title('ROS 2 Turtle Client')

        self.canvas = tk.Canvas(self.tk_root, width=600, height=600)
        self.canvas.pack()

        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.bgcolor('white')
        self.screen.setworldcoordinates(-5, -5, 5, 5)

        self.bot_avatar = turtle.RawTurtle(self.screen)
        self.bot_avatar.shape('turtle')
        self.bot_avatar.color(self.config_color)
        self.bot_avatar.pensize(self.config_pen_size)
        self.bot_avatar.speed(0)

        # Timer to trigger GUI redraws at 20Hz
        self.render_timer = self.create_timer(0.05, self._render_loop)

    def _state_callback(self, msg: TurtleMsg):
        """Caches the latest message received from the server."""
        self.latest_turtle_data = msg

    def _render_loop(self):
        """Updates the turtle's visual state and refreshes the Tkinter window."""
        current_color = self.latest_turtle_data.color

        # Handle Pen State
        if current_color == 'None':
            self.bot_avatar.penup()
        else:
            self.bot_avatar.pencolor(current_color)
            self.bot_avatar.pensize(self.config_pen_size)
            self.bot_avatar.pendown()

        # Handle Position
        pos = self.latest_turtle_data.turtle_pose.position
        self.bot_avatar.setpos(pos.x, pos.y)

        # Handle Orientation
        quat = self.latest_turtle_data.turtle_pose.orientation
        yaw = get_yaw_from_quaternion(quat.x, quat.y, quat.z, quat.w)
        self.bot_avatar.setheading(math.degrees(yaw))

        # Push updates to the screen
        self.tk_root.update_idletasks()
        self.tk_root.update()


def main(args=None):
    rclpy.init(args=args)
    node = RefactoredTurtleClient()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Client shut down by user.")

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
