echo "DINAMYXEL FIND"
echo "************************************"
echo "Ricordati di alimentare i dynamixel "
echo " "
echo " cerco i dynamixel su /dev/ttyACM1"
echo "************************************"
#sudo chmod 666 /dev/ttyACM10
rosrun dynamixel_workbench_controllers find_dynamixel /dev/ttyACM1
