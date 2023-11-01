import xml.etree.ElementTree as et
import os
import getpass
import socket
from datetime import datetime

import pandas as pd
import numpy as np
from tqdm import tqdm


class cdr:
    def __init__(self, xml, progress_bar=False):
        # Parse label
        self.xml = xml
        self.label = et.parse(self.xml).getroot()

        # Get CSV name
        self.csv = os.path.dirname(self.xml) + "/" + (
            self.label.find("{http://pds.nasa.gov/pds4/pds/v1}File_Area_Observational")
            .find("{http://pds.nasa.gov/pds4/pds/v1}File")
            .find("{http://pds.nasa.gov/pds4/pds/v1}file_name")
            .text
        )

        # Parse CSV
        with open(self.csv, mode="r") as fd:
            nlines = len(fd.readlines())

        if progress_bar:
            self.data = pd.concat(
                [
                    chunk
                    for chunk in tqdm(
                        pd.read_csv(self.csv, chunksize=100, engine="python"),
                        desc="Loading CDR",
                        total=np.ceil(nlines / 100),
                        unit="chunk",
                    )
                ]
            )
        else:
            self.data = pd.read_csv(self.csv, engine="python")

    def writeRSF(self, progress_bar=False):
        # Pull out active sounding
        data_active = self.data[self.data["record_type"] == 0]
        modes = data_active["mode_name"].unique()

        for mode in tqdm(
            modes, desc="Writing RSF Files", disable=(not progress_bar), unit="file"
        ):
            data_active_sub = data_active[data_active["mode_name"] == mode]

            # Make name from CSV name
            rsf = os.path.abspath(self.csv.replace(".csv", "_%s.rsf" % mode))

            # Get number of samples and sample interval for mode
            #print(data_active_sub["n_samples"].mode())
            nsamp = data_active_sub["n_samples"].mode()[0]
            dt = data_active_sub["sample_time_increment"].to_numpy()[0]

            # Remove stationary soundings and get spacing between soundings
            data_active_sub_roving = data_active_sub[data_active_sub["stationary_sounding"] == 0]
            if(len(data_active_sub_roving) == 0):
                print("Skipping RSF build for mode:", mode)
                continue
            
            dx = data_active_sub_roving["sounding_group_spacing"].to_numpy()[0]


            # Check assumption that sounding group spacing is constant, whine and quit if not
            if(len(np.unique(data_active_sub_roving["sounding_group_spacing"])) != 1):
                print("Non-constant sample group spacing:", np.unique(data_active_sub_roving["sounding_group_spacing"]))
                print("File:", self.csv)
                print("Not handled. Quitting.")
                return

            # Write RSF header
            fd = open(rsf, mode="w")

            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            fd.write(
                "4.0\tsfrimfaxread\t%s:\t%s@%s\t%s\n\n"
                % (os.getcwd(), getpass.getuser(), socket.gethostname(), dt_string)
            )
            fd.write('\tin="stdin"\n')
            fd.write('\tdata_format="native_float"\n')
            fd.write("\tesize=4\n")
            fd.write('\tlabel1="Time"\n')
            fd.write('\tunit1="ns"\n')
            fd.write("\tn1=%d\n\to1=0\n\td1=%.9f\n" % (nsamp, dt))
            fd.write('\tlabel2="Distance"\n')
            fd.write('\tunit2="m"\n')
            fd.write("\tn2=%d\n\to2=0\n\td2=%2.2f\n" % (len(data_active_sub_roving), dx/100.0))
            fd.write("\n\f\f\x04") # nl ff ff eot

            fd.close()

            # Extract and write data
            startC = "s0001"
            stopC = "s" + str(nsamp)
            rgram = data_active_sub_roving.loc[:, startC:stopC].to_numpy().astype(np.float32)

            fd = open(rsf, mode="ab")
            rgram.tofile(fd)
            fd.close()
