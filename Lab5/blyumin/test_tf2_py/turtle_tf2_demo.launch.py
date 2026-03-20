from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='turtlesim', executable='turtlesim_node', name='sim'),
        Node(package='test_tf2_py', executable='broadcaster', name='bc1', parameters=[{'turtlename': 'turtle1'}]),
        Node(package='test_tf2_py', executable='broadcaster', name='bc2', parameters=[{'turtlename': 'turtle2'}]),
        Node(package='test_tf2_py', executable='listener', name='listener', parameters=[{'target_frame': 'turtle2'}]),
    ])
