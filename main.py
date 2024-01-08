# 尝试使用pulp解决线性规划问题
# 任务： 最大化 z = 4x + 3y
import numpy as np
import matplotlib.pyplot as plt
import pulp

def getResult_pulp():
    # 最大化
    my_lp_problem = pulp.LpProblem("My_LP_Problem", pulp.LpMaximize)
    # 声明变量 Continuous 首字母C要大写
    x = pulp.LpVariable('x', lowBound=0, cat='Continuous')
    y = pulp.LpVariable('y', lowBound=2, cat='Continuous')
    # 定义目标函数和约束条件，使用重载符号 +=
    #目标函数
    my_lp_problem += 4 * x + 3 * y
    my_lp_problem += 2 * y <= 25 - x
    my_lp_problem += 4 * y >= 2 * x - 8
    my_lp_problem += y <= 2 * x - 5
    # print(my_lp_problem)
    # 求解 solve 没有r
    my_lp_problem.solve()
    # print(my_lp_problem.status) #返回：1
    print(pulp.LpStatus[my_lp_problem.status]) #返回：optimal
    '''
    Optimal - objective value 73.75  -2 iterations time 0.002
    Problem MODEL has 3 rows, 2 columns and 6 elements
    '''
    # 打印： {}  .format()
    for variable in my_lp_problem.variables():
        print("{} = {}".format(variable.name, variable.varValue))
    print(pulp.value(my_lp_problem.objective))



def print_fig(x, y1, y2, y3, y4):
    plt.plot(x, y1, label = r'$y\geq2$')#geq >=
    plt.plot(x, y2, label = r'$2y\leq25-x$')
    plt.plot(x, y3, label = r'$4y\geq2x-8$')
    plt.plot(x, y4, label = r'$y\leq2x-5$')
    plt.xlim((0, 16))#args:0-16
    plt.ylim((0, 11))
    plt.xlabel(r'$x$')#有$就可以斜体，不知道r有什么用：使用latex语言eg(r'$\theta$')
    plt.ylabel(r'$y$')
    #绘制阴影区域
    y5 = np.minimum(y2, y4)#上顶
    y6 = np.maximum(y1, y3)
    plt.fill_between(x, y5, y6, where=y5>y6, color='grey', alpha=0.5)#alpha
    #绘制图标
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)#横纵坐标比值？
    #解决遮挡 √
    plt.tight_layout()
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    x = np.linspace(0, 20, 2000)#min, max, num /return:array
    y1 = (x * 0) + 2
    y2 = (25 - x) / 2.0
    y3 = (2 * x - 8) / 4.0
    y4 = 2 * x - 5
    # print_fig(x, y1, y2, y3, y4)
    getResult_pulp()

