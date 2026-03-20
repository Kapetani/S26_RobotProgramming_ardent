import os
from glob import glob
from setuptools import setup

package_name = 'test_tf2_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.launch.py'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Timothy Blyumin',
    description='TF2 demo for Lecture 13',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'broadcaster = test_tf2_py.turtle_tf2_broadcaster:main',
            'listener = test_tf2_py.turtle_tf2_listener:main',
        ],
    },
)
