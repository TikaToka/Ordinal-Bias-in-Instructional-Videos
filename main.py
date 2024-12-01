import numpy as np
import os
import argparse
from tqdm import tqdm
import random
import shutil
from distutils.dir_util import copy_tree


parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str)
parser.add_argument('--mode', type=str)
parser.add_argument('--seed', type=int, default=42)
parser.add_argument('--name', type=str, default='')
print(parser.parse_args().dataset)
print(parser.parse_args().mode)
print(parser.parse_args().seed)
print(parser.parse_args().name)

random.seed(parser.parse_args().seed)

dataset = parser.parse_args().dataset
vidpath = './data/' + dataset
outpath = './data_' + parser.parse_args().name + '/' + dataset


file_names = [s.split(".")[0] for s in os.listdir(
    vidpath + '/features') if s.endswith(".npy")]

try:
    os.makedirs(outpath)
except OSError:
    pass
shutil.copy(vidpath + '/mapping.txt', outpath + '/' + 'mapping.txt')
copy_tree(vidpath + '/splits', outpath + '/splits')

for s in tqdm(file_names):
    v = np.load(vidpath + '/features/' + s + ".npy")
    l = []
    f = open(vidpath + '/groundTruth/' + s + ".txt")
    while True:
        line = f.readline()
        if not line:
            break
        l.append(line.rstrip())
    f.close()

    label_idx = []

    count = 1
    for i in range(len(l)-1):
        if l[i] == l[i+1]:
            if i == len(l)-2:
                count += 1
                label_idx.append((l[i], count))
            else:
                count += 1
        else:
            if i == len(l)-2:
                label_idx.append((l[i], count))
                label_idx.append((l[i+1], 1))
            else:
                label_idx.append((l[i], count))
                count = 1
            
    action_units = []
    num = 0
    for i in label_idx:
        frames = []
        for j in range(i[1]):
            frames.append(v[:, num])
            num += 1
        action_units.append(frames)
        
    if parser.parse_args().mode == 'blank':
        for ac in range(len(action_units)):
            if random.randint(1, 100) <= 15:
                if dataset == 'gtea':
                    action_units[ac] = np.zeros(
                        np.shape(action_units[ac])).tolist()
                    label_idx[ac] = ('background', label_idx[ac][1])
                elif dataset == 'breakfast':
                    action_units[ac] = np.zeros(
                        np.shape(action_units[ac])).tolist()
                    label_idx[ac] = ('SIL', label_idx[ac][1])
                # else:  # 50salads
                #     print("50salads")
                #     action_units[ac] = np.zeros(
                #         np.shape(action_units[ac])).tolist()
                #     break

    # if parser.parse_args().mode == 'reverse':
    #     print("reverse")
    #     action_units.reverse()
    #     label_idx.reverse()

    # elif parser.parse_args().mode == 'one':
    #     print("one")
    #     if len(action_units) >= 3:
    #         action_units[1], action_units[2] = action_units[2], action_units[1]
    #         label_idx[1], label_idx[2] = label_idx[2], label_idx[1]
    #     else:
    #         action_units[0], action_units[1] = action_units[1], action_units[0]
    #         label_idx[0], label_idx[1] = label_idx[1], label_idx[0]

    # elif parser.parse_args().mode == 'swap':
    #     print("swap")
    #     idx = random.randint(0, len(action_units)-2)
    #     action_units[idx], action_units[idx +
    #                                     1] = action_units[idx+1], action_units[idx]
    #     label_idx[idx], label_idx[idx+1] = label_idx[idx+1], label_idx[idx]
        
    # elif parser.parse_args().mode == 'blank15':
    #     for ac in range(len(action_units)):
    #         if random.randint(1, 100) <= 15:
    #             if dataset == 'gtea':
    #                 action_units[ac] = np.zeros(
    #                     np.shape(action_units[ac])).tolist()
    #                 label_idx[ac] = ('background', label_idx[ac][1])
    #             elif dataset == 'breakfast':
    #                 action_units[ac] = np.zeros(
    #                     np.shape(action_units[ac])).tolist()

    # elif parser.parse_args().mode == 'blank50':
    #     for ac in range(len(action_units)):
    #         if random.randint(1, 100) <= 50:
    #             if dataset == 'gtea':
    #                 action_units[ac] = np.zeros(
    #                     np.shape(action_units[ac])).tolist()
    #                 label_idx[ac] = ('background', label_idx[ac][1])
    #             elif dataset == 'breakfast':
    #                 action_units[ac] = np.zeros(
    #                     np.shape(action_units[ac])).tolist()
                    
    # elif parser.parse_args().mode == 'blank100':
    #     si = np.shape(np.array(action_units))
    #     for ac in range(len(action_units)):
    #         if random.randint(1, 100) <= 100:
    #             if dataset == 'gtea':
    #                 action_units[ac] = np.zeros(
    #                     np.shape(action_units[ac])).tolist()
    #                 label_idx[ac] = ('background', label_idx[ac][1])
    #             elif dataset == 'breakfast':
    #                 action_units[ac] = np.zeros(
    #                     np.shape(action_units[ac])).tolist()
    #                 label_idx[ac] = ('SIL', label_idx[ac][1])
    #     assert (si == np.shape(np.array(action_units)))

    elif parser.parse_args().mode == 'mask':
        if dataset == 'gtea':
            lists = {"close": "put"}
            temp = 'background'
        elif dataset == 'breakfast':
            print("breakfast")
            lists = {"pour_dough2pan": "fry_pancake"}
            temp = 'SIL'
        else:
            for ac in range(len(action_units)-1):
                if label_idx[ac][0] in lists.keys():
                    print("mask")
                    action_units[ac+1] = np.zeros(
                        np.shape(action_units[ac+1])).tolist()
                    label_idx[ac+1] = (temp, label_idx[ac+1][1])

    # # SWAP RANDOM 2
    # elif parser.parse_args().mode == 'random':
    #     print("random")
    #     rn = random.sample(range(0, len(action_units)), 2)
    #     action_units[rn[0]], action_units[rn[1]
    #                                       ] = action_units[rn[1]], action_units[rn[0]]
    #     label_idx[rn[0]], label_idx[rn[1]] = label_idx[rn[1]], label_idx[rn[0]]

    elif parser.parse_args().mode == 'all':
        print("all")
        idx = list(range(len(action_units)))
        random.shuffle(idx)
        action_units = [action_units[i] for i in idx]
        label_idx = [label_idx[i] for i in idx]

    # elif parser.parse_args().mode == 'alleasy':
    #     mid = len(action_units) //2
    #     action_units = action_units[mid:] + action_units[:mid]
    #     mid = len(label_idx) //2
    #     label_idx = label_idx[mid:] + label_idx[:mid]
        
    # elif parser.parse_args().mode == 'rand':
    #     if dataset == 'gtea':
    #         lists = {"put": "take"}
    #     elif dataset == 'breakfast':
    #         lists = {"pour_dough2pan": "fry_pancake"}
    #     else:
    #         lists = {"cut_tomato": "place_tomato_into_bowl"}
    #     for ac in range(len(action_units)-1):
    #         if label_idx[ac][0] in lists.keys():
    #             rn = random.randint(0, len(action_units)-1)
    #             action_units[ac+1], action_units[rn
    #                                             ] = action_units[rn], action_units[ac+1]
    #             label_idx[ac+1], label_idx[rn] = label_idx[rn], label_idx[ac+1]

    # elif parser.parse_args().mode == 'blank_set':
    #     print("blank_new")
    #     if dataset == 'gtea':
    #         lists = {'take': 'background',
    #                  "close": "put", "open": "background"}
    #         lab = 'background'
    #     elif dataset == '50salads':
    #         continue
    #     else:
    #         lists = {"pour_dough2pan": "fry_pancake", "put_egg2plate": "SIL",
    #                  "cut_orange": "squeeze_orange", "put_bunTogether": "SIL"}
    #         lab = 'SIL'
    #     for idx in range(len(label_idx)-1):
    #         if label_idx[idx] in lists.keys():
    #             action_units[idx +
    #                          1] = np.zeros(np.shape(action_units[idx+1])).tolist()
    #             label_idx[idx+1] = (lab, label_idx[idx+1][1])
    else:
        print("no mode")
        break

    try:
        os.makedirs(outpath + '/features')
    except OSError:
        if not os.path.isdir(outpath + '/features'):
            raise

    vout = np.zeros(v.shape)
    num = 0
    for i in action_units:
        for j in range(len(i)):
            vout[:, num] = np.array(i[j])
            num += 1

    np.save(outpath + '/features/' + s + ".npy", vout)

    # print(v[:,0])
    # print(vout[:,-label_idx[-1][1]])
    # print(action_units[-1][0])
    # print((v[:,0]==vout[:,-label_idx[-1][1]]).all())

    try:
        os.makedirs(outpath + '/groundTruth')
    except OSError:
        if not os.path.isdir(outpath + '/groundTruth'):
            raise

    f = open(outpath + '/groundTruth/' + s + ".txt", 'w')
    for i in label_idx:
        for j in range(i[1]):
            f.write(i[0] + '\n')
    f.close()
