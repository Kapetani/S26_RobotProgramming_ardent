import os
from glob import glob
from setuptools import setup

package_name = 'time_tf2_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.launch.py'))),
    ],
    entry_points={
        'console_scripts': [
            'broadcaster = time_tf2_py.turtle_tf2_broadcaster:main',
            'listener = time_tf2_py.turtle_tf2_listener:main',
        ],
    },
)
