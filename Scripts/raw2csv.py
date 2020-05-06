# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from bokeh.io import output_notebook, push_notebook, show
from bokeh.models import Span
from bokeh.plotting import figure

import pandas as pd
import pyexcelerate


# %%
i_file = "../Data/imu__9.txt"
o_file = "../Result/imu__9.xlsx"


# %%
data = []
with open(i_file) as f:
    lines = list(f)[26:-3]
    for line in lines:

        st = line.split(",")
        data.append(st)


# %%
data_df = pd.DataFrame(data, columns=["x", "y", "z", "time"])
data_df[["x", "y", "z"]] = data_df[["x", "y", "z"]].astype(float)
data_df["time"] = data_df["time"].astype(int)
data_df["duration"] = data_df.time.cumsum()


# %%
fragment = []
silence = False
data_filtered = (data_df["x"] < 0.3) & (data_df["x"] > -0.3)
cnt = 0
for idx in range(len(data_filtered)):
    if data_filtered[idx]:
        cnt = cnt + 1
    else:
        cnt = 0
        if silence:
            fragment.append(idx - 1)
            silence = False
    if cnt > 400:
        silence = True
        if idx == len(data_filtered)-1:
            fragment.append(idx)
silence = False
data_filtered = (data_df["x"] < 0.3) & (data_df["x"] > -0.3)
cnt = 0
for idx in reversed(range(len(data_filtered))):
    if data_filtered[idx]:
        cnt = cnt + 1
    else:
        cnt = 0
        if silence:
            fragment.append(idx + 1)
            silence = False
    if cnt > 400:
        silence = True
        if idx == 0:
            fragment.append(idx)
fragment.sort()


# %%
output_notebook()
p = figure(
    title="origin",
    x_axis_label="time",
    y_axis_label="x",
    plot_width=1500,
    plot_height=800,
)
p.line(data_df.duration, data_df.x, legend_label="Amplitude", line_width=2)
for idx in fragment:
    line = data_df.duration[idx]
    vline = Span(
        location=line,
        dimension="height",
        line_color="red",
        line_dash="dashed",
        line_width=3,
    )
    p.add_layout(vline)
handle = show(p, notebook_handle=True)
push_notebook(handle=handle)


# %%
# with pd.ExcelWriter('IMU.xlsx') as writer:
# data_df[['x','y','z','duration']].to_excel(writer, sheet_name='IMU_origin')
w_data = [data_df[["x", "y", "z", "duration"]].columns.tolist(),] + data_df[
    ["x", "y", "z", "duration"]
].values.tolist()
wb = pyexcelerate.Workbook()
wb.new_sheet("IMU_origin", data=w_data)
wb.save(o_file)
print("Write origin done")
file_len = int((len(fragment) - 2) / 2)
file_cnt = 0
for idx in range(0, len(fragment) - 3, 2):
    # os.system('clear')
    file_cnt = file_cnt + 1
    file_idx_s = fragment[idx]
    file_idx_e = fragment[idx + 3]
    # with pd.ExcelWriter('IMU.xlsx', mode= 'a') as writer:
    # data_df[['x','y','z','duration']][file_idx_s:file_idx_e].to_excel(writer, sheet_name='IMU_' + str(file_cnt), index=False)
    w_data = [
        data_df[["x", "y", "z", "duration"]][file_idx_s:file_idx_e].columns.tolist(),
    ] + data_df[["x", "y", "z", "duration"]][file_idx_s:file_idx_e].values.tolist()
    wb.new_sheet(
        "IMU_" + str(file_cnt),
        data=w_data,
    )
    wb.save(o_file)
    print("Write fragment file(" + str(file_cnt) + "/" + str(file_len) + ")")
print("done")
# os.system('pause')


# %%



# %%


