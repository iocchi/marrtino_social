echo "Centra tutti i servo"
echo "          +---+"
echo "          |* *|"
echo "          +---+"
echo "   5    4 3 | 6 7    8"
echo "o--+----+-+ - +-+----+--o"
rostopic pub -1 /spallasx_controller/command std_msgs/Float64 2.6
rostopic pub -1 /spalladx_controller/command std_msgs/Float64 2.6
rostopic pub -1 /spallasxj_controller/command std_msgs/Float64 2.6
rostopic pub -1 /spalladxj_controller/command std_msgs/Float64 2.6
rostopic pub -1 /gomitosx_controller/command std_msgs/Float64 2.6
rostopic pub -1 /gomitodx_controller/command std_msgs/Float64 2.6
echo "Avanti rotazione DX"
rostopic pub -1 /spalladx_controller/command std_msgs/Float64 1.6
echo "Avanti SX"
rostopic pub -1 /spallasx_controller/command std_msgs/Float64 3.6
echo " flessione DX chiude"
rostopic pub -1 /spalladxj_controller/command std_msgs/Float64 3.6
echo " flessione SX chiude"
rostopic pub -1 /spallasxj_controller/command std_msgs/Float64 1.6
echo " gomito DX apre"
rostopic pub -1 /gomitodx_controller/command std_msgs/Float64 3
echo " gomito SX apre"
rostopic pub -1 /gomitosx_controller/command std_msgs/Float64 1.6
echo " gomito DX chiude"
rostopic pub -1 /gomitodx_controller/command std_msgs/Float64 1.6
echo " gomito SX chiude"
rostopic pub -1 /gomitosx_controller/command std_msgs/Float64 3