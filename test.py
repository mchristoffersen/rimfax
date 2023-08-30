from edr import edr
from cdr import cdr

rfax = cdr("./rimfax_calibrated_00415.xml")
rfax.writeRSF()
