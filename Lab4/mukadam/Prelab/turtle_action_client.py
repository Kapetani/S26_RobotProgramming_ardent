from action_msgs.msg import GoalStatus
from turtle_interfaces.action import MakeSquare

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from rclpy.parameter import Parameter
from rcl_interfaces.msg import ParameterDescriptor


class TurtleSquareClient(Node):

    def __init__(self):
        super().__init__('square_client')

        self.declare_parameter(
            'square_size',
            50.0,
            ParameterDescriptor(description='Size of square')
        )

        self._action_client = ActionClient(self, MakeSquare, 'make_square')


    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f"{feedback_msg.feedback.current_pose}")


    def get_result_callback(self, future):
        result = future.result().result
        status = future.result().status

        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info(f"{result.final_pose}")
        else:
            self.get_logger().info(f"{status}")

        rclpy.shutdown()


    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)


    def send_goal(self):
        self._action_client.wait_for_server()

        goal_msg = MakeSquare.Goal()
        goal_msg.square_size = self.get_parameter('square_size').value

        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        self._send_goal_future.add_done_callback(self.goal_response_callback)


def main(args=None):
    rclpy.init(args=args)

    node = TurtleSquareClient()
    node.send_goal()

    rclpy.spin(node)


if __name__ == '__main__':
    main()
