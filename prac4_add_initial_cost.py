'''
在prac3的基础上增加了启动成本: 一个工程停工后在开工就会增加额外的启动成本
A厂和B厂的启动成本分别是 20,000和 400,000。
obj: + [,]启动成本
'''
import numpy as np
import pandas as pd
import pulp

# 读取数据
factories = pd.read_csv('csv/factory_variables.csv', index_col=['Month', 'Factory'])
demand = pd.read_csv('csv/monthly_demand.csv', index_col=['Month'])
# 变量：production\ fatory_status \ swith_on
production = pulp.LpVariable.dicts("production",
                                   ((month, factory) for month, factory in factories.index),
                                   cat='Integer')
factory_status = pulp.LpVariable.dicts("factory_status",
                                      ((month, factory) for month, factory in factories.index),
                                      cat='Binary')
switch_on = pulp.LpVariable.dicts("switch_on",
                                  ((month, factory) for month, factory in factories.index),
                                  cat='Binary')
# 初始化问题和约束函数
model = pulp.LpProblem("scheduling_problem", pulp.LpMinimize)
# [(1, 'A'), (2, 'A'), (3, 'A'), (4, 'A'), etc.
factory_A_index = [tpl for tpl in factories.index if tpl[1] == 'A']
factory_B_index = [tpl for tpl in factories.index if tpl[1] == 'B']
print(demand.index[0])
print(factory_A_index[0])
model+= pulp.lpSum(
    [production[m, f] * factories.loc[(m, f), 'Variable_Costs'] for m, f in factories.index]
    +[factory_status[m, f] * factories.loc[(m, f), "Fixed_Costs"] for m, f in factories.index]
    +[switch_on[m, f] * 20000 for m, f in factory_A_index]
    +[switch_on[m, f] * 400000 for m, f in factory_B_index])
# 区分开！
# +[switch_on[m, 'A'] * 20000 for m in demand.index]
# +[switch_on[m, 'B'] * 400000 for m in demand.index])
'''
约束：
1、产量==需求量
2、停工，产量为0，；否则在最大和最小之间
3、B厂5月停工
'''
for month in demand.index:
    model += production[month, 'A'] + production[month, 'B'] == demand.loc[month, 'Demand']
for month, factory in factories.index:
    min_production = factories.loc[(month, factory), 'Min_Capacity']
    max_production = factories.loc[(month, factory), 'Max_Capacity']
    model += production[month, factory] >= min_production * factory_status[month, factory]
    model += production[month, factory] <= max_production * factory_status[month, factory]
model += factory_status[5, 'B'] == 0
model += production[5, 'B'] == 0
'''
定义switch_on: 看上个月factory_status=0, 本月为1就是
ps: 第0月需要特殊处理
'''
for month, factory in factories.index:
    if month == 1:
        model += switch_on[month, factory] == factory_status[month, factory]

    # for constraint in make_io_and_constraint(
    #     switch_on[month, factory],
    #     factory_status[month-1, factory],
    #     factory_status[month, factory],
    #     0, 1):
    #     model += constraint
    else:
        if factory_status[month - 1, factory] == 0 and factory_status[month, factory] == 1:
            model += switch_on[month, factory] == 1
        else:
            model += switch_on[month, factory] == 0

# 求解
model.solve()
print(pulp.LpStatus[model.status])
output = []
for month, factory in factories.index:
    var_output = {
        'Month': month,
        'Factory': factory,
        'Production': production[month, factory].varValue,
        'Factory Status': factory_status[month, factory].varValue,
        'Switch On': switch_on[month, factory].varValue
    }
    output.append(var_output)
output_df = pd.DataFrame.from_records(output).sort_values(['Month', 'Factory'])
output_df.set_index(['Month', 'Factory'], inplace=True)
print(output_df)
print(pulp.value(model.objective))


