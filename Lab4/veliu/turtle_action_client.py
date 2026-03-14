from rclpy.parameter import Parameter
from rcl_interfaces.msg import ParameterDescriptor
from turtlesim.srv import SetColor
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rcl_interfaces.msg import ParameterDescriptor
from turtle_interfaces.action import MakeSquare  # Ensure this matches your interface name

class TurtleActionClient(Node):
    def __init__(self):
	super().__init__('turtle_action_client')
        # declare the parameter with a default value of 'blue'
	color_desc = ParameterDescriptor(description='the starting color of the turtle.')
	self.declare_parameter('turtleColor', 'blue', ParameterDescriptor(description='blue'))
        
	turtle_color = self.get_parameter('turtleColor').get_parameter_value().string_value
	self.turtle_display.color(turtle_color)
        
	self.color_cli = self.create_client(SetColor, '/turtle1/set_pen')
	while not self.color_cli.wait_for_service(timeout_sec=1.0):
	    self.get_logger().info('Color service not available, waiting...')

	self.color_req = SetColor.Request()
	self.color_req.color = turtleColor
	self.server_call = True
	self.service_future = self.color_cli.call_async(self.color_req)

	self.color_req.width = pen_width
        
        # Pre-Lab 4: Declare the square_size parameter
        square_desc = ParameterDescriptor(description='Side length of the square.')
        self.declare_parameter('square_size', 100.0, square_desc)
        self.declare_parameter('wait_time', 1.0, ParameterDescriptor(description='Time between prints (sec)'))
        
        self._action_client = ActionClient(self, MakeSquare, 'make_square')

    def send_goal(self):
        # Pre-Lab 4: Get values from parameters
        size = self.get_parameter('square_size').get_parameter_value().double_value
        wait_val = self.get_parameter('wait_time').get_parameter_value().double_value

        goal_msg = MakeSquare.Goal()
        goal_msg.square_size = size

        # Log both values so you have evidence for your deliverable
        self.get_logger().info(f'Sending goal with size: {size} and wait_time: {wait_val}')
        
        self._action_client.wait_for_server()

        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Feedback: {feedback_msg.feedback.pose}')

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.final_pose}')

def main(args=None):
    rclpy.init(args=args)
    action_client = TurtleActionClient()
    action_client.send_goal()
    rclpy.spin(action_client)

if __name__ == '__main__':
    main()
