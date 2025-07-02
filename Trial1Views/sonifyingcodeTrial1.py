import numpy as np
from scipy.io.wavfile import write

# Same note map as the demo (mid-range, dissonant)
note_map = {
    "A": 311.13,   # D#4
    "T": 370.00,   # F#4
    "C": 415.30,   # G#4
    "G": 554.37    # C#5
}

sample_rate = 44100
bpm = 100
duration_per_note = 60 / bpm  # Same tempo as demo

def apply_envelope(wave, fade_fraction=0.05):
    fade_len = int(len(wave) * fade_fraction)
    fade_in = np.linspace(0, 1, fade_len)
    fade_out = np.linspace(1, 0, fade_len)
    envelope = np.ones(len(wave))
    envelope[:fade_len] *= fade_in
    envelope[-fade_len:] *= fade_out
    return wave * envelope

def base_to_tone(base, duration=duration_per_note):
    freq = note_map.get(base, 0)
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = 0.5 * np.sin(2 * np.pi * freq * t)
    return apply_envelope(tone)

def sequence_to_waveform(sequence):
    tones = [base_to_tone(base) for base in sequence]
    return np.concatenate(tones)

# ⏩ Trial 1 Sequences
normal_seq = "CCACCATAGTACTACGATAGCCTAACGCGTTATGGCCAATGGCGGAGCTAACGGCTAGCTTGGTCACCCCTGCTAAAGAAAGAGGAGGAGTCACTCCTCGAAGTCTCCCCGGACTCAAACACCTTATAGCCCGTCAAGCTAATAATGGTATGAAGACTACGGATTGCCCGGTGCAGCTCGCGGTCATCTTCCTCAAGGCCGCACCTATGATACGACTTTGATTTGCGTGTAACTCGTAAGCAGTAGTAAGCGACATGGTATTACGTACAGTCTTTCAAGGAGCAAAAACATCACGTGCAGGCGAGATCCAACCTGTAAGAAATTCTATGCAGTACGGCAGTTTACGTAAATTAAAACTCAACAGAGCCTCCCCTTGCAGTCGTTTGAGAATAGACAAGTCTGCGGATCCGCCTTGTACGCCTAATTAGTGACGAAGCGAAACTACCTAGTGCTCATACTTCTGCAAATCGGTAGGCAACG"
mutated_seq = "CCACCATAGTACAACGATAGCCTAACGCGTTATGGCCAATGGCGGAGCTAACGGCTAGCTTGGTCACCCCTGCTAAAGAAAGAGGAGGAGTCACTCCTCGAAGTCTGCCCGGACTCAAACACCTTATAGCCCGTCAAGCTAATAATGGTATGAAGCCTACGGATTGCCCGGTGCAGCTCGCGGTCATCTTCCTCAAGGCCGCACCTATGATATGACTTTGATTTGCGTGTAACTCGTAAGCAGTAGTAAGCGACATGGTATTACGTACAGTCTTTCAAGGAGCAAAAACATCACGTGCAGGCGAGATCCAACCTGAAAGAAATTCTATGCAGTACGGCAGTTTACGTAAATTAAAACTCAACAGAGCCTCCCCTTGCAGTCGTTTGAGAATAGACAAGTCTGCGGATCCGCCTTGGACGCCTAATTAGTGACGAAGCGAAACTACCTAGTGCTTATACTTCTGCAAATCGGTAGGCAACG"

# 🎵 Convert both to waveform
normal_wave = sequence_to_waveform(normal_seq)
mutated_wave = sequence_to_waveform(mutated_seq)

# 🧊 Pad to match length
max_len = max(len(normal_wave), len(mutated_wave))
normal_wave = np.pad(normal_wave, (0, max_len - len(normal_wave)))
mutated_wave = np.pad(mutated_wave, (0, max_len - len(mutated_wave)))

# 🎚️ Mix together
combined_wave = (normal_wave + mutated_wave) / 2.0

# 🔊 Normalize
audio_data = np.int16(combined_wave / np.max(np.abs(combined_wave)) * 32767)

# 💾 Export as Trial 1 file
write("trial1_sonification.wav", sample_rate, audio_data)
print("✅ Exported: trial1_sonification.wav")
