import numpy as np
from Classes import *
from KL_Algorithm import *

def pitch_cost_consonance(difference):
    '''
    according to consonance
    input: absolute difference of pitch
    return: cost
    '''
    if difference == 0:
        return 0
    if difference == 1:
        return 5.7
    if difference == 2:
        return 5.325
    if difference == 3:
        return 3.675
    if difference == 4:
        return 3.675
    if difference == 5:
        return 2.85
    if difference == 6:
        return 4.65
    else:
        return 3.35

def sub_cost(mode, note1, note2, k=0.2, consider_note_distance=False,
             consider_downbeat=False, downbeat_weight=2, consider_force=False):
    '''
    mode:   1 -> direct pitch + consider consonance
            2 -> pitch difference + not consider consonance
    note:   class Note
    k:      weight of duration
    consider_note_distance: True    ->  pitch difference is cost
                            False   ->  cost is 1 if different
    consider_downbeat:      True    ->  consider downbeat of note by weighing the cost more
    consider_force:         True    ->  consider force
    '''
    if mode == 1: # direct pitch and consider consonance
        if note1 == 'empty':
            cost = pitch_cost_consonance('empty') + k*note2.length
            if consider_downbeat:
                if note2.downbeat:
                    cost = cost * downbeat_weight
                    '''
                else:
                    cost = 0
                    '''
        elif note2 == 'empty':
            cost = pitch_cost_consonance('empty') + k*note1.length
            if consider_downbeat:
                if note1.downbeat:
                    cost = cost * downbeat_weight
                    '''
                else:
                    cost = 0
                    '''
        elif (note1.pitch==note2.pitch and (note1.length - note2.length) < 0.001):
            cost = 0
        else:
            cost = pitch_cost_consonance(abs(note1.pitch-note2.pitch)) + abs(k*(note1.length-note2.length))
            if consider_downbeat:
                if note1.downbeat:
                    cost = cost * downbeat_weight
                if note2.downbeat:
                    cost = cost * downbeat_weight

    if mode == 2: # pitch difference and not consonance
        if note1 == 'empty':
            if consider_note_distance:
                cost_pitch = 1
                # cost_pitch = abs(note2.pitch)
            else:
                cost_pitch = 1
            cost_duration = k * note2.length
            # cost_duration = k
            cost = cost_pitch + cost_duration
            if note2.downbeat and consider_downbeat:
                cost = cost * downbeat_weight
            if consider_force:
                cost = cost * note2.force / 100
        elif note2 == 'empty':
            if consider_note_distance:
                cost_pitch = 1
                # cost_pitch = abs(note1.pitch)
            else:
                cost_pitch = 1
            cost_duration = 0 * note1.length
            # cost_duration = k
            cost = cost_pitch + cost_duration
            if note1.downbeat and consider_downbeat:
                cost = cost * downbeat_weight
            # print(note1, note2, cost)
            if consider_force:
                cost = cost * note1.force / 100
        elif (note1.pitch == note2.pitch) and (abs(note1.length-note2.length) <= 0.001):
            cost = 0
        else:
            if consider_note_distance:
                cost_pitch = abs(note1.pitch - note2.pitch)
            else:
                cost_pitch = 1 - (note1.pitch == note2.pitch)

            cost_duration = k * abs(note1.length - note2.length)
            cost = cost_pitch + cost_duration
            if consider_downbeat:
                if note1.downbeat:
                    cost = cost * downbeat_weight
                if note2.downbeat:
                    cost = cost * downbeat_weight
            if consider_force:
                cost = cost * note1.force / 100 * note2.force / 100
        # print(note1, note2, cost)
    return cost

def edit_distance(piece1, piece2, mode=1, k=0.2, consider_note_distance=False, consider_downbeat=False,
                downbeat_weight=2, consider_force=False):
    '''
    return the edit_distance between piece1 and piece2
    '''
    matrix = [[0 for j in range(len(piece2) + 1)] for i in range(len(piece1) + 1)]

    # initialize
    matrix[0][0] = 0
    for i in range(1, len(piece2) + 1): # change piece2[i-1] to empty
        matrix[0][i] = matrix[0][i - 1] + sub_cost(mode=mode, note1='empty', note2=piece2[i - 1], k=k,
                                                   consider_note_distance=consider_note_distance,
                                                   consider_downbeat=consider_downbeat,
                                                   downbeat_weight=downbeat_weight,
                                                   consider_force=consider_force)
    for j in range(1, len(piece1) + 1): # change piece1[i-1] to empty
        matrix[j][0] = matrix[j - 1][0] + sub_cost(mode=mode, note1=piece1[j - 1], note2='empty', k=k,
                                                   consider_note_distance=consider_note_distance,
                                                   consider_downbeat=consider_downbeat,
                                                   downbeat_weight=downbeat_weight,
                                                   consider_force=consider_force)
    # Dynamic Programming
    for i in range(len(piece1)):
        for j in range(len(piece2)):
            note1, note2 = piece1[i], piece2[j]
            '''
            note1 -> empty + matrix[i][j+1]
            note2 -> empty + matrix[i+1][j]
            note1 -> note2 + matrix[i][j]
            '''
            matrix[i + 1][j + 1] = min([
                matrix[i][j + 1] + sub_cost(mode=mode, note1=note1, note2='empty', k=k,
                                            consider_note_distance=consider_note_distance,
                                            consider_downbeat=consider_downbeat,
                                            downbeat_weight=downbeat_weight, consider_force=consider_force),
                matrix[i + 1][j] + sub_cost(mode=mode, note1='empty', note2=note2, k=k,
                                            consider_note_distance=consider_note_distance,
                                            consider_downbeat=consider_downbeat,
                                            downbeat_weight=downbeat_weight, consider_force=consider_force),
                matrix[i][j] + sub_cost(mode=mode, note1=note1, note2=note2, k=k,
                                        consider_note_distance=consider_note_distance,
                                        consider_downbeat=consider_downbeat,
                                        downbeat_weight=downbeat_weight, consider_force=consider_force)
            ])
    return matrix[-1][-1]

def distance2value(distance, index):
    '''
    input:  distance
    return: similarity
    '''
    if index == 1:
        value = np.log(1 + np.exp(-distance))
    elif index == 2:
        value = 100 - distance
    elif index == 3:
        if distance <= 0.1:
            value = 10
        else:
            value = 1 / distance
    return value

def max_flow_value(music1, music2, mode=1, k=0.2, consider_note_distance=False,
            consider_downbeat=True, downbeat_weight=2, consider_force=False):
    '''
    compute the max-flow value
    '''
    values = []
    match = []
    for i in range(len(music1.pieces_list)):
        for j in range(len(music2.pieces_list)):
            distance = edit_distance(music1.pieces_list[i], music2.pieces_list[j], mode=mode, k=k,
                                consider_note_distance=consider_note_distance,
                                consider_downbeat=consider_downbeat, downbeat_weight=downbeat_weight,
                                consider_force=consider_force)
            '''
            1: log(1+exp(-x))
            2: linear 100 - x
            3: 1 / x
            '''
            value = distance2value(distance, 1) # change distance to similarity
            values.append((i, j, value))
    # compute the max flow value
    max_flow_value, max_flow_connect = run_kuhn_munkres(x_y_values=values)

    # sort in decreasing order
    max_flow_connect = sorted(max_flow_connect, key=lambda d: d[2], reverse=True)
    for i in range(len(max_flow_connect)):
        match.append((music1.pieces_list_original[max_flow_connect[i][0]],
                      music2.pieces_list_original[max_flow_connect[i][1]],
                      max_flow_connect[i][2]))
    # return max_flow_value / min(len(music2.pieces_list), len(music1.pieces_list)), match
    return max_flow_value, match
###########################################
# following methods do not use max flow

def minimum_distance_between_pieces(music1, music2, mode=1, k=0.2, consider_note_distance=False,
            consider_downbeat=True, downbeat_weight=2, consider_force=False):
    '''
    return the minimum distance between pieces of two songs
    '''
    min_dis = 10000
    for i in range(len(music1.pieces_list)):
        for j in range(len(music2.pieces_list)):
            distance = edit_distance(music1.pieces_list[i], music2.pieces_list[j], mode=mode, k=k,
                                consider_note_distance=consider_note_distance,
                                consider_downbeat=consider_downbeat, downbeat_weight=downbeat_weight,
                                consider_force=consider_force)
            if distance < min_dis:
                min_dis = distance
    return min_dis

def average_minimum_distance_between_pieces(music1, music2, mode=1, k=0.2, consider_note_distance=False,
            consider_downbeat=True, downbeat_weight=2, consider_force=False):
    '''
    find average minimum distance for song 1's pieces
    '''
    dis_sum = 0
    for i in range(len(music1.pieces_list)):
        min_dis = 10000
        for j in range(len(music2.pieces_list)):
            distance = edit_distance(music1.pieces_list[i], music2.pieces_list[j], mode=mode, k=k,
                                consider_note_distance=consider_note_distance,
                                consider_downbeat=consider_downbeat, downbeat_weight=downbeat_weight,
                                consider_force=consider_force)
            min_dis = min(min_dis, distance)
        dis_sum += min_dis
    return dis_sum / len(music1.pieces_list)

def three_minimum_distance_between_pieces(music1, music2, mode=1, k=0.2, consider_note_distance=False,
            consider_downbeat=True, downbeat_weight=2, consider_force=False):
    '''
    return sum of three least distance d_i for all song 1's piece 1
    '''
    dis_list = []
    for i in range(len(music1.pieces_list)):
        min_dis = 10000
        for j in range(len(music2.pieces_list)):
            distance = edit_distance(music1.pieces_list[i], music2.pieces_list[j], mode=mode, k=k,
                                consider_note_distance=consider_note_distance,
                                consider_downbeat=consider_downbeat, downbeat_weight=downbeat_weight,
                                consider_force=consider_force)
            min_dis = min(min_dis, distance)
        dis_list.append(min_dis)
    dis_list = sorted(dis_list, reverse=True)
    return dis_list[0] + dis_list[1] + dis_list[2]
