import numpy as np
from scipy.signal import butter, filtfilt, sosfiltfilt
import scipy
from IPython.display import Audio, Image

def main():
    print('Enter MIDI notes (separated by commas):')
    a=input()
    map(int, a.split(','))
    notes = np.array(a)
    print('Enter MIDI note durations in seconds:')
    b=input()
    map(int, b.split(','))
    durs = np.array(b)
    print('Enter sampling rate:')
    c=input()
    fs=int(c)
    print('Apply Chorus? (True/False):')
    d=input()
    if (d=='True'):
        chorus=True
    else:
        chorus=False
    print('Delay Time (0-44100 samples):')
    e=input()
    delay=int(e)
    print('Select Reverb Space (none, garage, hallway, or deepspace):')
    reverbSpace=input()
    print('Apply Flanger? (True/False):')
    g=input()
    if (g=='True'):
        flanger=True
        print('Enter Flanger Rate (default 1):')
        h=input()
        flangeRate=int(h)
        print('Enter Flanger Depth (default 0.01):')
        i=input()
        flangeDepth=int(i)
    else:
        flanger=False
        flangeRate=0
        flangeDepth=0
    print('Apply Lowpass Filter? (True/False):')
    j=input()
    if (j=='True'):
        lowpass=True
        print('Enter Cutoff Frequency:')
        k=input()
        FcLow = int(k)
        print('Enter Filter Order:')
        l=input()
        orderLow = int(l)
    else:
        lowpass=False
        FcLow=0
        orderLow=4
    print('Apply Highpass Filter? (True/False)')
    m=input()
    if (m=='True'):
        highpass = True
        print('Enter Cutoff Frequency):')
        n=input()
        FcHigh=int(n)
        print('Enter Filter Order):')
        o=input()
        orderHigh = int(o)
    else:
        highpass = False
        FcHigh = 0
        orderHigh = 4
    print('Please Refer to File: "output.wav"')




### Main Bandpass Filter for Subtractive Synthesis ###

    def butter_bandpass(cutoff1, cutoff2, order):
        fs = 44100
        nyq = 0.5 * fs
        normal_cutoff1 = cutoff1 / nyq
        normal_cutoff2 = cutoff2 / nyq
        white, off = butter(order, [normal_cutoff1, normal_cutoff2], btype='bandpass')
        return (white, off)

    def bandaid(data, cutoff, order):
        fs = 44100
        cutoff1 = cutoff - 5
        cutoff2 = cutoff + 5
        white, off = butter_bandpass(cutoff1, cutoff2, order)
        song = filtfilt(white, off, data)  # filtfilt
        return song



    ### Lowpass Filter ###

    def butter_lowpass(cutoff, order):
        fs = 44100
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        low, off = butter(order, normal_cutoff, btype='low', output='sos')  # svd filter
        return (low, off)

    def bandaid_low(data, cutoff, order):
        fs = 44100
        low, off = butter_lowpass(cutoff, order)
        song = sosfiltfilt(low, data)
        return song



    ### Highpass Filter ###

    def butter_highpass(cutoff, order):
        fs = 44100
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        high, off = butter(order, normal_cutoff, btype='hp', output='sos')  # svd filter
        return (high, off)

    def bandaid_high(data, cutoff, order):
        fs = 44100
        high, off = butter_lowpass(cutoff, order)
        song = sosfiltfilt(high, data)
        return song



    ### Convolution Reverb ###

    from scipy.io import wavfile
    from scipy import signal

    fs1, hallway = wavfile.read('/Users/tuckeralexander/PycharmProjects/pythonProject1/venv/Conic Long Echo Hall.wav')
    fs2, deepspace = wavfile.read('/Users/tuckeralexander/PycharmProjects/pythonProject1/venv/Deep Space.wav')
    fs3, garage = wavfile.read('/Users/tuckeralexander/PycharmProjects/pythonProject1/venv/Parking Garage.wav')

    def convolution_reverb(midi, IR):
        out = signal.convolve(midi, IR[:, 1])
        return (out)



    ### Processing of MIDI Input and Emplementation of Effects ###

    def white(notes, durs, fs=44100, chorus=False, delay=0, reverbSpace='none', flanger=False, flangeRate=5,
              flangeDepth=.01, lowpass=False, FcLow=0, orderLow=4, highpass=False, FcHigh=0, orderHigh=4):

        baseSound = noteCreate(notes, durs)

        ### Chorus (add major third to each note) ###
        finalSound = np.zeros((2, len(baseSound)))
        finalSound[0, :] = baseSound
        if chorus:
            finalSound[1, :] = noteCreate(np.array(notes) + 4, durs)
            finalSound = np.sum(finalSound, axis=0)
        else:
            finalSound = finalSound.flatten()

        ### Flanger (time varying delay) ###
        length = len(finalSound)
        currentSample = np.array(range(length))
        lfo = 2 + np.sin(2 * np.pi * flangeRate * (currentSample) / fs)
        index = np.around(currentSample - fs * flangeDepth * lfo)
        index[index < 0] = 0
        index[index > (length - 1)] = length - 1
        out = np.zeros(length)
        if flanger:
            for i in range(length):
                out[i] = float(finalSound[i]) + float(finalSound[int(index[i])])
            finalSound = out

        ### Delay (input range 0-44100, max corresponding to 1 second)
        h = np.zeros((1, fs)).flatten()
        h[0] = 1
        h[delay] = 1
        finalSound = np.convolve(finalSound, h)

        h1 = np.zeros((1, fs)).flatten()
        h1[0] = 1
        h1[delay] = 1
        finalSound = np.convolve(finalSound, h1)

        ### Convolution Reverb (choose from 3 environmental IR's) ###
        if (reverbSpace == 'hallway'):
            finalSound = convolution_reverb(finalSound, hallway)
        elif (reverbSpace == 'garage'):
            finalSound = convolution_reverb(finalSound, garage)
        elif (reverbSpace == 'deepspace'):
            finalSound = convolution_reverb(finalSound, deepspace)

        ### Lowpass and Highpass Filters ###
        if lowpass:
            finalSound = bandaid_low(finalSound, FcLow, orderLow)

        if highpass:
            finalSound = bandaid_high(finalSound, FcHigh, orderHigh)

        return finalSound

    def delayrace(data, mm, scale):
        pad = np.zeros(int(len(data) / 1000 * mm))
        NewX = data / abs(data).max()
        song = np.concatenate([NewX, pad])
        d1song = np.concatenate([pad, NewX])
        final = song + (d1song * scale)
        return (final)

    def noteCreate(notes, durs):
        sr = 44100  # sample rate
        check = len(notes)  # first check, same lengths
        check2 = len(durs)
        totalsound = np.array([])
        lengths = np.zeros(len(durs))  # zeros array to alter with lengths of notes in samples
        if check == check2:  # ensures same inputs lengths
            count = check
            notes = newnote(notes)
            for i in range(count):  # main iterater.
                lengths[i] = sr * durs[i]
                whitey = np.random.randn(int(lengths[i]))  # Generates a white noise for given number of samples
                sound = bandaid(data=whitey, cutoff=notes[i], order=3)  # run white noise through the steep band pass
                (r, e, soundEnv) = ADSR(sound, durs[i])  # applies ADSR to each note
                totalsound = np.concatenate((totalsound, soundEnv))  # concatenates the sounds

        else:
            print('please ensure that you have entered the same number of durations as notes')
            return ()
        finalSound = delayrace(totalsound, 65, 0.3)
        return (finalSound)

    #This turns our midi values into frequencies
    def newnote(notes):
        import numpy as np
        trueKeys = np.array(notes)
        relativeKeys = trueKeys-60
        freq = 440*2**(relativeKeys/12)
        return(freq)


    # This applies a uniform ADSR envelope to each of our notes
    def ADSR(x, dur, a=.2, d=.2, sustain=.5, r=.2, fs=44100):
        ti = fs * dur
        ax = np.arange(0, a, 1 / ti)
        ay = np.linspace(0, 1, ax.size)

        if (sustain == 0):  # sustain is false when the sustain level argument is 0
            rx = np.arange(a, a + r, 1 / ti)
            ry = np.linspace(1, 0, rx.size)

            restx = np.arange(a + r, x.size / ti, 1 / ti)
            resty = np.linspace(0, 0, restx.size)

            t = np.concatenate((ax, rx, restx))
            y = np.concatenate((ay, ry, resty))

            signal = np.multiply(x, y)
            return (t, y, signal)


        else:
            dx = np.arange(a, (a + d), 1 / ti)
            dy = np.linspace(1, sustain, dx.size)

            sx = np.arange(a + d, (x.size / ti) - r, 1 / ti)
            sy = np.linspace(sustain, sustain, sx.size)

            rx = np.arange((x.size / ti) - r, x.size / ti, 1 / ti)
            ry = np.linspace(sustain, 0, rx.size)

            t = np.concatenate((ax, dx, sx, rx))
            y = np.concatenate((ay, dy, sy, ry))

            signal = np.multiply(x, y)
            return (t, y, signal)

    soundtest1 = white(notes, durs, fs, chorus, delay, reverbSpace, flanger, flangeRate, flangeDepth, lowpass, FcLow, orderLow, highpass, FcHigh, orderHigh)
    scipy.io.wavfile.write('output.wav', 44100, soundtest1)

if __name__=="__main__":
    main()

