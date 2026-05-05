import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command

def generate_launch_description():
    package_name = 'my_robot'
    
    # Paths to files
    urdf_path = os.path.join(get_package_share_directory(package_name), 'urdf', 'my_robot.urdf.xacro')
    rviz_path = os.path.join(get_package_share_directory(package_name), 'rviz', 'my_robot.rviz')
    
    # Process Xacro
    robot_description_content = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)
    
    # Gazebo Launch File (Step 6c)
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py'))
    )
    
    # Spawn Entity Node (Step 6d)
    spawn_robot = Node(
        package='gazebo_ros', 
        executable='spawn_entity.py', 
        arguments=['-topic', 'robot_description', '-entity', 'my_robot'],
        output='screen'
    )

    return LaunchDescription([
        # Robot State Publisher (Set use_sim_time to True)
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description': robot_description_content,
                'use_sim_time': True
            }]
        ),
        # RViz2 (Set use_sim_time to True)
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_path],
            parameters=[{'use_sim_time': True}]
        ),
        gazebo_launch,
        spawn_robot
    ])
