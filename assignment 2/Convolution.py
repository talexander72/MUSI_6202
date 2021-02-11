import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sc
from scipy.io import wavfile
import scipy.io
from scipy import signal
from scipy.io.wavfile import read



x = np.ones(200)    #initializing x and h
x_pad = np.pad(x,1) #padding to allow proper indexing inside for loop

h1 = np.arange(25) / 25
h2 = [1]
h3 = np.flip(h1)
h = np.concatenate((h1,h2,h3))
h_pad = np.pad(h,75) #padding

t_x = np.arange(x.size)
t_h = np.arange(h.size)
t = np.arange(x.size + h.size - 1)



# length of any discrete convolution = (length of x) + (length of h) - 1
# if x is length 200 and h is length 100 then y  is length 299

def myTimeConv(x,h):
    out = []
    value = 0
    for i in range(t_x.size):
        value = value + x_pad[t_x.size-i] * h_pad[i]
        out = np.append(out, value)
    import time
    start_time = time.time()
    runtime = str("--- %s seconds ---" % (time.time() - start_time))
    return out, runtime
    
    
y,runtime = myTimeConv(x,h)
z = scipy.signal.convolve(x,h)
plt.plot(y)
plt.title('Discrete Convolution Output')
plt.xlabel('time (samples)')
plt.ylabel('amplitude')



def time_test(x,h):
    import time
    dummy = scipy.signal.convolve(x,h)
    start_time = time.time()
    runtime2 = str("--- %s seconds ---" % (time.time() - start_time))
    return runtime2


def CompareConv(x,h):
    y,runtime = myTimeConv(x,h)
    y = np.append(y,np.zeros(50))
    z = scipy.signal.convolve(x,h)
    
    diff = y-z
    
    abs_diff = np.abs(diff)
    mean_abs_diff = np.mean(abs_diff) # mean absolute difference
    mean_diff = np.sum(abs_diff) / (y.size * z.size) # mean difference  
    std_dev = np.std(diff) # standard deviation
    
    runtime2 = time_test(x,h)
    times = [runtime, runtime2] #
    return mean_diff, mean_abs_diff, std_dev, times

mean1, absmean1, deviation1, times1 = CompareConv(x,h)



def loadSoundFile(filename):
    fs,x = wavfile.read(filename)
    return x

x2 = loadSoundFile('piano.wav')
h2 = loadSoundFile('impulse-response.wav')
mean2, absmean2, deviation2, times2 = CompareConv(x2,h2)    # doesn't work, my padding inside my original function was causing me problems
