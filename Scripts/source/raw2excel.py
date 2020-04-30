import pandas as pd
import pyexcelerate


class PositionData:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.fragment = []
        self.data_df = pd.DataFrame()
    def __init__(self, input_file):
        self.input_file = input_file
        self.fragment = []
        self.data_df = pd.DataFrame()
    def read_file(self):
        data = []
        with open(self.input_file) as f:
            lines = list(f)[26:-3]
            for line in lines:

                st = line.split(",")
                data.append(st)

        data_df = pd.DataFrame(data, columns=["x", "y", "z", "time"])
        data_df[["x", "y", "z"]] = data_df[["x", "y", "z"]].astype(float)
        data_df["time"] = data_df["time"].astype(int)
        data_df["duration"] = data_df.time.cumsum()
        self.data_df = data_df

    def find_move(self):
        silence = False
        data_filtered = (self.data_df["x"] < 0.3) & (self.data_df["x"] > -0.3)
        cnt = 0
        for idx in range(len(data_filtered)):
            if data_filtered[idx]:
                cnt = cnt + 1
            else:
                cnt = 0
                if silence:
                    self.fragment.append(idx - 1)
                    silence = False
            if cnt > 400:
                silence = True
                if idx == len(data_filtered) - 1:
                    self.fragment.append(idx)
        silence = False
        data_filtered = (self.data_df["x"] < 0.3) & (self.data_df["x"] > -0.3)
        cnt = 0
        for idx in reversed(range(len(data_filtered))):
            if data_filtered[idx]:
                cnt = cnt + 1
            else:
                cnt = 0
                if silence:
                    self.fragment.append(idx + 1)
                    silence = False
            if cnt > 400:
                silence = True
                if idx == 0:
                    fragment.append(idx)
        self.fragment.sort()

    def write_file(self):
        w_data = [self.data_df[["x", "y", "z", "duration"]].columns.tolist(),] + self.data_df[
            ["x", "y", "z", "duration"]
        ].values.tolist()
        wb = pyexcelerate.Workbook()
        wb.new_sheet("IMU_origin", data=w_data)
        print("Write origin done")
        file_len = int((len(self.fragment) - 2) / 2)
        file_cnt = 0
        for idx in range(0, len(self.fragment) - 3, 2):
            file_cnt = file_cnt + 1
            file_idx_s = self.fragment[idx]
            file_idx_e = self.fragment[idx + 3]
            w_data = (
                [
                    self.data_df[["x", "y", "z", "duration"]][
                        file_idx_s:file_idx_e
                    ].columns.tolist(),
                ]
                + self.data_df[["x", "y", "z", "duration"]][
                    file_idx_s:file_idx_e
                ].values.tolist()
            )
            wb.new_sheet(
                "IMU_" + str(file_cnt), data=w_data,
            )
            wb.save(self.output_file)
            print("Write fragment file(" + str(file_cnt) + "/" + str(file_len) + ")")
        print("done")

    def clear(self):
        self.input_file = ""
        self.output_file = ""
        self.fragment = []


if __name__ == "__main__":
    i_file = input("Input file name: ")
    o_file = input("Output file name: ")
    d = PositionData(i_file, o_file)
    d.read_file()
    d.find_move()
    d.write_file()
