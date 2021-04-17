import numpy as np
from Classes import *
from Utilities import *
import os
data_path = '../../dataset2/'
'''
    overlap_rate:   overlap rate of pieces
    piece_len:      length of piece
    k:      weight of duration
    mode:   1 -> direct pitch + consider consonance
            2 -> pitch difference + not consider consonance
    pitch_operation:    1->pitch difference 2->pitch mode 12
    duration_operation: 1->duration ratio   2->duration difference 
    consider_note_distance: True    ->  pitch difference is cost
                            False   ->  cost is 1 if different
    consider_downbeat:      True    ->  consider downbeat of note by weighing the cost more
    consider_force:         True    ->  consider force
    '''
overlap_rate = 0.8
piece_len = 5
k = 0
mode = 2 # 1:(direct pitch) consider consonance, 2:not consider consonance
pitch_operation = 1 # 1:difference, 2:direct
duration_operation = 1 # 1: ratio 2: difference
consider_note_distance = False
consider_downbeat = True
downbeat_weight = 1.2
consider_force = False
'''
overlap_rate=0.8	piece_len=5	k=0	mode=2
pitch_operation=1	duration_operation=1	consider_note_distance=True
consider_downbeat=False	downbeat_weight=1.2	consider_force=False
accuracy:0.7560975609756098	average index:4.048780487804878
'''
def brutal():
    files = os.listdir(data_path)
    file_num = len(files)
    musics = []
    for file in files:
        music = Music(data_path + file)
        music.execute_change(pitch_operation=pitch_operation, duration_operation=duration_operation,
                        piece_len=piece_len, overlap_rate=overlap_rate)
        musics.append(music)
    accuracy = 0
    avg_index = 0

    for i in range(file_num):
        res = {}
        for j in range(file_num):
            if (i == j) or (files[i][3:] == files[j][3:]):
                continue
            '''
            three functions for brutal:
            average_minimum_distance_between_pieces()
            three_minimum_distance_between_pieces()
            minimum_distance_between_pieces()
            '''
            distance = average_minimum_distance_between_pieces(musics[i], musics[j], mode=mode, k=k,
                                    consider_note_distance=consider_note_distance, consider_downbeat=consider_downbeat,
                                    downbeat_weight=downbeat_weight,consider_force=consider_force)
            res[files[j]] = distance
        res = sorted(res.items(), key=lambda d: d[1], reverse=False)
        print('name:\t{}-------------------------------------------------------'.format(files[i]))

        index = 0
        for key, value in res:
            print("{}:\t{}".format(key, value))
            index += 1
            if key[:2] == files[i][:2]:  # ground truth
                print(index)
                avg_index += index
                if (index == 1):
                    accuracy += 1
                break

    print("accuracy:{}\taverage index:{}".format(accuracy / file_num, avg_index / file_num))

def edit_distance_optimized():
    files = os.listdir(data_path)
    file_num = len(files)
    musics = []
    for file in files:
        music = Music(data_path + file)
        music.execute_change(pitch_operation=pitch_operation, duration_operation=duration_operation,
                        piece_len=piece_len, overlap_rate=overlap_rate)
        musics.append(music)
    accuracy = 0
    avg_index = 0

    for i in range(file_num):
        # if ('case19' not in files[i]):
        #     continue
        res = {}
        # if ("case24" not in files[i]):
        #     continue
        for j in range(file_num):
            if (i == j) or (files[i][3:] == files[j][3:]):
                continue
            '''
            three functions for brutal:
            average_minimum_distance_between_pieces()
            three_minimum_distance_between_pieces()
            minimum_distance_between_pieces()
            '''
            distance, _ = max_flow_value(musics[i], musics[j], mode=mode, k=k,
                                    consider_note_distance=consider_note_distance, consider_downbeat=consider_downbeat,
                                    downbeat_weight=downbeat_weight, consider_force=consider_force)
            res[files[j]] = distance
        res = sorted(res.items(), key=lambda d: d[1], reverse=True)
        print('name:\t{}-------------------------------------------------------'.format(files[i]))

        index = 0
        for key, value in res:
            print("{}:\t{}".format(key, value))
            index += 1
            if key[:2] == files[i][:2]:  # ground truth
                print(index)
                avg_index += index
                if (index == 1):
                    accuracy += 1
    print("overlap_rate={}\tpiece_len={}\tk={}\tmode={}".format(overlap_rate, piece_len, k, mode))
    print("pitch_operation={}\tduration_operation={}\tconsider_note_distance={}".format(pitch_operation, duration_operation, consider_note_distance))
    print("consider_downbeat={}\tdownbeat_weight={}\tconsider_force={}".format(consider_downbeat, downbeat_weight, consider_force))
    print("accuracy:{}\taverage index:{}".format(accuracy / file_num, avg_index / file_num))
    return accuracy / file_num, avg_index / file_num
def main():
    edit_distance_optimized()
main()



