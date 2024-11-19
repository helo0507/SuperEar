import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import medfilt

# Custom colors
custom_colors_hex = [
    '#EAA8A8', '#E28080', '#E56B6B', '#E95555',
    '#EC4040', '#EF2B2B', '#DE1616', '#CD0000'
]
custom_colors = [tuple(int(h[i:i+2], 16) / 255 for i in (1, 3, 5)) for h in custom_colors_hex]

# File path
txt_file_path = "combined_amplitude_ratio_data.txt"

# Load data
frequencies, combined_amplitude_ratio = np.loadtxt(
    txt_file_path, skiprows=1, delimiter="\t", unpack=True
)

# Process to remove abrupt changes
filtered_combined_amplitude = medfilt(combined_amplitude_ratio, kernel_size=3)
threshold = np.mean(combined_amplitude_ratio) + 3 * np.std(combined_amplitude_ratio)
threshold_combined_amplitude = filtered_combined_amplitude.copy()

jump_indexes = np.where(np.abs(filtered_combined_amplitude - np.mean(combined_amplitude_ratio)) > threshold)[0]
for idx in jump_indexes:
    if 0 < idx < len(filtered_combined_amplitude) - 1:
        threshold_combined_amplitude[idx] = (filtered_combined_amplitude[idx - 1] + filtered_combined_amplitude[idx + 1]) / 2
    elif idx == 0:
        threshold_combined_amplitude[idx] = filtered_combined_amplitude[idx + 1]
    else:
        threshold_combined_amplitude[idx] = filtered_combined_amplitude[idx - 1]

# Plot the original and processed enhancement ratio
plt.figure(figsize=(10, 8))
plt.subplot(2, 1, 1)
plt.plot(frequencies, combined_amplitude_ratio, color=custom_colors[7], linewidth=1.5)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Enhancement Ratio')
plt.xlim(250, 1000)
plt.ylim(10, 300)

plt.subplot(2, 1, 2)
plt.plot(frequencies, threshold_combined_amplitude, color=custom_colors[7], linewidth=1.5)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Enhanced Ratio (Balanced)')
plt.xlim(250, 1000)
plt.ylim(10, 100)

plt.tight_layout()
plt.show()

# Gain balancing
smooth_window_size = 2
non_zero_gains = threshold_combined_amplitude[threshold_combined_amplitude > 5]
gain_threshold = np.mean(non_zero_gains)
adaptive_gain = np.ones_like(threshold_combined_amplitude)

for i, gain in enumerate(threshold_combined_amplitude):
    if gain > gain_threshold:
        adaptive_gain[i] = gain_threshold / gain
    elif gain > 0:
        adaptive_gain[i] = gain / gain_threshold

adaptive_gain_smoothed = np.convolve(adaptive_gain, np.ones(smooth_window_size) / smooth_window_size, mode='same')
adjusted_threshold_amplitude = threshold_combined_amplitude * adaptive_gain_smoothed

# Plot the original and balanced enhancement ratio
plt.figure(figsize=(10, 8))

plt.subplot(2, 1, 1)
plt.plot(frequencies, threshold_combined_amplitude, color=custom_colors[7], linewidth=1.5)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Enhancement Ratio')
plt.xlim(250, 1000)
plt.ylim(10, 300)

plt.subplot(2, 1, 2)
plt.plot(frequencies, adjusted_threshold_amplitude, color=custom_colors[7], linewidth=1.5)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Enhanced Ratio (Balanced)')
plt.xlim(250, 1000)
plt.ylim(10, 100)

plt.tight_layout()
plt.show()

# Calculate gain difference curve
gain_difference_ratio = adjusted_threshold_amplitude / combined_amplitude_ratio

# Plot the gain difference curve
plt.figure(figsize=(10, 6))
plt.plot(frequencies, gain_difference_ratio, color=custom_colors[3], linewidth=1.5)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Gain Difference Ratio')
plt.title('Gain Difference Curve')
plt.xlim(250, 1000)
plt.ylim(0, 10)  # Adjust the y-axis range based on actual needs
plt.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()

# Export gain difference curve data
output_file_path = "gain_difference_ratio_curve.txt"
export_data = np.column_stack((frequencies, gain_difference_ratio))
np.savetxt(output_file_path, export_data, delimiter="\t", header="Frequency (Hz)\tGain Difference Ratio", fmt="%.6f")

print(f"Gain difference curve successfully exported to: {output_file_path}")
