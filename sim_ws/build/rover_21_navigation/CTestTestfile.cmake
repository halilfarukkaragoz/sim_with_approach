# CMake generated Testfile for 
# Source directory: /home/halil/Documents/sim_ws/src/rover_21_autonomous_drive-master/rover_21_navigation
# Build directory: /home/halil/Documents/sim_ws/build/rover_21_navigation
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(_ctest_rover_21_navigation_roslaunch-check_launch "/home/halil/Documents/sim_ws/build/rover_21_navigation/catkin_generated/env_cached.sh" "/usr/bin/python2" "/opt/ros/melodic/share/catkin/cmake/test/run_tests.py" "/home/halil/Documents/sim_ws/build/rover_21_navigation/test_results/rover_21_navigation/roslaunch-check_launch.xml" "--return-code" "/usr/bin/cmake -E make_directory /home/halil/Documents/sim_ws/build/rover_21_navigation/test_results/rover_21_navigation" "/opt/ros/melodic/share/roslaunch/cmake/../scripts/roslaunch-check -o \"/home/halil/Documents/sim_ws/build/rover_21_navigation/test_results/rover_21_navigation/roslaunch-check_launch.xml\" \"/home/halil/Documents/sim_ws/src/rover_21_autonomous_drive-master/rover_21_navigation/launch\" ")
subdirs("gtest")
