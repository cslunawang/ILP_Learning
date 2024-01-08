'''
生产A车和B车：
obj：利润最大化  -x y代表两种车的产量
    30000 * x + 45000 * y
baseline : x = y = 4
1、3 * x + 4 * y <= 30
2、5 * x + 6 * y <= 2 * 30
3、1.5 * x + 3 * y <= 21
'''
import numpy as np
import pulp
import matplotlib.pyplot as plt

def get_Result():
    my_lp_problem = pulp.LpProblem("My_Lp_Problem", pulp.LpMaximize)
    x = pulp.LpVariable('x', lowBound=0, cat='Continuous')
    y = pulp.LpVariable('y', lowBound=0, cat='Continuous')
    my_lp_problem += 30000 * x + 45000 * y
    my_lp_problem += 3 * x + 4 * y <= 30
    my_lp_problem += 5 * x + 6 * y <= 2 * 30
    my_lp_problem += 1.5 * x + 3 * y <= 21
    my_lp_problem.solve()
    print(pulp.LpStatus[my_lp_problem.status])
    # for variable in my_lp_problem.variables():
    #     print("{} = {}".format(variable.name, variable.varValue))
    # print(pulp.value(my_lp_problem.objective))
    '''
    another way
    '''
    print("Production of Car A = {}".format(x.varValue))
    print("Production of Car B = {}".format(y.varValue))
    print(pulp.value(my_lp_problem.objective))

def draw_pic():
    x = np.linspace(0, 10, 2000)
    y = np.linspace(0, 8, 2000)
    y1 = 3 * x + 4 * y
    y2 = 5 * x + 6 * y
    y3 = 1.5 * x + 3 * y
    plt.plot(x, y1, label=r'$3x+4y\leq30$')
    plt.plot(x, y2, label=r'$5x+6y\leq60$')
    plt.plot(x, y3, label=r'$1.5x+3y\leq21$')
    plt.xlim((0, 10))
    plt.xlim((0,8))
    plt.xlabel(r'$x$')
    plt.ylabel(r'$y$')
    #绘制阴影区域
    # y4 = np.minimum(0)
    y4 = 0
    y5 = np.maximum(y1, y2, y3)
    plt.fill_between(x, y4, y5, where=y5>y4, color='grey', alpha=0.5)
    #绘制图表
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0)
    #解决遮挡
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    get_Result()
    draw_pic()