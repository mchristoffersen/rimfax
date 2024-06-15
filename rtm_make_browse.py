import os
import glob
import m8r
import matplotlib.pyplot as plt
import numpy as np
import sys

file = sys.argv[1]

# Title for plot
name = os.path.basename(file).replace(".rsf", "").split("_")
name = "_".join(name[:3]) + " " + name[3]

# Title for plot
name = os.path.basename(file).replace(".rsf", "").split("_")
name = name[2] + " " + name[3]

# Plot width and height
inp = m8r.Input(file)
n1 = inp.int("n1")
d1 = inp.float("d1")
n2 = inp.int("n2")
d2 = inp.float("d2")
data = inp.read().T
inp.close()

if(len(data.shape) == 1):
    data = np.expand_dims(data, 1)

if ("Surface") in file:
    pclip = 2
    hgt = n1/2
    data = data[::2]

elif ("Shallow") in file:
    pclip = 0.5
    hgt = n1/10
    t = (np.arange(n1)-575)*d1
    t[t < 0] = 0
    gain = t**(1.5)
    data = data*gain[:, np.newaxis]
    data = data[::10, :]

elif ("Deep") in file:
    pclip = .1
    hgt = n1/5
    t = (np.arange(n1)-564)*d1
    t[t < 0] = 0
    gain = t**(2)
    gain[gain > 0.5e6] = 0.5e6
    data = data*gain[:, np.newaxis]
    data = data[::5, :]

else:
    exit()

wth = n2*4

fig = plt.figure(figsize=(wth, hgt), dpi=1)
ax = fig.add_axes([0, 0, 1, 1])  # span the whole figure
ax.set_axis_off()

ax.imshow(data, cmap='Greys', aspect='auto', interpolation="Lanczos", vmin=np.percentile(data, pclip), vmax= np.percentile(data, 100-pclip))

#plt.figure(figsize=(wth, hgt))
#plt.imshow(data, cmap="Greys", vmin=np.percentile(data, 2), vmax=np.percentile(data, 98), extent=[0, n2*d2, n1*d1, 0])
#plt.xlabel("Distance (m)")
#plt.ylabel("Time (ns)")
#plt.title(name)
plt.savefig(file.replace(".rsf", ".jpg"))
plt.close()
