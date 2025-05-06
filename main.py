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
        
    if parser.parse_args().mode == 'blank': # MLM style masking
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

    elif parser.parse_args().mode == 'mask': # Action Masking
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

    elif parser.parse_args().mode == 'all': # Sequence Shuffling
        print("all")
        idx = list(range(len(action_units)))
        random.shuffle(idx)
        action_units = [action_units[i] for i in idx]
        label_idx = [label_idx[i] for i in idx]

        
    elif parser.parse_args().mode == 'rand': # Limited Sequence Shuffling
        if dataset == 'gtea':
            lists = {"put": "take"}
        elif dataset == 'breakfast':
            lists = {"pour_dough2pan": "fry_pancake"}
        else:
            lists = {"cut_tomato": "place_tomato_into_bowl"}
        for ac in range(len(action_units)-1):
            if label_idx[ac][0] in lists.keys():
                rn = random.randint(0, len(action_units)-1)
                action_units[ac+1], action_units[rn
                                                ] = action_units[rn], action_units[ac+1]
                label_idx[ac+1], label_idx[rn] = label_idx[rn], label_idx[ac+1]

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
