import pytrigno
import numpy as np


trigno = pytrigno.TrignoIMU(n_sensors = 16, host='172.31.1.73',
                 cmd_port=50040, emg_port=50043, data_port=50044, timeout=10)
trigno.start()

    

data = trigno.getEMG()
data = np.mean(data, axis = 1)
emgData = DelsysEMG()
emgData.emg = data


  
N_CHANNELS = 9 # Number of channels is 9 according to official documentation
N_SENSORS = trigno.total_sensors
TOTAL_CHANNELS = N_CHANNELS * N_SENSORS
data = trigno.getData().squeeze()
imuData = DelsysIMU()
imuData.acc_x = data[[i for i in range(0, TOTAL_CHANNELS, N_CHANNELS)]]
imuData.acc_y = data[[i for i in range(1, TOTAL_CHANNELS, N_CHANNELS)]]
imuData.acc_z = data[[i for i in range(2, TOTAL_CHANNELS, N_CHANNELS)]]
imuData.gyro_x = data[[i for i in range(3, TOTAL_CHANNELS, N_CHANNELS)]]
imuData.gyro_y = data[[i for i in range(4, TOTAL_CHANNELS, N_CHANNELS)]]
imuData.gyro_z = data[[i for i in range(5, TOTAL_CHANNELS, N_CHANNELS)]]
