import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# Read the audio files
Fs, signal = wavfile.read('Test_Enhanced_Audio.wav')  # Target audio signal
Fs_noise, noise_signal = wavfile.read('noise.wav')  # Noise audio signal

# Ensure the signal is multi-channel; expand dimensions if single-channel
if signal.ndim == 1:
    signal = np.expand_dims(signal, axis=1)
if noise_signal.ndim == 1:
    noise_signal = np.expand_dims(noise_signal, axis=1)

# Get the length of the signals
len_signal = signal.shape[0]
len_noise = noise_signal.shape[0]

# Extract individual channels from the signals
channels = [signal[:, i] for i in range(signal.shape[1])]
noise_channels = [noise_signal[:, i] for i in range(noise_signal.shape[1])]

# Set parameters for frequency spectrum analysis
N = len(channels[0])
NFFT = 2 ** int(np.ceil(np.log2(N)))
frequencies = Fs / 2 * np.linspace(0, 1, NFFT // 2 + 1)

# Extract the noise spectrum and calculate the noise threshold
noise_spectrum = np.abs(np.fft.fft(noise_channels[0], NFFT)[:NFFT // 2 + 1])
noise_threshold = np.mean(noise_spectrum) * 1.5  # Threshold for significant noise

# Define audio channels and corresponding frequency ranges
audio_files = [
    channels[7], channels[0], channels[1], channels[6],
    channels[5], channels[4], channels[7], channels[0],
    channels[3], channels[1], channels[3], channels[7]
]
freq_ranges = [
    (0, 206.752), (206.794, 326.321), (326.405, 365.139), (365.181, 443.702),
    (443.744, 559.653), (559.695, 683.679), (683.721, 836.977), (837.019, 932.933),
    (933.035, 971.476), (971.518, 1040.79), (1040.83, 1082.55), (1082.59, 2344.6)
]

# Extract spectral segments from each frequency range
spectrum_segments = []
for i, audio in enumerate(audio_files):
    Y = np.fft.fft(audio, NFFT) / N
    f = Fs / 2 * np.linspace(0, 1, NFFT // 2 + 1)
    idx_range = np.where((f >= freq_ranges[i][0]) & (f <= freq_ranges[i][1]))[0]
    
    # Check if the frequency range overlaps with noise
    noise_overlap = np.any(noise_spectrum[idx_range] > noise_threshold)
    
    if noise_overlap:
        # Use the previous channel to replace the noisy one
        if i > 0:
            prev_audio = audio_files[i - 1]
            prev_Y = np.fft.fft(prev_audio, NFFT) / N
            spectrum_segments.extend(prev_Y[idx_range])
        else:
            # Skip if it's the first channel
            continue
    else:
        spectrum_segments.extend(Y[idx_range])

# Combine spectral segments into a single spectrum
new_spectrum = np.zeros(NFFT, dtype=np.complex)
new_spectrum[:len(spectrum_segments)] = spectrum_segments
new_spectrum[-len(spectrum_segments):] = np.conj(spectrum_segments[::-1])

# Adjust specific target frequencies
target_frequencies = [463.342, 475.791, 471.123, 927.61, 1383.42, 1552.45, 1752.31]
divisors = [22, 14, 8, 31, 17, 10, 8]

for target_freq, divisor in zip(target_frequencies, divisors):
    idx = np.argmin(np.abs(frequencies - target_freq))
    new_spectrum[idx] /= divisor

# Compute the magnitude of the frequency spectrum
spectrum_magnitude = np.abs(new_spectrum[:NFFT // 2 + 1])

# Plot the spectrum
plt.figure(figsize=(10, 6))
plt.plot(frequencies, spectrum_magnitude, linewidth=1.5, label="Noise Reduced Spectrum")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("Frequency Spectrum After Noise Reduction")
plt.grid(True)
plt.xlim(0, 1000)
plt.legend()
plt.show()
