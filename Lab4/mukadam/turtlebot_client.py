import math
import tkinter as tk
import turtle

import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor

from turtle_interfaces.msg import TurtleMsg
from turtle_interfaces.srv import SetColor


def rpy_from_quat(x, y, z, w):
    roll = math.atan2(2.0 * (w * x + y * z), 1.0 - 2.0 * (x * x + y * y))
    pitch = math.asin(2.0 * (w * y - z * x))
    yaw = math.atan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))
    return roll, pitch, yaw


class TurtleClient(Node):

    def __init__(self):
        super().__init__('turtlebot_client')

        #declare the turtle color parameter with a default value
        self.declare_parameter(
            'turtleColor',
            'blue',
            ParameterDescriptor(description='Initial turtle color')
        )

        #declare the pen size parameter with a default value
        self.declare_parameter(
            'penSize',
            3,
            ParameterDescriptor(description='Initial pen size')
        )

        #read the parameter values
        self.turtle_color = self.get_parameter('turtleColor').value
        self.pen_size = self.get_parameter('penSize').value

        #store the most recent turtle message from the server
        self.turtle = TurtleMsg()

        #track whether the service call is still active
        self.server_call = False

        #subscribe to the turtle state topic
        self.sub = self.create_subscription(
            TurtleMsg,
            'turtleState',
            self.turtle_callback,
            10
        )

        #create the color service client
        self.color_cli = self.create_client(SetColor, 'set_color')

        #wait until the set_color service is available
        while not self.color_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('color service not available, waiting...')

        #build the request using the startup color parameter
        self.color_req = SetColor.Request()
        self.color_req.color = self.turtle_color

        #call the service once so the server uses the chosen color
        self.server_call = True
        self.service_future = self.color_cli.call_async(self.color_req)

        #create the tkinter window
        self.root = tk.Tk()
        self.root.title('Turtle Client')

        #create the drawing canvas
        self.canvas = tk.Canvas(self.root, width=600, height=600)
        self.canvas.pack()

        #set up the turtle graphics screen
        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.bgcolor('white')
        self.screen.setworldcoordinates(-5, -5, 5, 5)

        #create the turtle display object
        self.turtle_display = turtle.RawTurtle(self.screen)
        self.turtle_display.shape('turtle')
        self.turtle_display.color(self.turtle_color)
        self.turtle_display.pensize(self.pen_size)
        self.turtle_display.speed(0)

        #update the display periodically
        self.timer = self.create_timer(0.05, self.update)

    def turtle_callback(self, msg):
        #save the newest turtle state from the server
        self.turtle = msg

    def update(self):
        #lift the pen when the color is None
        if self.turtle.color == 'None':
            self.turtle_display.penup()
        else:
            #use the current turtle color and pen size for drawing
            self.turtle_display.pencolor(self.turtle.color)
            self.turtle_display.pensize(self.pen_size)
            self.turtle_display.pendown()

        #move the turtle to the new position
        self.turtle_display.setpos(
            self.turtle.turtle_pose.position.x,
            self.turtle.turtle_pose.position.y
        )

        #convert quaternion orientation to yaw angle
        roll, pitch, yaw = rpy_from_quat(
            self.turtle.turtle_pose.orientation.x,
            self.turtle.turtle_pose.orientation.y,
            self.turtle.turtle_pose.orientation.z,
            self.turtle.turtle_pose.orientation.w
        )

        #rotate the turtle display to match heading
        self.turtle_display.seth(math.degrees(yaw))

        #mark the startup service call as complete once it finishes
        if self.server_call and self.service_future.done():
            self.server_call = False

        #refresh the tkinter window
        self.root.update_idletasks()
        self.root.update()


def main(args=None):
    rclpy.init(args=args)
    node = TurtleClient()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
