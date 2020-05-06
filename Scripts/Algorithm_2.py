import pandas as pd
import numpy as np
import math
import localization as lx
io = r'C:\Users\VLSILAB-100\Desktop\smims\a.xlsx'
io_imu = r'C:\Users\VLSILAB-100\Desktop\smims\b.xlsx'
io_an = r'C:\Users\VLSILAB-100\Desktop\smims\an.xlsx'
io_an_d = r'C:\Users\VLSILAB-100\Desktop\smims\c.xlsx'
data = pd.read_excel(io, header=None)
data_imu = pd.read_excel(io_imu, header=None)
data_an = pd.read_excel(io_an, header=None)
data_an_d = pd.read_excel(io_an_d, header=None)
x = data[0]
y = data[1]
z = data[2]
x_imu = data_imu[0]
y_imu = data_imu[1]
z_imu = data_imu[2]
x_a = data_an[0]
y_a = data_an[1]
z_a = data_an[2]
x_b = data_an[3]
y_b = data_an[4]
z_b = data_an[5]
x_c = data_an[6]
y_c = data_an[7]
z_c = data_an[8]
x_d = data_an[9]
y_d = data_an[10]
z_d = data_an[11]
d_a = data_an_d[0]
d_b = data_an_d[1]
d_c = data_an_d[2]
d_d = data_an_d[3]
imu_d = []
EP = []
x_aver = []
y_aver = []
z_aver = []
l = len(x_imu)

for i in range(0,l):
    distance = math.sqrt(math.pow(x_imu[i],2) + math.pow(y_imu[i],2) + math.pow(z_imu[i],2))
    imu_d.append(distance)

def anchors_3(x, y, z, x_a, y_a, z_a, x_b, y_b, z_b, x_c, y_c, z_c, d_a, d_b, d_c, imu_d) :
    P=lx.Project(mode='3D',solver='LSE')
    P.add_anchor('anchore_A',(x_a, y_a, z_a))
    P.add_anchor('anchore_B',(x_b, y_b, z_b))
    P.add_anchor('anchore_C',(x_c, y_c, z_c))
    P.add_anchor('anchore_D',(x, y, z))
    t,label=P.add_target()
    t.add_measure('anchore_A',d_a)
    t.add_measure('anchore_B',d_b)
    t.add_measure('anchore_C',d_c)
    t.add_measure('anchore_D',imu_d)
    P.solve()
    return t.loc.std()

def average (x_1, y_1, z_1, x_2, y_2, z_2, x_3, y_3, z_3, x_4, y_4, z_4):
    x_aver = (x_1 + x_2 + x_3 + x_4) / 4 
    y_aver = (y_1 + y_2 + y_3 + y_4) / 4 
    z_aver = (z_1 + z_2 + z_3 + z_4) / 4 
    return x_aver, y_aver, z_aver

for k in range(0,l):
    if d_a[k+1] == 0:
        a =  anchors_3(x[k], y[k], z[k], x_b[0], y_b[0], z_b[0], x_c[0], y_c[0], z_c[0], x_d[0], y_d[0], z_d[0], d_b[k+1], d_c[k+1], d_d[k+1], imu_d[k])
        x[k+1] = a[0]
        y[k+1] = a[1]
        z[k+1] = a[2]
    elif d_b[k+1] == 0:
        a =  anchors_3(x[k], y[k], z[k], x_a[0], y_a[0], z_a[0], x_c[0], y_c[0], z_c[0], x_d[0], y_d[0], z_d[0], d_a[k+1], d_c[k+1], d_d[k+1], imu_d[k])
        x[k+1] = a[0]
        y[k+1] = a[1]
        z[k+1] = a[2]
    elif d_c[k+1] == 0:
        a =  anchors_3(x[k], y[k], z[k], x_a[0], y_a[0], z_a[0], x_b[0], y_b[0], z_b[0], x_d[0], y_d[0], z_d[0], d_a[k+1], d_b[k+1], d_d[k+1], imu_d[k])
        x[k+1] = a[0]
        y[k+1] = a[1]
        z[k+1] = a[2]
    elif d_d[k+1] == 0:
        a =  anchors_3(x[k], y[k], z[k], x_a[0], y_a[0], z_a[0], x_b[0], y_b[0], z_b[0], x_c[0], y_c[0], z_c[0], d_a[k+1], d_b[k+1], d_c[k+1], imu_d[k])
        x[k+1] = a[0]
        y[k+1] = a[1]
        z[k+1] = a[2]
    elif d_a[k+1] != 0 and d_a[k+1] != 0 and d_a[k+1] != 0 and d_a[k+1] != 0:
        a =  anchors_3(x[k], y[k], z[k], x_a[0], y_a[0], z_a[0], x_b[0], y_b[0], z_b[0], x_c[0], y_c[0], z_c[0], d_a[k+1], d_b[k+1], d_c[k+1], imu_d[k])
        b =  anchors_3(x[k], y[k], z[k], x_a[0], y_a[0], z_a[0], x_b[0], y_b[0], z_b[0], x_d[0], y_d[0], z_d[0], d_a[k+1], d_b[k+1], d_d[k+1], imu_d[k])
        c =  anchors_3(x[k], y[k], z[k], x_a[0], y_a[0], z_a[0], x_c[0], y_c[0], z_c[0], x_d[0], y_d[0], z_d[0], d_a[k+1], d_c[k+1], d_d[k+1], imu_d[k])
        d =  anchors_3(x[k], y[k], z[k], x_b[0], y_b[0], z_b[0], x_c[0], y_c[0], z_c[0], x_d[0], y_d[0], z_d[0], d_b[k+1], d_c[k+1], d_d[k+1], imu_d[k])
        EP.append(a)
        EP.append(b)
        EP.append(c)
        EP.append(d)
        a_aver, b_aver, c_aver = average (EP[0][0], EP[0][1], EP[0][2], EP[1][0], EP[1][1], EP[1][2], EP[2][0], EP[2][1], EP[2][2], EP[3][0], EP[3][1], EP[3][2]) 
        x[k+1] = a_aver
        y[k+1] = b_aver
        z[k+1] = c_aver
        EP=[]
    else :
        x[k+1] = x[k] + x_imu
        y[k+1] = y[k] + y_imu
        z[k+1] = z[k] + z_imu

data_f = np.transpose(np.vstack((x, y, z)))

data_df = pd.DataFrame(data_f)
data_df.columns = ['x_average','y_average','z_average']
writer = pd.ExcelWriter('Save_Excel_2.xlsx')
data_df.to_excel(writer,float_format='%.5f')
writer.save()


