import numpy as np
import copy

class Note:
    def __init__(self):
        self.pitch = 0          # pitch
        self.length = 0         # length of pitch
        self.downbeat = False   # whether downbeat or not
        self.force = 0          # note force

class Music:
    def __init__(self, path):
        '''
        :param name: address of the music
        '''
        if path is None:
            return
        self.name = path
        notes_list = np.load(path, allow_pickle=True)
        self.original_notes_list = copy.deepcopy(notes_list)
        self.notes_list = copy.deepcopy(notes_list)

    def pitch_difference(self):
        '''
        change self.notes_list to pitch-difference sequence
        '''
        self.notes_list[0].pitch = 0
        for i in range(1, len(self.original_notes_list)):
            self.notes_list[i].pitch = self.original_notes_list[i].pitch - self.original_notes_list[i-1].pitch

    def pitch_direct(self):
        '''
        change self.notes_list to mod 12 sequence
        '''
        for i in range(0, len(self.original_notes_list)):
            self.notes_list[i].pitch = self.original_notes_list[i].pitch % 12

    def duration_ratio(self):
        '''
        change self.notes_list to duration-ratio sequence
        '''
        self.notes_list[0].length = 1
        for i in range(1, len(self.original_notes_list)):
            self.notes_list[i].length = self.original_notes_list[i].length / self.original_notes_list[i-1].length

    def duration_difference(self):
        '''
        change self.notes_list to duration-difference sequence
        '''
        self.notes_list[0].length = 0
        for i in range(1, len(self.original_notes_list)):
            self.notes_list[i].length = self.original_notes_list[i].length - self.original_notes_list[i - 1].length

    def cut_into_pieces(self, piece_len=6, overlap_rate=0.5):
        '''
        cut the self.notes_list into list of pieces
        cut self.notes_list into different pieces
        piece_len: length(note) of each piece
        overlap_rate: overlap rate of different pieces
        '''
        self.piece_len = piece_len
        self.overlap_rate = overlap_rate
        pieces_list = []
        pieces_list_original = []
        overlap = int(piece_len * overlap_rate) # overlap length
        stride = piece_len - overlap # stride of length
        idx = 0
        while(idx < len(self.notes_list)):
            if idx + piece_len <= len(self.notes_list):
                pieces_list.append(self.notes_list[idx:idx+piece_len])
                pieces_list_original.append(self.original_notes_list[idx:idx+piece_len])
            else:
                pieces_list.append(self.notes_list[idx:])
                pieces_list_original.append(self.original_notes_list[idx:])
            idx += stride
        self.pieces_list = pieces_list
        self.pieces_list_original = pieces_list_original


    def execute_change(self, pitch_operation, duration_operation, piece_len=6, overlap_rate=0.5):
        '''
        pitch_operation:    1->pitch difference 2->pitch mode 12
        duration_operation: 1->duration ratio   2->duration difference
        piece_len: length of piece
        overlap_rate: overlap between different pieces
        '''

        if pitch_operation == 1:
            self.pitch_difference()
        elif pitch_operation == 2:
            self.pitch_direct()

        if duration_operation == 1:
            self.duration_ratio()
        elif duration_operation == 2:
            self.duration_difference()

        self.cut_into_pieces(piece_len, overlap_rate)