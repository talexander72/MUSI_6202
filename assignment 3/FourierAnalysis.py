import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sc
from scipy.io import wavfile
import scipy.io
from scipy import signal
from scipy.io.wavfile import read     # didnt use all of these, just copied from previous assignment




# QUESTION 1

def generateSinusoidal(a, fs, freq, length, phase):
    
    t = np.arange(length * fs) / fs
    x = a * np.sin(2 * np.pi * freq * t + phase)
    
    return t,x,fs

(t1,x1,fs) = generateSinusoidal(1,44100,400,0.5,(np.pi/2))
t_slice = t1[0:round(fs*.005)]
x_slice = x1[0:round(fs*.005)]
plt.plot(t_slice,x_slice)
plt.title('Generated Sinusoid')
plt.xlabel('time (seconds)')
plt.ylabel('amplitude')
plt.tight_layout()





# QUESTION 2

def generateSquare(a, fs, freq, length, phase):
    
    t = np.arange(length * fs) / fs
    x = np.zeros(t.size)
    w = 2 * np.pi * freq
    
    for i in range(1,10):
        (t,y,fs) = generateSinusoidal(a/(2*i-1),fs,freq*(2*i-1),length,phase)
        step = (a * 4 / np.pi) * y
        x = np.add(x,step)
    return t,x
        
(t2,x2) = generateSquare(1,44100,400,0.5,0)

t2_slice = t2[0:round(fs*.005)]
x2_slice = x2[0:round(fs*.005)]
plt.plot(t2_slice,x2_slice) 
plt.title('Approximated Square Wave')
plt.xlabel('time (seconds)')
plt.ylabel('amplitude')
plt.tight_layout()





# QUESTION 3

def computeSpectrum(x,fs):
    
    complex_spec = np.fft.fft(x)
    
    XAbs = np.abs(complex_spec)
    XAbs = XAbs[0:round(x.size/2)]  # trimming off conjugate symmetry for each returned value
    
    XPhase = np.angle(complex_spec)
    XPhase = XPhase[0:round(x.size/2)]
    
    XRe = np.real(complex_spec)
    XRe = XRe[0:round(x.size/2)]
    
    XIm = np.imag(complex_spec)
    XIm = XIm[0:round(x.size/2)]
    
    resolution = fs/x.size  # frequency resolution of fft
    f = np.zeros(round(x.size/2))
    for i in range(round(x.size/2)):
        f[i] = i*resolution
    
    plt.subplot(2,1,1)
    plt.plot(f,XAbs)
    plt.title('Magnitude and Phase Spectrum of Signal')
    plt.ylabel('amplitude')
    plt.subplot(2,1,2)
    plt.plot(f,XPhase)
    plt.xlabel('frequency (Hz)')
    plt.ylabel('phase (radians)')
    plt.tight_layout()
    
    return XAbs,XPhase,XRe,XIm,f
    
(XAbs1,XPhase1,XRe1,XIm1,f1) = computeSpectrum(x1,44100)     # spectrum of sin wave
(XAbs2,XPhase2,XRe2,XIm2,f2) = computeSpectrum(x2,44100)     #  spectrum of square wave
