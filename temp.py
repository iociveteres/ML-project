import os
import pandas as pd
import numpy as np  

def procces_df(df: pd.DataFrame):
    df = df.set_index('Cycle_Index')
    df.reset_index(drop=True)
    
    return df

def add_to_df(df_to_add_to: pd.DataFrame, df_to_add_from: pd.DataFrame, file_name):
    df = df_to_add_from
    
    cycle_l = []
    cycle_time_l = []
    min_current_l = []
    max_current_l = []
    min_voltage_l = []
    max_voltage_l = []
    discharge_capacity_l = []
    charge_energy_l = []
    discharge_energy_l = []
    charge_capacity_l = []
    discharge_capacity_l = []
    charge_energy_l = []
    discharge_energy_l = []
    efficiency_l = []

    charge_capacity_change_l = []
    discharge_capacity_change_l = []
    charge_energy_change_l = []
    discharge_energy_change_l = []
    # 0th
    fab_charge_capacity = df['Charge_Capacity (Ah)'].iloc[0]
    fab_discharge_capacity = df['Discharge_Capacity (Ah)'].iloc[0]
    fab_charge_energy = df['Charge_Energy (Wh)'].iloc[0]
    fab_discharge_energy = df['Discharge_Energy (Wh)'].iloc[0]

    cycle_l.append(0)
    cycle_time_l.append(df['Test_Time (s)'].iloc[0])

    min_current_l.append(df['Min_Current (A)'].iloc[0])
    max_current_l.append(df['Max_Current (A)'].iloc[0])
    
    min_voltage_l.append(df['Min_Voltage (V)'].iloc[0])
    max_voltage_l.append(df['Max_Voltage (V)'].iloc[0])

    charge_capacity_l.append(fab_charge_capacity)
    discharge_capacity_l.append(fab_discharge_capacity)
    charge_energy_l.append(fab_charge_energy)
    discharge_energy_l.append(fab_discharge_energy)

    charge_capacity_change_l.append(1/fab_charge_capacity)
    discharge_capacity_change_l.append(1/fab_discharge_capacity)
    charge_energy_change_l.append(1/fab_charge_energy)
    discharge_energy_change_l.append(1/fab_discharge_energy)
    # 1st
    init_charge_capacity = df['Charge_Capacity (Ah)'].iloc[1]
    init_discharge_capacity = df['Discharge_Capacity (Ah)'].iloc[1]
    init_charge_energy = df['Charge_Energy (Wh)'].iloc[1]
    init_discharge_energy = df['Discharge_Energy (Wh)'].iloc[1]

    cycle_l.append(1)
    cycle_time_l.append(df['Test_Time (s)'].iloc[1] - df['Test_Time (s)'].iloc[0])

    min_current_l.append(df['Min_Current (A)'].iloc[1])
    max_current_l.append(df['Max_Current (A)'].iloc[1])
    
    min_voltage_l.append(df['Min_Voltage (V)'].iloc[1])
    max_voltage_l.append(df['Max_Voltage (V)'].iloc[1])

    charge_capacity_l.append(init_charge_capacity)
    discharge_capacity_l.append(init_discharge_capacity)
    charge_energy_l.append(init_charge_energy)
    discharge_energy_l.append(init_discharge_energy)

    charge_capacity_change_l.append(1)
    discharge_capacity_change_l.append(1)
    charge_energy_change_l.append(1)
    discharge_energy_change_l.append(1)

    stop = int(df.shape[0]) - 1
    for i, row in enumerate(range(21, stop, 20)):
        cur_cycle = row

        cur_cycle_time = df['Test_Time (s)'].iloc[row] - df['Test_Time (s)'].iloc[row - 1]

        cur_min_current = np.convolve(df['Min_Current (A)'].iloc[row - 10:row + 10], np.ones(20)/20, mode='valid')[0]
        cur_max_current = np.convolve(df['Max_Current (A)'].iloc[row - 10:row + 10], np.ones(20)/20, mode='valid')[0]
        
        cur_min_voltage = np.convolve(df['Min_Voltage (V)'].iloc[row - 10:row + 10], np.ones(20)/20, mode='valid')[0]
        cur_max_voltage = np.convolve(df['Max_Voltage (V)'].iloc[row - 10:row + 10], np.ones(20)/20, mode='valid')[0]

        cur_charge_capacity = np.convolve(df['Charge_Capacity (Ah)'].iloc[row - 10:row + 10], np.ones(20)/20, mode='valid')[0]
        cur_charge_capacity_change = cur_charge_capacity/init_charge_capacity

        cur_discharge_capacity = np.convolve(df['Discharge_Capacity (Ah)'].iloc[row - 10:row + 10], np.ones(20)/20, mode='valid')[0]
        cur_discharge_capacity_change = cur_discharge_capacity/init_discharge_capacity

        cur_charge_energy = np.convolve(df['Charge_Energy (Wh)'].iloc[row - 10:row + 10], np.ones(20)/20, mode='valid')[0]
        cur_charge_energy_change = cur_charge_energy/init_charge_energy

        cur_discharge_energy = np.convolve(df['Discharge_Energy (Wh)'].iloc[row - 10:row + 10], np.ones(20)/20, mode='valid')[0]
        cur_discharge_energy_change = cur_discharge_energy/init_discharge_energy

        cur_efficiency = cur_discharge_energy / cur_charge_energy

        cycle_l.append(cur_cycle)
        cycle_time_l.append(cur_cycle_time)

        min_current_l.append(cur_min_current)
        max_current_l.append(cur_max_current)
        min_voltage_l.append(cur_min_voltage)
        max_voltage_l.append(cur_max_voltage)

        charge_capacity_l.append(cur_charge_capacity)
        discharge_capacity_l.append(cur_discharge_capacity)
        charge_energy_l.append(cur_charge_energy)
        discharge_energy_l.append(cur_discharge_energy)
        efficiency_l.append(cur_efficiency)

        charge_capacity_change_l.append(cur_charge_capacity_change)
        discharge_capacity_change_l.append(cur_discharge_capacity_change)
        charge_energy_change_l.append(cur_charge_energy_change)
        discharge_energy_change_l.append(cur_discharge_energy_change)

    local_df = pd.DataFrame()

    local_df["Cell Id"] = np.array([file_name] * len(cycle_l))
    local_df["Cycle"] = np.array(cycle_l)
    local_df["Cycle_time"] = np.array(cycle_time_l)

    local_df["Min_current"] = np.array(min_current_l)
    local_df["Max_current"] = np.array(max_current_l)
    local_df["Min_voltage"] = np.array(min_voltage_l)
    local_df["Max_voltage"] = np.array(max_voltage_l)

    local_df["Charge_capacity"] = np.array(charge_capacity_l)
    local_df["Charge_capacity_ratio"] = np.array(charge_capacity_change_l)
    local_df["Discharge_capacity"] = np.array(discharge_capacity_l)
    local_df["Discharge_capacity_ratio"] = np.array(discharge_capacity_change_l)

    local_df["Charge_energy"] = np.array(charge_energy_l)
    local_df["Charge_energy_ratio"] = np.array(charge_energy_change_l)
    local_df["Discharge_energy"] = np.array(discharge_energy_l)
    local_df["Discharge_energy_ratio"] = np.array(discharge_energy_change_l)

    df_to_add_to = pd.concat([df_to_add_to, local_df])
    return df_to_add_to
    
def process_csvs():
    csvs_l = os.listdir('./Li-ion_Batteries/')
    general_dataframe = pd.DataFrame(columns=['Cell Id', 'Cycle', 'Cycle_time', 
                                'Min_current', 'Max_current',
                                'Min_voltage', 'Max_voltage',
                                'Charge_capacity', 'Charge_capacity_ratio',
                                'Discharge_capacity', 'Discharge_capacity_ratio',
                                'Charge_energy', 'Charge_energy_ratio',
                                'Discharge_energy', 'Discharge_energy_ratio'])
    for csv_name in csvs_l:
        print(csv_name)
        df_to_add_from = pd.read_csv("./Li-ion_Batteries/" + csv_name)
        add_to_df(general_dataframe, df_to_add_from, csv_name.replace('_cycle_data.csv', ''))

    return general_dataframe

general_dataframe = process_csvs()
general_dataframe.head(5)