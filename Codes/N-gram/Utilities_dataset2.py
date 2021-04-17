from Classes import *
import numpy as np
import os

data_path = '../../dataset2/'

def extract_n_grams(n, music):
    gram_dic = {}
    music.pitch_difference()
    notes_list = music.notes_list[1:]
    idx = 0
    while (idx <= len(notes_list)-n):
        pitch_list = []
        for i in range(n):
            pitch_list.append(notes_list[idx+i].pitch)
        idx += 1

        pitch_list = tuple(pitch_list)
        try:
            gram_dic[pitch_list] += 1
        except:
            gram_dic[pitch_list] = 1
    music.TF = {}
    for key in gram_dic.keys():
        music.TF[key] = gram_dic[key] / idx
    music.gram_dic = gram_dic
    return gram_dic

def Ukkonen(n, music1, music2):
    n1 = 0
    n2 = 0
    gram_dic1 = extract_n_grams(n, music1)
    gram_dic2 = extract_n_grams(n, music2)
    for key in gram_dic1.keys():
        n1 += gram_dic1[key]
        if key not in gram_dic2.keys():
            gram_dic2[key] = 0

    for key in gram_dic2.keys():
        n2 += gram_dic2[key]
        if key not in gram_dic1.keys():
            gram_dic1[key] = 0
    sum = 0
    for key in gram_dic1.keys():
        sum += abs(gram_dic1[key] - gram_dic2[key])
    return 1 - sum / (n1 + n2)

def SumCommon(n, music1, music2):
    n1 = 0
    n2 = 0
    sum = 0
    gram_dic1 = extract_n_grams(n, music1)
    gram_dic2 = extract_n_grams(n, music2)
    for key in gram_dic1.keys():
        n1 += gram_dic1[key]
        if key in gram_dic2.keys():
            sum += (gram_dic1[key] + gram_dic2[key])
    for key in gram_dic2.keys():
        n2 += gram_dic2[key]
    return sum / (n1 + n2)

# def TF_IDF_correlation(n, music1, music2):


def Ukkonen_Wrapper(n):
    files = os.listdir(data_path)
    file_num = len(files)
    musics = []
    for file in files:
        music = Music(data_path + file)
        musics.append(music)

    accuracy = 0
    avg_index = 0
    for i in range(0, file_num):
        res = {}
        for j in range(0, file_num): # similarity of music i and music j
            if (i == j) or (files[i][3:] == files[j][3:]):
                continue
            res[files[j]] = Ukkonen(n, musics[i], musics[j])

        # sort in decreasing order
        res = sorted(res.items(), key=lambda d: d[1], reverse=True)
        print('name:\t{}-------------------------------------------------------'.format(files[i]))

        index = 0
        for key, value in res:
            print("{}:\t{}".format(key, value))
            index += 1
            if key[:2] == files[i][:2]: # ground truth
                print(index)
                avg_index += index
                if (index == 1):
                    accuracy += 1

    print("accuracy:{}\taverage index:{}".format(accuracy / file_num, avg_index / file_num))


def SumCommon_Wrapper(n):
# accuracy:0.34285714285714286	average index:5.4
    files = os.listdir(data_path)
    file_num = len(files)
    musics = []
    for file in files:
        music = Music(data_path + file)
        musics.append(music)

    accuracy = 0
    avg_index = 0
    for i in range(0, file_num):
        res = {}
        for j in range(0, file_num): # similarity of music i and music j
            if (i == j) or (files[i][3:] == files[j][3:]):
                continue
            res[files[j]] = SumCommon(n, musics[i], musics[j])

        # sort in decreasing order
        res = sorted(res.items(), key=lambda d: d[1], reverse=True)
        print('name:\t{}-------------------------------------------------------'.format(files[i]))

        index = 0
        for key, value in res:
            print("{}:\t{}".format(key, value))
            index += 1
            if key[:2] == files[i][:2]: # ground truth
                print(index)
                avg_index += index
                if (index == 1):
                    accuracy += 1

    print("accuracy:{}\taverage index:{}".format(accuracy / file_num, avg_index / file_num))

def TF_IDF_correlation(n):
# accuracy:0.2857142857142857	average index:6.8
    files = os.listdir(data_path)
    file_num = len(files)
    musics = []
    gram_num_dic = {} # gram_num_dic[key] denotes the number of songs contain key

    for file in files:
        music = Music(data_path + file)
        gram_dic = extract_n_grams(n, music)
        # update gram_num_dic
        for key in gram_dic.keys():
            try:
                gram_num_dic[key] += 1
            except:
                gram_num_dic[key] = 1
        musics.append(music)

    # calculate IDF
    IDF = {}
    for key in gram_num_dic.keys():
        IDF[key] = np.log(file_num / gram_num_dic[key])

    # calculate TFIDF
    for music in musics:
        music.TFIDF = {}
        for key in IDF.keys():
            if key not in music.TF.keys():
                music.TF[key] = 0
            music.TFIDF[key] = music.TF[key] * IDF[key]

    accuracy = 0
    avg_index = 0
    for i in range(0, file_num):
        # if ('10') not in files[i]:
        #     continue
        res = {}
        for j in range(0, file_num): # similarity of music i and music j
            if (i == j) or (files[i][3:] == files[j][3:]):
                continue
            up = 0.0
            down1 = 0.0
            down2 = 0.0
            for key in musics[i].TFIDF.keys():
                if musics[i].TF[key] != 0 or musics[j].TF[key] != 0 :
                    up += musics[i].TFIDF[key] * musics[j].TFIDF[key]
                    down1 += musics[i].TFIDF[key] ** 2
                    down2 += musics[j].TFIDF[key] ** 2
            res[files[j]] = up / np.sqrt(down1 * down2)

        # sort in decreasing order
        res = sorted(res.items(), key=lambda d: d[1], reverse=True)
        print('name:\t{}-------------------------------------------------------'.format(files[i]))
        # accuracy:0.3142857142857143	average index:6.2
        index = 0
        for key, value in res:
            print("{}:\t{}".format(key, value))
            index += 1
            if key[:2] == files[i][:2]: # ground truth
                print(index)
                avg_index += index
                if (index == 1):
                    accuracy += 1

    print("accuracy:{}\taverage index:{}".format(accuracy / file_num, avg_index / file_num))

def TF_IDF_common(n):
# accuracy:0.08571428571428572	average index:17.257142857142856
    files = os.listdir(data_path)
    file_num = len(files)
    musics = []
    gram_num_dic = {} # gram_num_dic[key] denotes the number of songs contain key

    for file in files:
        music = Music(data_path + file)
        gram_dic = extract_n_grams(n, music)
        # update gram_num_dic
        for key in gram_dic.keys():
            try:
                gram_num_dic[key] += 1
            except:
                gram_num_dic[key] = 1
        musics.append(music)
    # calculate IDF
    IDF = {}
    for key in gram_num_dic.keys():
        IDF[key] = np.log(file_num / gram_num_dic[key])
    # calculate TFIDF
    for music in musics:
        music.TFIDF = {}
        for key in IDF.keys():
            if key not in music.TF.keys():
                music.TF[key] = 0
            music.TFIDF[key] = music.TF[key] * IDF[key]

    accuracy = 0
    avg_index = 0
    for i in range(0, file_num):
        # if ('10' not in files[i]):
        #     continue
        res = {}
        for j in range(0, file_num): # similarity of music i and music j
            if (i == j) or (files[i][3:] == files[j][3:]):
                continue
            up = 0.0
            down = 1e-10
            for key in musics[i].TFIDF.keys():
                if musics[i].TF[key] != 0 and musics[j].TF[key] != 0 :
                    print(key)
                    up += np.sqrt(IDF[key] * np.sqrt(musics[i].TF[key] * musics[j].TF[key]))
                    down += IDF[key]
            res[files[j]] = up / down

        # sort in decreasing order
        res = sorted(res.items(), key=lambda d: d[1], reverse=True)
        print('name:\t{}-------------------------------------------------------'.format(files[i]))

        index = 0
        for key, value in res:
            print("{}:\t{}".format(key, value))
            index += 1
            if key[:2] == files[i][:2]: # ground truth
                print(index)
                avg_index += index
                if (index == 1):
                    accuracy += 1

    print("accuracy:{}\taverage index:{}".format(accuracy / file_num, avg_index / file_num))

def Tversky_equal(n):
    files = os.listdir(data_path)
    file_num = len(files)
    musics = []
    gram_num_dic = {}  # gram_num_dic[key] denotes the number of songs contain key

    for file in files:
        music = Music(data_path + file)
        gram_dic = extract_n_grams(n, music)
        # update gram_num_dic
        for key in gram_dic.keys():
            try:
                gram_num_dic[key] += 1
            except:
                gram_num_dic[key] = 1
        musics.append(music)
    # calculate IDF
    IDF = {}
    for key in gram_num_dic.keys():
        IDF[key] = np.log(file_num / gram_num_dic[key])
    # calculate TFIDF
    for music in musics:
        music.TFIDF = {}
        for key in IDF.keys():
            if key not in music.TF.keys():
                music.TF[key] = 0
            music.TFIDF[key] = music.TF[key] * IDF[key]

    accuracy = 0
    avg_index = 0
    for i in range(0, file_num):
        res = {}
        for j in range(0, file_num):  # similarity of music i and music j
            if (i == j) or (files[i][3:] == files[j][3:]):
                continue
            sum1 = 0.0
            sum2 = 0.0
            sum3 = 0.0
            for key in musics[i].TFIDF.keys():
                if musics[i].TF[key] != 0 and musics[j].TF[key] != 0:
                    sum1 += IDF[key]
                elif musics[i].TF[key] != 0 and musics[j].TF[key] == 0:
                    sum2 += IDF[key]
                elif musics[i].TF[key] == 0 and musics[j].TF[key] != 0:
                    sum3 += IDF[key]
            res[files[j]] = sum1 / (sum1 + sum2 + sum3)

        # sort in decreasing order
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

    print("accuracy:{}\taverage index:{}".format(accuracy / file_num, avg_index / file_num))

def Tversky_weighted(n):
    files = os.listdir(data_path)
    file_num = len(files)
    musics = []
    gram_num_dic = {}  # gram_num_dic[key] denotes the number of songs contain key

    for file in files:
        music = Music(data_path + file)
        gram_dic = extract_n_grams(n, music)
        # update gram_num_dic
        for key in gram_dic.keys():
            try:
                gram_num_dic[key] += 1
            except:
                gram_num_dic[key] = 1
        musics.append(music)
    # calculate IDF
    IDF = {}
    for key in gram_num_dic.keys():
        IDF[key] = np.log(file_num / gram_num_dic[key])
    # calculate TFIDF
    for music in musics:
        music.TFIDF = {}
        for key in IDF.keys():
            if key not in music.TF.keys():
                music.TF[key] = 0
            music.TFIDF[key] = music.TF[key] * IDF[key]

    accuracy = 0
    avg_index = 0
    for i in range(0, file_num):
        res = {}
        for j in range(0, file_num):  # similarity of music i and music j
            if (i == j) or (files[i][3:] == files[j][3:]):
                continue

            alpha_up = 0.0
            alpha_down = 0.0
            beta_up = 0.0
            beta_down = 0.0
            for key in musics[i].TF.keys():
                if (musics[i].TF[key] != 0) and (musics[j].TF[key] != 0):
                    alpha_up += musics[i].TF[key]
                    beta_up += musics[j].TF[key]
                alpha_down += musics[i].TF[key]
                beta_down += musics[j].TF[key]
            alpha = alpha_up / alpha_down
            beta = beta_up / beta_down
            # print(alpha, beta)
            sum1 = 1e-10
            sum2 = 0.0
            sum3 = 0.0
            for key in musics[i].TFIDF.keys():
                if musics[i].TF[key] != 0 and musics[j].TF[key] != 0:
                    sum1 += IDF[key]
                elif musics[i].TF[key] != 0 and musics[j].TF[key] == 0:
                    sum2 += IDF[key]
                elif musics[i].TF[key] == 0 and musics[j].TF[key] != 0:
                    sum3 += IDF[key]
            res[files[j]] = sum1 / (sum1 + alpha*sum2 + beta*sum3)

            # sort in decreasing order
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

    print("accuracy:{}\taverage index:{}".format(accuracy / file_num, avg_index / file_num))
def main():
    TF_IDF_common(3)      # accuracy:0.4634146341463415	average index:9.707317073170731
    TF_IDF_correlation(3) # accuracy:0.5121951219512195	average index:9.560975609756097
    SumCommon_Wrapper(4)  # accuracy:0.6585365853658537	average index:5.926829268292683
    Ukkonen_Wrapper(4)    # accuracy:0.7073170731707317	average index:5.853658536585366
    Tversky_equal(3)        # accuracy:0.5121951219512195	average index:9.560975609756097
    Tversky_weighted(3)     # accuracy:0.36585365853658536	average index:12.560975609756097
main()