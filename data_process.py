from csv_read import *
import datetime
import matplotlib.pyplot as plt

# 计算运行时间：开始时间
start_time = datetime.datetime.now()
# 选取一组实验的文件,第几行第几个点


src_data = MyData(2, 1)
# 读取数据
gradient_csv_path = src_data.load_gradient_csv()
data2process = src_data.read_csv(gradient_csv_path)
# 抽取第一列
col1 = src_data.pick_col(data2process, 0)
position = src_data.find_max(col1)
# 完全复制一个列表
position_plus = position[:]
# 最开头添加0
position_plus.insert(0, 1)
src_data.write_csv(position_plus)
# 计算运行时间：结束时间
plt.figure(2)
plt.plot(col1)
plt.show()

end_time = datetime.datetime.now()
# 显示运行时间
print(str("The program ran for " + str((end_time - start_time).seconds)) + ' seconds')
