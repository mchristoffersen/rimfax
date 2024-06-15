#!/bin/bash

find /zippy/MARS/targ/supl/RIMFAX/data_calibrated/rsf -name "*.rsf" | parallel -j 40 python /zippy/MARS/code/supl/RIMFAX/make_browse.py

mv /zippy/MARS/targ/supl/RIMFAX/data_calibrated/rsf/*.jpg /zippy/MARS/targ/supl/RIMFAX/data_calibrated/jpg/
