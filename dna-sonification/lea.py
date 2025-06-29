import music21
print(music21.__version__)

from music21 import note, stream

# Define the DNA-to-note mapping
nucleotide_to_note = {
    'A': 'C2',
    'T': 'G4',
    'C': 'C6',
    'G': 'F#7'
}

dna_sequence = input("Enter NONmutated DNA sequence: ")

# music stream 
melody = stream.Stream 

# tempo setting 
tempo_mark = tempo.MetronomeMark(number=100) 
