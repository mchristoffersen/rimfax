#!/bin/bash

files=`ls /zippy/MARS/code/supl/RIMFAX/rtm_shallow/isc_*.rsf`
odir='/zippy/MARS/targ/supl/RIMFAX/data_calibrated/rtm_shallow/'
mkdir -p $odir

for file in $files
do
        ofile=$odir`basename $file`
	sfcp < $file > $ofile --out=stdout
done
