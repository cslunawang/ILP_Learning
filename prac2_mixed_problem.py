'''
使用三种原料制作两种烤肠
para: 两种材料三种比例 - x1 y1 z1 x2 y2 z2
obj: 使用最小成本
    4.32 * （x1+x2) + 2.46 * (y1+y2) + 1.86 * (z1+z2)
s.t.: -0.05kg
1、350 * 50 * x1 + 500 * 50 * x1 <= 30
2、350 * 50 * y1 + 500 * 50 * y1 <= 20
3、350 * 50 * z1 + 500 * 50 * z1 <= 17
4、x1 > 0.4
5、x2 > 0.6
6、z1 <= 0.25
7、z2 <= 0.25
8、x1 + x2 >= 23
9-n: 材料恰好用完
'''
import pulp
import numpy as np

def get_Result():
    # 成本最小化 混合问题
    model = pulp.LpProblem("Cost_minimizing_blending_problem", pulp.LpMinimize)
    sausages = ['economic', 'premium']# 经济型、优质型
    ingradients = ['pork', 'wheat', 'starch']
    weights = pulp.LpVariable.dicts("weight kg",
                                    ((i, j) for i in sausages for j in ingradients),
                                    cat = 'Continuous')
    # 目标函数
    model += (
        pulp.lpSum([
            4.32 * weights[(i, 'pork')]
            + 2.46 * weights[(i, 'wheat')]
            + 1.86 * weights[(i, 'starch')]
            for i in sausages
        ])
    )
    # 约束
    model += pulp.lpSum([weights[('economic', j)] for j in ingradients]) == 350 * 0.05
    model += pulp.lpSum([weights[('premium', j)] for j in ingradients]) == 500 * 0.05
    model += pulp.lpSum([weights[i, 'pork'] for i in sausages]) <= 30
    model += pulp.lpSum([weights[i, 'wheat'] for i in sausages]) <= 20
    model += pulp.lpSum([weights[i, 'starch'] for i in sausages]) <= 17
    model += pulp.lpSum([weights[i, 'pork'] for i in sausages]) >= 23
    model += weights['economic', 'pork'] >= 0.4 * pulp.lpSum(
        [weights['economic', j] for j in ingradients])
    model += weights['premium', 'pork'] >= 0.6 * pulp.lpSum(
        [weights['premium', j] for j in ingradients])
    model += weights['economic', 'starch'] <= 0.25 * pulp.lpSum(
        [weights['economic', j] for j in ingradients])
    model += weights['premium', 'starch'] <= 0.25 * pulp.lpSum(
        [weights['premium', j] for j in ingradients])
    # 求解
    model.solve()
    print(pulp.LpStatus[model.status])# 注意:pulp.LpStatus是数组，用[]表示索引
    for var in weights:# 返回索引
        var_value = weights[var].varValue
        print("The weight of {0} in {1} sausages is {2} kg".format(var[1], var[0], var_value))
    total_cost = pulp.value(model.objective)
    print('The total cost is {} for 350 economy sausages and 500 premium sausages'.format(total_cost))

if __name__ == '__main__':
    get_Result()
