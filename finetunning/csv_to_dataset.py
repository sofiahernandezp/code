import datetime
import pandas as pd
import numpy as np
import os
from rich.traceback import install
install()

input_dir = os.path.join(os.path.dirname(__file__), "mindrove_raw")
output_dir = os.path.join(os.path.dirname(__file__), "mindrove_dataset")

# if output_dir does not exist, create it
os.makedirs(output_dir, exist_ok=True)

# find all csv files in mindrove_raw
filenames = []
for filename in os.listdir(input_dir):
    if filename.endswith(".csv"):
        filenames.append(filename)

for filename in filenames:
    csv_file = os.path.join(input_dir, filename)

    emg_df = pd.read_csv(csv_file, delimiter=";", decimal=",")

    # find the index of all beep (1) and boop (2) in the csv file
    beep_index = emg_df.index[emg_df["Trigger"] == 1].tolist()
    boop_index = emg_df.index[emg_df["Trigger"] == 2].tolist()

    print(f"beep_index: {beep_index}")
    print(f"boop_index: {boop_index}")

    # check if the number of beep and boop is the same
    if len(beep_index) != len(boop_index):
        print("Number of beep and boop is not the same")
        exit(1)

    # create a new collumn named gesture and fill it with 0
    emg_df["Gesture"] = 0

    # fill the gestrues 1 to len(beep_index) between beep and boop
    reps_per_gesture = 3
    count = 0
    gesture = 1
    for i in range(len(beep_index)):
        count += 1
        emg_df.loc[beep_index[i]:boop_index[i], "Gesture"] = gesture
        print(f"Gestures {gesture} from {beep_index[i]} to {boop_index[i]}")

        if count == reps_per_gesture:
            count = 0
            gesture += 1

    # create a new dataframe with the fields
    # Sample_num,Task_number,EMG1,EMG2,EMG3,EMG4,EMG5,EMG6,EMG7,EMG8,Timestamp,Video_timestamp,Angle_sample
    new_df = pd.DataFrame(
        columns=[
            "Sample_num",
            "Task_number",
            "EMG1", "EMG2", "EMG3", "EMG4", "EMG5", "EMG6", "EMG7", "EMG8",
            "Timestamp"
        ]
    )

    # fill the new dataframe
    new_df["Sample_num"] = np.linspace(0, len(emg_df) - 1, len(emg_df))
    new_df["Task_number"] = emg_df["Gesture"]
    new_df["EMG1"] = emg_df["CH1"]
    new_df["EMG2"] = emg_df["CH2"]
    new_df["EMG3"] = emg_df["CH3"]
    new_df["EMG4"] = emg_df["CH4"]
    new_df["EMG5"] = emg_df["CH5"]
    new_df["EMG6"] = emg_df["CH6"]
    new_df["EMG7"] = emg_df["CH7"]
    new_df["EMG8"] = emg_df["CH8"]

    # Change the tiemstamp from 11:20:16.292487 to unix timestamp
    print()
    print(f"timestamp original: {emg_df['Timestamp'][0]}")
    print(f"timestamp new: {pd.to_datetime(emg_df['Timestamp'][0])}")
    print(f"timestamp unix: {pd.to_datetime(emg_df['Timestamp'][0]).timestamp()}")
    new_df["Timestamp"] = pd.to_datetime(emg_df["Timestamp"], format="%H:%M:%S.%f")
    # change date to current date
    new_df["Timestamp"] = new_df["Timestamp"].apply(
        lambda x: x.replace(
            year=datetime.datetime.now().year,
            month=datetime.datetime.now().month,
            day=datetime.datetime.now().day
        )
    )

    # to unix timestamp
    new_df["Timestamp"] = new_df["Timestamp"].apply(lambda x: x.timestamp())

    # save the new dataframe to a csv file
    new_filename = filename.replace(".csv", "_dataset.csv")
    new_df.to_csv(os.path.join(output_dir, new_filename), index=False)
