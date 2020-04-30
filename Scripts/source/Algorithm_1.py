import pandas as pd
import numpy as np

io = r'C:\Users\VLSILAB-100\Desktop\smims\a1.xlsx'
io_imu = r'C:\Users\VLSILAB-100\Desktop\smims\b.xlsx'
data = pd.read_excel(io, header=None)
data_imu = pd.read_excel(io_imu, header=None)
x = data[0]
y = data[1]
z = data[2]
x_imu = data_imu[0]
y_imu = data_imu[1]
z_imu = data_imu[2]
x_imu_p = []
y_imu_p = []
z_imu_p = []
x_aver = []
y_aver = []
z_aver = []
l = len(x)
x_aver.append(data[0][0])
y_aver.append(data[1][0])
z_aver.append(data[2][0])
x_imu_p.append(data[0][0])
y_imu_p.append(data[1][0])
z_imu_p.append(data[2][0])
def imu(x, y, z, x_imu, y_imu, z_imu):
    x_imu_p = x + x_imu
    y_imu_p = y + y_imu
    z_imu_p = z + z_imu
    return x_imu_p, y_imu_p, z_imu_p
def average (x_imu_p, y_imu_p, z_imu_p, x_p, y_p, z_p):
    x_aver = (x_p + x_imu_p) / 2    
    y_aver = (y_p + y_imu_p) / 2  
    z_aver = (z_p + z_imu_p) / 2 
    return x_aver, y_aver, z_aver


for i in range(0,l-1):
    a, b, c = imu(x_aver[i], y_aver[i], z_aver[i], x_imu[i], y_imu[i], z_imu[i])
    x_imu_p.append(a)
    y_imu_p.append(b)
    z_imu_p.append(c)
    if(x[i+1] != 0 and y[i+1] != 0 and z[i+1] != 0):
        a_aver, b_aver, c_aver = average (x_imu_p[i+1], y_imu_p[i+1], z_imu_p[i+1], x[i+1], y[i+1], z[i+1])  
        x_aver.append(a_aver)
        y_aver.append(b_aver)
        z_aver.append(c_aver)
    else :
        x_aver.append(x_imu_p[i+1])
        y_aver.append(x_imu_p[i+1])
        z_aver.append(x_imu_p[i+1])

data_f = np.transpose(np.vstack((x_imu_p, y_imu_p, z_imu_p, x_aver, y_aver, z_aver)))

data_df = pd.DataFrame(data_f)
data_df.columns = ['x_imu_prediction','y_imu_prediction','z_imu_prediction','x_average','y_average','z_average']
writer = pd.ExcelWriter('Save_Excel_1.xlsx')
data_df.to_excel(writer,float_format='%.5f')
writer.save()

