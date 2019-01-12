from mido import MidiFile
import mido
import time
import numpy as np
from datastructures.base_structures import NoteTransitionDictionary, ProbabilityMatrix, NoteTransitionMatrix, NoteTransition


#creates MidiFile objects from midi files
bb = MidiFile("Parker,_Charlie_-_Billie's_Bounce (1).mid")
bfa = MidiFile("Parker,_Charlie_-_Blues_For_Alice.mid")
c = MidiFile("Parker,_Charlie_-_Cheryl.mid")
dl = MidiFile("Parker,_Charlie_-_Donna_Lee.mid")
o = MidiFile("Parker,_Charlie_-_Ornithology.mid")
pm = MidiFile("Parker,_Charlie_-_Parker's_Mood.mid")
mls = MidiFile("My_Little_Suede_Shoes.mid")
ntt = MidiFile("Nows_The_Time.mid")

#creates lists to store MidiFile objects based on the interesting channel
midi_songs_channel_zero = []
midi_songs_channel_other = []

#load MidiFile objects into appropriate lists
midi_songs_channel_zero.append(bb)
midi_songs_channel_zero.append(bfa)
midi_songs_channel_zero.append(c)
midi_songs_channel_zero.append(dl)
midi_songs_channel_zero.append(pm)
midi_songs_channel_zero.append(mls)
midi_songs_channel_zero.append(ntt)

midi_songs_channel_other.append(o)

#for testing which tracks are contained in the midi file
for track in ntt.tracks:
    #print(track)
    pass

#for testing which channels the messages are on
for message in ntt:
    #print(message)
    pass

#for testing which is the interesting channel
n = []
for message in ntt:
    if message.type == "note_on" and  message.channel == 0 and message.velocity != 0:
        n.append(message.note)
#print(n)

#store the list of notes on interesting channel from each song into a list
all_notes = []
for song in midi_songs_channel_zero:
    notes = []
    for message in song:
        if message.type == "note_on" and message.channel == 0 and message.velocity != 0:
             notes.append(message.note)
    all_notes.append(notes)

for song in midi_songs_channel_other:
    notes = []
    for message in song:
        if message.type == "note_on" and message.channel == 1 and message.velocity != 0:
            notes.append(message.note)
    all_notes.append(notes)

#store each note transition as a tuple into a list
transitions = []
for notes in all_notes:
    for i in range(len(notes)-1):
        transition = NoteTransition(notes[i],notes[i+1])
        transitions.append(transition)

#create markov model data structures
nd = NoteTransitionDictionary()
pm = ProbabilityMatrix()
ntm = NoteTransitionMatrix()

#feed the data from the note transitions into the model
nd.add_note_transitions(transitions)
pm.update(nd)

#print the models
#print(nd.__repr__())
#print(pm.__repr__())
#print(ntm.__repr__())

#check which rows have non-zero rows
x = 0
while x < pm.get_size():
    row = pm.get_matrix()[x]
    if sum(row) != 0:
        x
    x += 1

#generate notes based on the model
starting_note = 60
generated_notes = [starting_note]
current_note = starting_note
amount = 120

while amount > 0:
    next_transition = np.random.choice(ntm.get_matrix()[current_note], replace=True, p=pm.get_matrix()[current_note])
    end = next_transition.get_end()
    current_note = end
    generated_notes.append(current_note)
    amount -= 1

#make a list of messages from the generated notes
msgs = []
for note in generated_notes:
    on_msg = mido.Message("note_on", note=note)
    off_msg = mido.Message("note_off", note=note)
    msgs.append(on_msg)
    msgs.append(off_msg)

#send messages to the outport
with mido.open_output('Microsoft GS Wavetable Synth 0') as outport:
    i = 0
    while i < (len(msgs)-1):
        outport.send(msgs[i])
        time.sleep(0.05)
        outport.send(msgs[i+1])
        i += 1








