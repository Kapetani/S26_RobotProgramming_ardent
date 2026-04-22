import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    package_name = 'my_robot'

    # Set paths
    urdf = os.path.join(get_package_share_directory(package_name), 'urdf', 'my_robot.urdf.xacro')
    
    # Action 6a/b: Set use_sim_time to true by default
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # Xacro processing
    robot_desc = ParameterValue(Command(['xacro ', urdf]), value_type=str)

    # Robot State Publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_desc}]
    )

    # Action 6c/d: Include Gazebo Launch
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py'))
    )

    # Action 6d: Spawn Entity Node
    gazebo_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'my_robot']
    )

    # Rviz Node (keeping it for the Task 8 question)
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        parameters=[{'use_sim_time': use_sim_time}]
    )

    # Action 6e: Add to LaunchDescription
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        robot_state_publisher_node,
        gazebo_launch,
        gazebo_robot,
        rviz_node
    ])
