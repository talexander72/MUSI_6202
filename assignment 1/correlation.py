### loading in packages
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sc
from scipy.io import wavfile
import scipy.io
from scipy import signal
from scipy.io.wavfile import read

### function 1
def crossCorr(x,y):
    z = sc.correlate(x,y)
    z = z / np.max(z)
    return z
    
### function 2
def loadSoundFile(filename):
    fs,x = wavfile.read(filename)
    x = x[:,0]
    return x

### QUESTION 1 MAIN FUNCTION
def correlator():
    snare = loadSoundFile('snare.wav')
    loop = loadSoundFile('drum_loop.wav')
    z = crossCorr(snare,loop)
    n = np.arange(z.size)
    plt.plot(n,z)
    plt.title('Cross Correlation')
    plt.xlabel('Sample Number')
    plt.ylabel('Correlation Coefficient')
    return
    
correlator()
    
### QUESTION 2 MAIN FUNCTION
def findSnarePosition(snareFilename,drumloopFilename):
    snare = loadSoundFile(snareFilename)
    loop = loadSoundFile(drumloopFilename)
    z = crossCorr(snare,loop)
    pos = []
    for i in np.arange(len(z)):
        if z[i]==1:
            pos.append(i)
    return pos

findSnarePosition('snare.wav','drum_loop.wav')
