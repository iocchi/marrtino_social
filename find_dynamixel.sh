echo "DINAMYXEL FIND"
echo "************************************"
echo "Ricordati di alimentare i dynamixel "
echo " "
echo " cerco i dynamixel su /dev/ttyUSB0"
echo "************************************"
#sudo chmod 666 /dev/ttyUSB0
rosrun dynamixel_workbench_controllers find_dynamixel /dev/ttyUSB0
