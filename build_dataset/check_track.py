import pretty_midi
import numpy as np

'''
Note class: represent note, including:
    1. the note pitch
    2. the note duration
    3. downbeat
    4. intensity of note sound
'''


class Note:
    def __init__(self):
        self.pitch = 0
        self.length = 0
        self.downbeat = False
        self.force = 0


'''
Midi2Numpy: tool to convert midi file to numpy list of Note
    input_path: the path of the input midi file
    track_index: the index of the melody track of midi
    output_path: the path to save the numpy array
'''


def Midi2Numpy(input_path, output_path, track_index):
    midi_data = pretty_midi.PrettyMIDI(input_path)
    notes = midi_data.instruments[track_index].notes
    downbeats = midi_data.get_downbeats()

    dataset = []

    for n in notes:
        note = Note()
        for i in downbeats:
            '''
            the downbeat locates in this note's duration
            we see the note as downbeat
            '''
            if n.start <= i < n.end:
                note.downbeat = True
        note.pitch = n.pitch
        note.length = n.end - n.start
        note.force = n.velocity
        dataset.append(note)
    np.save(output_path, dataset)


path = 'plag/23_ma este meg.mid'

test = pretty_midi.PrettyMIDI()
midi_data = pretty_midi.PrettyMIDI(path)
# decide the track index
track_index = 0
notes = midi_data.instruments[track_index]
test.instruments.append(notes)
test.write('test.mid')
test.write("newdata" + path[4:])
