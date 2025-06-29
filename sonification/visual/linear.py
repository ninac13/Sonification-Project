import streamlit as st
from mapper import map_sequence_to_notes
from player import play_sonification
from visual.linear import render_linear

st.title("DNA Sonification & Visualization")

seq = st.text_area("Paste your DNA sequence here", height=150)

if st.button("Play Sonification"):
    notes = map_sequence_to_notes(seq)
    audio_bytes = play_sonification(notes)  # must return raw WAV/MP3 bytes
    st.audio(audio_bytes, format="audio/wav")

if st.button("Show Linear Visual"):
    viz = render_linear(seq)
    st.code(viz)