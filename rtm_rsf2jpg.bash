#!/bin/bash

find /zippy/MARS/code/supl/RIMFAX/rtm/ -name "isc*.rsf" | parallel -j 40 python /zippy/MARS/code/supl/RIMFAX/rtm_make_browse.py
