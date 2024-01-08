'''
github 无法访问，没有数据源
para：[n月，工厂A]-》（12,2），开工（12，2）
obj：最小化成本制定每个工厂产量，满足客户的需求
    [A, Fixed_Costs] + [A, capavity] *  [A, Variable_Costs] + (B)
s.t.:
1、factory_status * [n月，工厂A] + factory_status * [n月，工厂B] ==  demand
ps:
1、访问--factories.loc[(month, factory), 'Variable_Costs']
'''
import pandas as pd
import pulp

factories = pd.read_csv('csv/factory_variables.csv', index_col=['Month', 'Factory'])
print(factories)
'''
row: Max_Capacity Min_Capacity Variable_Costs Fixed_Costs
col: Month Factory
(24, 4)
'''
demand = pd.read_csv('csv/monthly_demand.csv', index_col=['Month'])
print(demand)
# (12, 1)
'''
row: Demand
col: Month
'''
# 定义决策变量-A-B工程每个月的产量: 必须是整数？  index:列
production = pulp.LpVariable.dicts("production",
                                   ((month, factory) for month, factory in factories.index),
                                   lowBound=0,
                                   cat='Integer')
# 定义决策变量-每个月是否开工，决定是否有固定成本: 0/1变量
factory_status = pulp.LpVariable.dicts("factory_status",
                                       ((month, factory) for month, factory in factories.index),
                                       cat='Binary')
'''
不能使用production>0: 表示开工
reason：pulp不是逻辑变成语言，线性规划本身是一些线性函数，用线规表示逻辑并不容易。
    我们在后面约束能看到factory_status与production是存在约束逻辑关系的。
'''
# 定义问题和目标函数
model = pulp.LpProblem("scheduling_problem", pulp.LpMinimize)
# 目标函数：
model += pulp.lpSum(
    [production[month, factory] * factories.loc[(month, factory), 'Variable_Costs'] for month, factory in factories.index]
    +[factory_status[month, factory] * factories.loc[(month, factory), 'Fixed_Costs'] for month, factory in factories.index])
# 约束：恰好相等  ---使用循环  ,为啥不用 * status??
for month in demand.index:
    model += production[month, 'A'] + production[month, 'B'] == demand.loc[month, 'Demand']
# 使用线性约束来表示逻辑约束需要一些技巧。 还需要*status
for month, factory in factories.index:
    min_production = factories.loc[(month, factory), 'Min_Capacity']
    max_production = factories.loc[(month, factory), 'Max_Capacity']
    model += production[month, factory] <= max_production * factory_status[month, factory]
    model += production[month, factory] >= min_production * factory_status[month, factory]
'''
if factory_status[month, factory]==0 : production[(month, factory)] >= 0 and production[(month, factory)] <= 0
else: production[(month, factory)] >= min_production and production[(month, factory)] <= max_production
'''
# B工厂5月份停工
model += factory_status[5, 'B'] == 0
model += production[5, 'B'] == 0 #这个其实可以不用，但是写上可以使优化速度更快，因为不需要通过不等式确定=0了
# 开始solve
model.solve()
print(pulp.LpStatus[model.status])
#打印 varValue能否省去？
output = []
for month, factory in factories.index:
    var_output = {
        'Month': month,
        'Factory': factory,
        'Production': production[month, factory].varValue,
        'Factory Status': factory_status[month, factory].varValue
    }
    output.append(var_output)
# 重新排序 (24, 4) -> (24, 2)
output_df = pd.DataFrame.from_records(output).sort_values(['Month', 'Factory'])
output_df.set_index(['Month', 'Factory'], inplace=True)
# 重新设置索引：主索引改为：Month, Factory
print(output_df)
print(pulp.value(model.objective))
# 12906400.0
