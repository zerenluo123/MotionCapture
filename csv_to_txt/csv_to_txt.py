import pandas as pd
import numpy as np

# determine the mocap and txt name according to dict ()
mocap_name = 'D1_053_KAN01_001' + '_worldpos'
txt_name = 'dog_walk09' + '_joint_pos'

# read mocap data from csv
pos_df = pd.read_csv(mocap_name + '.csv')
pos_csv = np.array(pos_df)
pos_csv = pos_csv[:, 1:]

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
swap_joint_indices = np.array([0,  24, 25, 26,
                               20, 21, 22, 23,
                               16, 17, 18, 19,
                               1,  2,  11, 12,
                               13, 14, 15, 6,
                               7,  8,  9,  10,
                               3,  4,  5])

for i in range(pos_csv.shape[0]): # every frame
    for j in range(pos_csv.shape[1]):
        swap_j = swap_joint_indices[j]
        pos_csv_swap[i, swap_j, :] = pos_csv[i, j, :].copy()

# reshape back to txt form
pos_csv_swap = pos_csv_swap.reshape(pos_csv_swap.shape[0], -1)

# save as txt
np.savetxt('gen_txt/' + txt_name + '_from_csv.txt', pos_csv_swap, fmt=['%-9.5f'] * pos_csv_swap.shape[1],
           delimiter=", ")


###########################################
##############   Debugging   ##############
###########################################
# # ! only for debugging: see if our methods - example = 0
# # our methods
# csv_pos = np.loadtxt('gen_txt/' + txt_name + '_from_csv.txt', delimiter=",")
#
# # example
# txt_pos = np.loadtxt('gen_txt/' + txt_name + '.txt', delimiter=",")
#
# # our method - example
# diff = csv_pos - txt_pos
#
# # check nonzero col and row
# row, col = np.nonzero(diff)
# # print(row, col)
# print("Nonzero value in the diff: ", diff[row, col])
#
# # widen the condition
# idx_e_5 = np.where(diff > 0.0001)
# print("Number of frame with the error larger than 10 ^ (-4): ", idx_e_5)


