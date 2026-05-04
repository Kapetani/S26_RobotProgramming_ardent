import os
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('my_robot')
    
    # Path to the XACRO file
    xacro_file = os.path.join(pkg_share, 'my_robot.urdf.xacro')
    rviz_config = os.path.join(pkg_share, 'my_robot.rviz')

    # Process XACRO into Robot Description
    robot_description_config = ParameterValue(Command(['xacro ', xacro_file]), value_type=str)
   
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py'))
    )

    gazebo_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'my_robot']
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description_config}]
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config]
        ),
        gazebo_launch,
        gazebo_robot
    ])
