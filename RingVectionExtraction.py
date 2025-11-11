import numpy as np
from constants import *

def extract_ring_vectors(matrix):

    result = []
    min_value = np.min(matrix)
    n = matrix.shape[0]
    levels = n // 2
    if matrix.shape[0] % 2 != 0:
        result.append([matrix[levels][levels] - min_value])
    matrix = adjust_matrix_order(matrix)
    n = matrix.shape[0]
    levels = n // 2
    start_points = select_start_points(matrix)

    for level in range(1, levels + 1):
        raw_data = extract_raw_ring_vectors(matrix, level, start_points[level - 1])
        standard_data = [x - min_value for x in raw_data]
        cleaned_data = [x for x in standard_data if x != -1]
        result.append(cleaned_data)
    return result

def extract_raw_ring_vectors(matrix, level, start_point):
    """
    根据给出的层级和起始点，返回顺时针遍历该圈的结果
    :param matrix: 矩阵
    :param level: 圈的层级
    :param start_point: 起始点坐标
    :return:
    """
    n = matrix.shape[0]
    x, y = start_point
    center = n // 2
    result = []

    # 这里上下两行取 level * 8 / 4 + 1 个，左右两列取 level * 8 /4 -1 个，共计 level * 8 个元素
    LT = (center - level, center - level)  # 圈的左上角顶点坐标
    RT = (center - level, center + level)  # 右上角坐标
    LB = (center + level, center - level)  # 左下角坐标
    RB = (center + level, center + level)  # 右下角坐标

    if x == LT[0]:  # 起始点在上行
        result.append(matrix[LT[0]:LT[0] + 1, y:RT[1] + 1].flatten())
        result.append(matrix[RT[0] + 1:RB[0], RT[1]:RT[1] + 1].T.flatten())
        result.append(matrix[LB[0]:RB[0] + 1, LB[1]:RB[1] + 1].flatten()[::-1])
        result.append(matrix[LT[0] + 1:LB[0], LT[1]:LT[1] + 1].T.flatten()[::-1])
        result.append(matrix[LT[0]:LT[0] + 1, LT[1]:y].flatten())
    elif x == LB[0]:  # 起始点在下行
        result.append(matrix[LB[0]:LB[0] + 1, LB[1]:y + 1].flatten()[::-1])
        result.append(matrix[LT[0] + 1:LB[0], LT[1]:LT[1] + 1].T.flatten()[::-1])
        result.append(matrix[LT[0]:LT[0] + 1, LT[1]:RT[1] + 1].flatten())
        result.append(matrix[RT[0] + 1:RB[0], RT[1]:RT[1] + 1].T.flatten())
        result.append(matrix[LB[0]:LB[0] + 1, y + 1:RB[1] + 1].flatten()[::-1])
    elif y == RT[1]:  # 起始点在右列
        result.append(matrix[x:RB[0], RT[1]:RT[1] + 1].T.flatten())
        result.append(matrix[LB[0]:RB[0] + 1, LB[1]:RB[1] + 1].flatten()[::-1])
        result.append(matrix[LT[0] + 1:LB[0], LT[1]:LT[1] + 1].T.flatten()[::-1])
        result.append(matrix[LT[0]:LT[0] + 1, LT[1]:RT[1] + 1].flatten())
        result.append(matrix[RT[0] + 1:x, RT[1]:RT[1] + 1].T.flatten())
    elif y == LT[1]:  # 起始点在左列
        result.append(matrix[LT[0] + 1:x + 1, LT[1]:LT[1] + 1].T.flatten()[::-1])
        result.append(matrix[LT[0]:LT[0] + 1, LT[1]:RT[1] + 1].flatten())
        result.append(matrix[RT[0] + 1:RB[0], RT[1]:RT[1] + 1].T.flatten())
        result.append(matrix[LB[0]:RB[0] + 1, LB[1]:RB[1] + 1].flatten()[::-1])
        result.append(matrix[x + 1:LB[0], LB[1]:LB[1] + 1].T.flatten()[::-1])
    return np.concatenate(result)

def adjust_matrix_order(matrix):

    min_value = np.min(matrix)
    n = matrix.shape[0]

    if n % 2 == 0:
        center = n // 2
        matrix = np.insert(matrix, center, min_value - 1, axis=0)
        matrix = np.insert(matrix, center, min_value - 1, axis=1)

        return matrix
    else:
        return matrix

def select_start_points(matrix):

    result = []
    n = matrix.shape[0]
    center = n // 2
    loops = n // 2
    max_point_index = find_max_index(matrix)

    max_point_xy = coordinate_transform(n, index=max_point_index, indexToXY=True)
    slope = calculate_slope(max_point_xy)
    # print(f"max_point_xy:{max_point_xy},slope:{slope}")

    if slope == Constants.X_IS_ZERO:
        if max_point_xy[1] > 0:
            for i in range(center - 1, -1, -1):
                result.append((i, center))
        else:
            for i in range(center + 1, n):
                result.append((i, center))

    elif slope == Constants.Y_IS_ZERO:
        if max_point_xy[0] > 0:
            for i in range(center + 1, n):
                result.append((center, i))
        else:
            for i in range(center - 1, -1, -1):
                result.append((center, i))
    else:
        state = state_by_slope_and_point(slope, max_point_xy)
        if state == Constants.Y_TO_POSITIVE:
            for y in range(1, loops + 1):  # y从1 ~ n/2
                x = int(round(y / slope, 0))
                index = coordinate_transform(n, XY=(x, y), indexToXY=False)
                result.append(index)

        elif state == Constants.Y_TO_NEGATIVE:
            for y in range(-1, 0 - (loops + 1), -1):  # y从-1 ~ -n/2
                x = int(round(y / slope, 0))
                index = coordinate_transform(n, XY=(x, y), indexToXY=False)
                result.append(index)

        elif state == Constants.X_TO_POSITIVE:
            for x in range(1, loops + 1):
                y = int(round(x * slope, 0))
                index = coordinate_transform(n, XY=(x, y), indexToXY=False)
                result.append(index)

        elif state == Constants.X_TO_NEGATIVE:
            for x in range(-1, 0 - (loops + 1), -1):
                y = int(round(x * slope, 0))
                index = coordinate_transform(n, XY=(x, y), indexToXY=False)
                result.append(index)
        # print(result)

    return result

def state_by_slope_and_point(slope, point):

    quadrant = find_quadrant(point)

    if slope < -1 or slope > 1:
        if quadrant == Constants.FIRST_QUADRAN or quadrant == Constants.SECOND_QUADRAN:
            return Constants.Y_TO_POSITIVE
        else:
            return Constants.Y_TO_NEGATIVE

    elif -1 <= slope <= 1:
        if quadrant == Constants.FIRST_QUADRAN or quadrant == Constants.FOURTH_QUADRAN:
            return Constants.X_TO_POSITIVE
        else:
            return Constants.X_TO_NEGATIVE

def find_quadrant(point):

    x, y = point

    if x > 0 and y > 0:
        return Constants.FIRST_QUADRAN
    elif x < 0 and y > 0:
        return Constants.SECOND_QUADRAN
    elif x < 0 and y < 0:
        return Constants.THIRD_QUADRAN
    elif x > 0 and y < 0:
        return Constants.FOURTH_QUADRAN
    else:
        return None

def find_max_index(matrix):

    matrix_copy = np.copy(matrix)
    n = matrix.shape[0]
    center_index = n // 2


    matrix_copy[center_index, center_index] = np.min(matrix) - 1


    max_index_flat = np.argmax(matrix_copy)
    max_index = np.unravel_index(max_index_flat, matrix_copy.shape)

    return max_index

def coordinate_transform(n, index=(0, 0), XY=(0, 0), indexToXY=True):

    if indexToXY:
        X = index[1] - n // 2
        Y = n // 2 - index[0]
        return X, Y
    else:
        row = n // 2 - XY[1]
        col = XY[0] + n // 2
        return row, col

def calculate_slope(point):

    x, y = point
    if y == 0:
        return Constants.Y_IS_ZERO
    elif x == 0:
        return Constants.X_IS_ZERO  # 或者可以选择返回 None 或其他表示无穷大的值
    else:
        return y / x