# for executing body symmetry
# 1) swap the left-hand-side body and right-hand-side body joints idxs
# 2) x, z coordinate remain unchanged, y coordinate *(-1)

import numpy as np

txt_name = 'dog_stepup_jump3_joint_pos_from_csv'
csv_pos = np.loadtxt('gen_txt/' + txt_name + '.txt', delimiter=",")
print(csv_pos.shape)

# ! 1) swap the left-hand-side body and right-hand-side body joints idxs
csv_pos_swap = np.zeros((csv_pos.shape[0], csv_pos.shape[1]))
swap_joint_indices = np.array([ 0,  1,  2,  3,  4,  5,
                               11, 12, 13, 14, 15,
                                6,  7,  8,  9, 10,
                               20, 21, 22, 23,
                               16, 17, 18, 19,
                               24, 25, 26])
for j in range(swap_joint_indices.shape[0]):
    swap_j = swap_joint_indices[j]
    csv_pos_swap[:, 3*j:3*j+3] = csv_pos[:, 3*swap_j:3*swap_j+3].copy()

# ! 2) x, z coordinate remain unchanged, y coordinate *(-1)
for j in range(swap_joint_indices.shape[0]):
    csv_pos_swap[:, 3*j] *= (-1)

print("csv ", csv_pos[:, 0])
print("csv swap ", csv_pos_swap[:, 0])

# ! save as txt
np.savetxt('gen_txt/' + txt_name + '_sym.txt', csv_pos_swap, fmt=['%-9.5f'] * csv_pos_swap.shape[1],
           delimiter=", ")



