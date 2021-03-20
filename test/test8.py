from Order import inp,outp,stop
from StrategyOBV import OBVTheory
from StrategyMA import MA
import math


def cal_ang(point_1, point_2, point_3):
    """
    根据三点坐标计算夹角
    :param point_1: 点1坐标
    :param point_2: 点2坐标
    :param point_3: 点3坐标
    :return: 返回任意角的夹角值，这里只是返回点2的夹角
    """
    try :
        a=math.sqrt((point_2[0]-point_3[0])*(point_2[0]-point_3[0])+(point_2[1]-point_3[1])*(point_2[1] - point_3[1]))
        b=math.sqrt((point_1[0]-point_3[0])*(point_1[0]-point_3[0])+(point_1[1]-point_3[1])*(point_1[1] - point_3[1]))
        c=math.sqrt((point_1[0]-point_2[0])*(point_1[0]-point_2[0])+(point_1[1]-point_2[1])*(point_1[1]-point_2[1]))
        A=math.degrees(math.acos((a*a-b*b-c*c)/(-2*b*c)))
        B=math.degrees(math.acos((b*b-a*a-c*c)/(-2*a*c)))
        C=math.degrees(math.acos((c*c-a*a-b*b)/(-2*a*b)))
    except :
        B=0
    return B



cal =  cal_ang((11493, 1), (11495, 2), (11500, 3))
print(11500,':',cal)
cal =  cal_ang((11493, 1), (11495, 2), (11496, 3))
print(11496,':',cal)
cal =  cal_ang((11493, 1), (11495, 2), (11495, 3))
print(11495,':',cal)
cal =  cal_ang((11493, 1), (11495, 2), (11494, 3))
print(11494,':',cal)
cal =  cal_ang((11493, 1), (11495, 2), (11493, 3))
print(11493,':',cal)
cal =  cal_ang((11493, 1), (11495, 2), (11492, 3))
print(11492,':',cal)
cal =  cal_ang((11493, 1), (11495, 2), (11491, 3))
print(11491,':',cal)
cal =  cal_ang((11493, 1), (11495, 2), (11490, 3))
print(11490,':',cal)
cal =  cal_ang((11493, 1), (11495, 2), (11489, 3))
print(11489,':',cal)