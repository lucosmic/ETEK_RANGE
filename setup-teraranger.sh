pip install pyserial
pip install crcmod

read -n1 -r -p "Plug in USB. Make sure the connection is solid." key
ls /dev/ttyA*

read -n1 -r -p "ttyAMA# should pop up. Else run \"ls /dev/ttyA*\""

