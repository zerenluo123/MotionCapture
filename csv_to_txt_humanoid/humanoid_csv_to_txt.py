import pandas as pd
import numpy as np

# determine the mocap and txt name according to dict (dog_clips_info.txt)
mocap_name = '69_13' + '_worldpos'
txt_name = '69_13_turn_in_place' + '_joint_pos'

# read mocap data from csv
pos_df = pd.read_csv("csv/" + mocap_name + '.csv')
pos_csv = np.array(pos_df)
pos_csv = pos_csv[:, 1:] # remove time column

# [cm] to [m]
pos_csv = pos_csv * 0.01

# minus pos init offset
pos_csv_init = pos_csv[0, 0:3].copy()
pos_csv_init[1] = 0
print("pos init offset: ", pos_csv_init)

pos_csv = pos_csv.reshape(pos_csv.shape[0], -1, 3)

for i in range(pos_csv.shape[0]):
    pos_csv[i] = pos_csv[i] - pos_csv_init

# reorder the joint according to dict (swap_idx_dict.txt)
pos_csv_swap = np.zeros((pos_csv.shape[0], pos_csv.shape[1], pos_csv.shape[2]))
swap_joint_indices = np.array([0,  5,  6,  7,                       # chest part
                               8,  9,  10, 11, 12, 13, 14, 15, 16,  # right arm
                               17, 18, 19, 20, 21, 22, 23, 24, 25,  # left arm
                               1,  2,  3,  4,                       # head part
                               26, 27, 28, 29, 30, 31,              # right leg
                               32, 33, 34, 35, 36, 37,              # left leg
                               ])

for i in range(pos_csv.shape[0]): # every frame
    for j in range(pos_csv.shape[1]):
        swap_j = swap_joint_indices[j]
        pos_csv_swap[i, swap_j, :] = pos_csv[i, j, :].copy()

# reshape back to txt form
pos_csv_swap = pos_csv_swap.reshape(pos_csv_swap.shape[0], -1)

# downsample to given time interval
pos_csv_swap = pos_csv_swap[::2, :]  # 取第一维的每隔一个元素，第二维全部
print(pos_csv_swap.shape)


# save as txt
import os
output_dir = 'gen_txt'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
output_file = os.path.join(output_dir, txt_name + '.txt')
np.savetxt(output_file, pos_csv_swap, fmt=['%-9.5f'] * pos_csv_swap.shape[1],
           delimiter=", ")

