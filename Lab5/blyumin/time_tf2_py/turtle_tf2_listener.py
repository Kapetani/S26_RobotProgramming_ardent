import math
import rclpy
from rclpy.node import Node
from tf2_ros import TransformException, Buffer, TransformListener
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn

class FrameListener(Node):
    def __init__(self):
        super().__init__('turtle_tf2_listener')
        self.target_frame = self.declare_parameter('target_frame', 'turtle2').get_parameter_value().string_value
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.publisher = self.create_publisher(Twist, f'/{self.target_frame}/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.on_timer)

    def on_timer(self):
        try:
            # LOOKING 5 SECONDS INTO THE PAST
            when = self.get_clock().now() - rclpy.duration.Duration(seconds=5.0)
            trans = self.tf_buffer.lookup_transform(self.target_frame, 'turtle1', when, timeout=rclpy.duration.Duration(seconds=1.0))
        except TransformException:
            return

        msg = Twist()
        msg.angular.z = 4.0 * math.atan2(trans.transform.translation.y, trans.transform.translation.x)
        msg.linear.x = 0.5 * math.sqrt(trans.transform.translation.x**2 + trans.transform.translation.y**2)
        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = FrameListener()
    rclpy.spin(node)
    rclpy.shutdown()
