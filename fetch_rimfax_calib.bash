#!/bin/bash

targdir="/zippy/MARS/orig/supl/RIMFAX"

# Grab MD5 hashes
wget -P $targdir -N 'https://pds-geosciences.wustl.edu/m2020/urn-nasa-pds-mars2020_rimfax/urn-nasa-pds-mars2020_rimfax.md5'

wget -P $targdir -m -nH -np --cut-dirs=2  'https://pds-geosciences.wustl.edu/m2020/urn-nasa-pds-mars2020_rimfax/data_calibrated/'

