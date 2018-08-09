# coding: utf-8

"""打开csv文件的类"""

import csv
import sys

import numpy as np

from position_data import *


class MyData:
    # 初始化
    def __init__(self, dir_sort_, group_num_):
        """
        :param dir_sort_:    第几行
        :param group_num_:   每行第几个点
        :return: none
        """
        self.dir_sort = dir_sort_
        self.group_num = group_num_

    # 方法1：输出文件路径
    def load_csv(self):

        if self.group_num > experiment_points[self.dir_sort]:
            print('Exceeded group number, please check again!')
            return -1

        else:
            dir_experiment_date = "I:/20180614/"  # 总路径，一般为实验日期
            if self.dir_sort > 0:
                csv_path = dir_experiment_date + "+" + str(
                    self.dir_sort) + "/" + "+" + str(self.dir_sort) + '.csv'  # 完整路径名称
            elif self.dir_sort < 0:
                csv_path = dir_experiment_date + str(
                    self.dir_sort) + "/" + str(self.dir_sort) + '.csv'  # 完整路径名称
            else:
                csv_path = dir_experiment_date + str(
                    self.dir_sort) + "/" + "+" + str(self.dir_sort) + '.csv'  # 0行完整路径名称
            print(csv_path)  # 打印路径
            return csv_path

    def load_gradient_csv(self):

        if self.group_num > experiment_points[self.dir_sort]:
            print('Exceeded group number, please check again!')
            return -1

        else:
            dir_experiment_date = "I:/20180614/"  # 总路径，一般为实验日期
            if self.dir_sort > 0:
                csv_path = dir_experiment_date + "+" + str(
                    self.dir_sort) + "/" + "+" + str(self.dir_sort) + '_gradient.csv'  # 完整路径名称
            elif self.dir_sort < 0:
                csv_path = dir_experiment_date + str(
                    self.dir_sort) + "/" + str(self.dir_sort) + '_gradient.csv'  # 完整路径名称
            else:
                csv_path = dir_experiment_date + str(
                    self.dir_sort) + "/" + "+" + str(self.dir_sort) + '_gradient.csv'  # 0行完整路径名称
            print(csv_path)  # 打印路径
            return csv_path

    # 方法2：读取文件内容
    def read_csv(self, file_path):
        """
        :param file_path:  接受一个文件的地址
        :return: 返回保存的列表
        """
        data_content = []  # 新建一个空的列表
        with open(file_path) as f:  # 打开文件，将文件对象保存在f中
            reader = csv.reader(f)  # 调用csv.reader()，并且将前面的文件对象作为实参传递给它，reader()返回一个列表
            for i, rows in enumerate(reader):
                if 15 < i:  # 从第16行开始去掉前面的文件头
                    data_content.append(rows)
        return data_content  # 返回保存的列表

    # 方法3：提取二维数组的第col列，返回一个一维列表
    def pick_col(self, src_data, col):
        """
        :param src_data: 原始数据（列表）
        :param col: 要提取的列
        :return: 返回一个一维列表
        """
        cols_limit = np.array(src_data).shape
        if col > cols_limit[1]:
            print('Oops: Exceed the limit of colums of this array ! ')
            print('The shape of the array [rows, cols]: ' + str(cols_limit))
            sys.exit()
        dst_data = [float(i[col]) for i in src_data]  # 从src_data的第i行取第col+1列
        return dst_data

    # 方法4：调谐滤波，去除高斯噪声
    def tuning_filter(self, src_data, length):
        """
        :param length: 选择计算的长度
        :return:
        """
        # 列表转numpy array数组
        data = np.array(src_data, np.float)
        # 看数组的结构
        data_shape = data.shape
        # 生成一个全1数组
        ones = np.ones(data_shape)
        # test
        print(data_shape)
        # 点除求倒数
        div_data = ones / data
        # 新建输出列表
        dst_list = []
        # 从原始数据开头开始数，到总长度减去模板长度结尾
        for i in range(0, len(src_data) - length):
            sum_temp = sum(div_data[i:(i + length)])  # 从第i个数据开始，到模板长度个数结束，切片求和
            dst_list.append(length * (1 / sum_temp))  # 添加到输出列表
        print(len(dst_list))
        return dst_list

    def sub_average(self, list_):
        """
        列表求差，后一个减前一个，输出一个所有差的均值
        :param list_: 输入一个一维列表
        :return: 返回一个均值，int
        """
        sub_ans = []  # 新建一个求值的结果的列表
        for i in range(1, len(list_)):  # 从第二个数开始向前减
            sub_ans.append(list_[i] - list_[i - 1])
        # 求平均并且取整
        average_ans = int(sum(sub_ans) / (len(list_) - 1))
        return average_ans

    def find_max(self, data):
        """
        本函数用于寻找一系列数据中极大值
        :param data: 输入的数据
        :return:
        """
        # 首先获得极大值的数目
        num_of_maxpoint = experiment_points[self.dir_sort]
        print(num_of_maxpoint)
        # 新建一个空位置列表
        position_list = []
        # 新建一个位置估计的列表
        sc = []
        # 求data的第1至3个突变点的位置,范围都是通过估算的，但是值是正确的
        for i in range(0, 3):
            sc.append(data.index(min(data[(i * 12000):(12000 + i * 10000)])))
        # 以前3个点的差的均值为基准
        length = self.sub_average(sc)
        # 第一个突变点的索引：
        pt1_index_base = sc[0]
        # 范围偏移量
        offset = 1000
        # 新建一个列表，包含所有求取范围的索引值，第一个突变点的范围的两个索引直接给出
        pt_index_range_list = [0, pt1_index_base + offset]
        # 开始计算所有突变点的求取范围的索引：
        for i in range(2, num_of_maxpoint + 1):
            pt_index_range_list.append(pt_index_range_list[i - 1] + length)
        # 开始计算所有突变点的索引：
        for i in range(0, num_of_maxpoint):
            position_list.append(data.index(min(data[pt_index_range_list[i]:pt_index_range_list[i + 1]])))
        print("The scope of points' index are: ")
        print(pt_index_range_list)
        print("The points' index are: ")
        print(position_list)
        return position_list

    def write_csv(self, list_):
        """
        用于将列表储存到一个csv文件中
        :param list_:输入一个列表
        :return:
        """

        # 将list_中的每一个数据都变成单独的列表，map() 会根据提供的函数对指定序列做映射。
        arr_list_ = list(map(lambda x: [x], list_))
        dir_experiment_date = "I:/20180614/"  # 总路径，一般为实验日期
        if self.dir_sort > 0:
            dst_path = dir_experiment_date + "+" + str(
                self.dir_sort) + "/" + "+" + str(self.dir_sort) + '_position.csv'  # 完整路径名称
        elif self.dir_sort < 0:
            dst_path = dir_experiment_date + str(
                self.dir_sort) + "/" + str(self.dir_sort) + '_position.csv'  # 完整路径名称
        else:
            dst_path = dir_experiment_date + str(
                self.dir_sort) + "/" + "+" + str(self.dir_sort) + '_position.csv'  # 0行完整路径名称
        with open(dst_path, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(arr_list_)
        print('The position information has been successfully written into a csv file!')
