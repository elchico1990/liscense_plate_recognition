
check_file()
{
	if [ ! -f "$1" ]
	then
		return 0
	else
		return 1
	fi
}

check_dir()
{
	if [ ! -d "$1" ]
	then
		return 0
	else
		return 1
	fi
}


# Check if Darknet is compiled
check_file "darknet/libdarknet.so"
retval=$?
if [ $retval -eq 0 ]
then
	echo "Darknet is not compiled! Go to 'darknet' directory and 'make'!"
	exit 0
fi

# Check # of arguments
if [ ! $# -eq 3 ]
then
	echo ""
	echo " Required arguments:"
	echo ""
	echo "   1. Output dir path"
	echo "   2. Output CSV file path"
	echo "   3. Video file "
	echo ""
	exit 1
fi

read -n1 -r -p "Press any key to continue..." key


# Download all networks
#bash get-networks.sh


# Check if input dir exists
# check_dir $1
# retval=$?
# if [ $retval -eq 0 ]
# then
# 	echo "Input directory ($1) does not exist"
# 	exit 0
# fi

# Check if output dir exists, if not, create it
check_dir $1
retval=$?
if [ $retval -eq 0 ]
then
	mkdir -p $1
fi

# Setting up

python3 main.py $1 $3
# Detect vehicles
python3 vehicle-detection.py $1

# Detect license plates
python3 license-plate-detection.py $1

# OCR
python3 license-plate-ocr.py $1
#
# # Draw output and generate list
python3 gen-outputs.py $1 > $2

# Clean files and draw output
rm $1/*_lp.png
rm $1/*car.png
rm $1/*_cars.txt
rm $1/*_lp.txt
rm $1/*_str.txt
rm -rf $1/images_from_video
