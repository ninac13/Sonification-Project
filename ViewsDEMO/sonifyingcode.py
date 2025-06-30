import numpy as np
from scipy.io.wavfile import write

# Map DNA bases to frequencies (Hz)
note_map = {
    "A": 65.41,   # C2
    "T": 392.00,  # G4
    "C": 1046.50, # C6
    "G": 2959.96  # F#7
}

# Audio settings
sample_rate = 44100  # CD-quality
bpm = 100
duration_per_note = 60 / bpm  # seconds per beat (0.6 sec at 100 BPM)

def base_to_tone(base, duration=duration_per_note):
    freq = note_map.get(base, 0)
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = 0.5 * np.sin(2 * np.pi * freq * t)
    return tone

def sequence_to_waveform(sequence):
    tones = [base_to_tone(base) for base in sequence]
    return np.concatenate(tones)

# Sequences
normal_seq = "ATGGTGCACCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAACGTGGATGAAGTTGGTGGTGAGGCCCTGGGCAG"
mutated_seq = "ATGGTGCACCTGACTCCTGTGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAACGTGGATGAAGTTGGTGGTGAGGCCCTGGGCAG"

# Convert to audio waveforms
normal_wave = sequence_to_waveform(normal_seq)
mutated_wave = sequence_to_waveform(mutated_seq)

# Pad shorter one (if needed)
max_len = max(len(normal_wave), len(mutated_wave))
normal_wave = np.pad(normal_wave, (0, max_len - len(normal_wave)))
mutated_wave = np.pad(mutated_wave, (0, max_len - len(mutated_wave)))

# Overlay (mix) the two
combined_wave = (normal_wave + mutated_wave) / 2.0  # Keep volume in range

# Normalize to 16-bit PCM range
audio_data = np.int16(combined_wave / np.max(np.abs(combined_wave)) * 32767)

# Export to WAV
write("demo_sonification.wav", sample_rate, audio_data)
print("✅ Exported: demo_sonification.wav")
