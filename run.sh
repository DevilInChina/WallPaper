Origin=$1
Pic_Geb=$2
Mtx=$3
Runner=python3

for i in $(ls $Origin);
do
	Runner main.py $Origin$i $Pic_Geb $Mtx
done
