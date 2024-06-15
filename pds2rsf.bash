#!/bin/bash
echo "SLEEPING FOR 6 HOURS!!!"

sleep 6h

files=`ls /zippy/MARS/orig/supl/RIMFAX/data_calibrated/202?/*.xml`

for file in $files:
do
    python /zippy/MARS/code/supl/RIMFAX/rimfax/sfrimfaxread.py $file
done
