from midiutil import MIDIFile
import random

# Function to add a phrase to the music
def add_phrase(track, channel, notes, start_time, duration, volume):
    time = start_time
    for pitch in notes:
        MyMIDI.addNote(track, channel, pitch, time, duration, volume)
        time += duration
    return time

# Create a MIDI file with one track
MyMIDI = MIDIFile(1)

# Tracks are zero-indexed
track = 0
time = 0  # Start at the beginning
channel = 0
MyMIDI.addTrackName(track, time, "Fetch Theme")
MyMIDI.addTempo(track, time, 120)

# Define the fetch-themed melody
base_notes = [60, 62, 64, 65, 67, 69, 71, 72]  # C Major scale
duration = 1  # 1 beat long
volume = 100  # 0-127, as per the MIDI standard

# Generate the main melody (4 phrases)
for _ in range(4):
    melody = [random.choice(base_notes) for _ in range(8)]
    time = add_phrase(track, channel, melody, time, duration, volume)

# Add a 'fetch' motif - a playful, quick run up and down
fetch_motif = [72, 76, 79, 76, 72]  # C, E, G, E, C
motif_duration = 0.25
time = add_phrase(track, channel, fetch_motif, time, motif_duration, volume)

# Repeat the main melody with variations (4 phrases)
for _ in range(4):
    melody_variation = [note + random.choice([-1, 0, 1]) for note in melody]  # Slight variation
    time = add_phrase(track, channel, melody_variation, time, duration, volume)

# Repeat the 'fetch' motif
time = add_phrase(track, channel, fetch_motif, time, motif_duration, volume)

# Add a bridge section to provide some contrast (2 phrases)
bridge_notes = [67, 69, 71, 72, 74, 76, 78, 79]  # G Major scale
for _ in range(2):
    bridge_melody = [random.choice(bridge_notes) for _ in range(8)]
    time = add_phrase(track, channel, bridge_melody, time, duration, volume)

# Return to the main melody for the final section (4 phrases)
for _ in range(4):
    final_melody = [random.choice(base_notes) for _ in range(8)]
    time = add_phrase(track, channel, final_melody, time, duration, volume)

# Ensure that the last note leads back to the first note of the piece
MyMIDI.addNote(track, channel, base_notes[0], time, duration, volume)

# Save the MIDI file
with open("fetch_theme_long.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)

