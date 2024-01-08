'''
数独
obj: 无
s.t.:
1、行、列、方格 ： 1-9
2、已知：取已知

二值变量： 9 * 81 = 729
'''

from pulp import *

# 存储1-9
Sequence = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
Vals = Sequence
Rows = Sequence
Cols = Sequence
# 定义9个 3*3 小方格, 列表也可以使用+=
Boxes = []
for i in range(3):
    for j in range(3):
        Boxes += [[(Rows[3 * i + k], Cols[3 * j + l]) for k in range(3) for l in range(3)]]
# len(Boxes): 9
# 定义问题，决策变量，目标函数
prob = pulp.LpProblem("Sudoku_Problem", LpMinimize)
# 定义729个二值决策变量， 变量的名字（索引）是（Val, Rows, Cols）
# 之前：传入list， 这里：传入tuple，tuple，每一个元素是一个list，pulp会帮我们展开
# 之前引用：choices['1','2','3'], 现在引用：choices['1']['2']['3']
# cat: Integer 和 Binary都可以
choices = LpVariable.dicts("Choice", (Vals, Rows, Cols), 0, 1, LpInteger)
# choices = LpVariable.dicts("Choice", (Vals, Rows, Cols), LpBinary)

# 目标函数就是固定的常量函数
prob += 0, "Arbitrary Objective Function"
# 约束：81个个子的9个决策变量有且仅有1个是1，其余为0
# 每个位置：二值变量的和为1
for r in Rows:
    for c in Cols:
        prob += lpSum([choices[v][r][c] for v in Vals]) == 1
'''
合并前
'''
# # 定义每一行 9个数都不同
# for v in Vals:
#     for r in Rows:
#         prob += lpSum([choices[v][r][c] for c in Cols]) == 1
# # 定义每一列 9个数都不同
# for v in Vals:
#     for c in Cols:
#         prob += lpSum([choices[v][r][c] for r in Rows]) == 1
# # 定义每个小表格的约束, 法1麻烦， 改为法2：Boxes
# for v in Vals:
#     for b in Boxes:
#         prob += lpSum([choices[v][r][c] for (r, c) in b]) == 1
#     # for i in range(3):
#     #     for j in range(3):
#             # prob += lpSum([choices[v][3 * i + k][3 * j + l] for k in range(3)
#             #                for l in range(3)]) == 1
'''
合并后
'''
for v in Vals:
    for r in Rows:
        prob += lpSum([choices[v][r][c] for c in Cols]) == 1
    for c in Cols:
        prob += lpSum([choices[v][r][c] for r in Rows]) == 1
    for b in Boxes:
        prob += lpSum([choices[v][r][c] for (r, c) in b]) == 1
# 对于已经填上的格子：
# prob += choices['5']['1']['1'] == 1
# prob += choices['3']['1']['2'] == 1
# prob += choices['7']['1']['5'] == 1
prob += choices['6']['2']['1'] == 1
prob += choices['1']['2']['4'] == 1
prob += choices['9']['2']['5'] == 1
prob += choices['5']['2']['6'] == 1
prob += choices['9']['3']['2'] == 1
prob += choices['8']['3']['3'] == 1
prob += choices['6']['3']['8'] == 1
prob += choices['8']['4']['1'] == 1
prob += choices['6']['4']['5'] == 1
prob += choices['3']['4']['9'] == 1
prob += choices['4']['5']['1'] == 1
prob += choices['8']['5']['4'] == 1
prob += choices['3']['5']['6'] == 1
prob += choices['1']['5']['9'] == 1
prob += choices['7']['6']['1'] == 1
prob += choices['2']['6']['5'] == 1
prob += choices['6']['6']['9'] == 1
prob += choices['6']['7']['2'] == 1
prob += choices['2']['7']['7'] == 1
prob += choices['8']['7']['8'] == 1
prob += choices['4']['8']['4'] == 1
prob += choices['1']['8']['5'] == 1
prob += choices['9']['8']['6'] == 1
prob += choices['5']['8']['9'] == 1
prob += choices['8']['9']['5'] == 1
prob += choices['7']['9']['8'] == 1
prob += choices['9']['9']['9'] == 1

# 写到一个文件里
# prob.writeLP("Sudoku.lp")
# prob.solve()
# print(LpStatus[prob.status])
sudokuout = open('sudoku.txt', 'w')
#
# for r in Rows:
#     if r == "1" or r == "4" or r == "7":
#         sudokuout.write("+------+------+------+\n")
#     for c in Cols:
#         for v in Vals:
#             if value(choices[v][r][c]) == 1:
#                 if c == "1" or c == "4" or c == "7":
#                     sudokuout.write("|")
#                 sudokuout.write(v + "")
#                 if c == "9":
#                     sudokuout.write("|\n")
# sudokuout.write("+------+------+------+")

while True:
    prob.solve()
    print("Status", LpStatus[prob.status])
    if LpStatus[prob.status] == "Optimal":
        # 写入
        for r in Rows:
            if r == "1" or r == "4" or r == "7":
                sudokuout.write("+------+------+------+\n")
            for c in Cols:
                for v in Vals:
                    if value(choices[v][r][c]) == 1:
                        if c == "1" or c == "4" or c == "7":
                            sudokuout.write("|")
                        sudokuout.write(v + "")
                        if c == "9":
                            sudokuout.write("|\n")
        sudokuout.write("+------+------+------+\n\n\n")
        # 添加约束，这个约束可以排除相同的解
        # prob += lpSum([choices["1"][r][c] for r in Rows for c in Cols
        #                if value(choices["1"][r][c] == 1)]) <= 8
        print("aaaaaaaaaaaaaaaaaaa", value(lpSum([choices[v][r][c] for v in Vals for r in Rows for c in Cols
                       if value(choices[v][r][c]) == 1])))
        prob += lpSum([choices[v][r][c] for v in Vals for r in Rows for c in Cols
                       if value(choices[v][r][c]) == 1]) <= 80
    else:
        break
sudokuout.close()
print("written done !!!")














