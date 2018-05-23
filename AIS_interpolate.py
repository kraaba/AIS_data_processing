__author__ = 'mirko'

import pandas as pd  # Import Pandas package (high-performance, easy-to-use data structures and analysis tools)
import os  # Provides portable way of using operating system dependent functionality

AIS_dir = 'AIS_BIASstation'  # Directory with all the folders with AIS data from monitoring locations
AIS_mon_locs = os.listdir(AIS_dir)  # List the subdirectories in the AIS_dir folder

# For documentation AIS data from only one monitoring location is sufficient. 
# The script can be simply extended for looping through all the monitoring locations
# by adding "for loc in AIS_mon_locs:" instead of the next line.
loc = AIS_mon_locs[0]  # For demonstration choose only one folder for of AIS data
AIS_mon_loc_path = os.path.join(AIS_dir, loc)  # List monthly AIS data files in the one location AIS folder
# Loop through the monthly AIS data files
for file in os.listdir(AIS_mon_loc_path):
    # Read only the .txt files
    if file.endswith(".txt"):
        file = os.path.join(AIS_mon_loc_path, file)  # Construct the path of the file to be read
        data = pd.read_table(file, sep=';')  # Read the data from the file
        DAYTIME = data.DAY + ' ' + data.TIME  # Add the date and time together into one timestamp
        # Construct a new dataframe from the raed data
        AIS_mon_data = pd.DataFrame(data={'Time': DAYTIME, 'Latitude': data.LAT, 'Longitude': data.LON,
                                          'MMSI': data.MMSI,  'Vs': data.Vs, 'Ship_type': data.TYPEc,
                                          'L1': data.L1, 'L2': data.L2, 'B1': data.B1, 'B2': data.B2,
                                          'Draught': data.DRAUGHT, 'Dist': round(data.DISTKM)})
        # Convert the timestamp to the datetime format
        AIS_mon_data.Time = pd.to_datetime(AIS_mon_data.Time, format='%d-%m-%Y %H:%M:%S', utc=True)

        # Add the AIS data from one location together into one variable
        if file == os.path.join(AIS_mon_loc_path, os.listdir(AIS_mon_loc_path)[0]):
            AIS_mon_data_l = AIS_mon_data  # Create a file to append the data to from the first iteration
        else:
            AIS_mon_data_l = AIS_mon_data_l.append(AIS_mon_data)  # Append to the data frame

del data, AIS_mon_data, DAYTIME, file, AIS_mon_loc_path  # Do some clean up
#%%

import datetime
import matplotlib.pyplot as plt

AIS_mon = AIS_mon_data_l['MMSI'].value_counts() > 1
ships = AIS_mon_data_l.MMSI.unique()

#for one_ship in ships:
#    AIS_mon_one_ship = AIS_mon_data[AIS_mon_data.MMSI == one_ship]

ind = 1
time_thresh = datetime.timedelta(minutes=20)


if AIS_mon[ships[ind]]:
    AIS_mon_one_ship = AIS_mon_data_l[AIS_mon_data_l.MMSI == ships[ind]]
    AIS_mon_one_ship = AIS_mon_one_ship.sort_values(by='Time')

    no = 1
    voyage_no = [1]
    for i in range(1, len(AIS_mon_one_ship)):

        if AIS_mon_one_ship.Time[i] - AIS_mon_one_ship.Time[i-1] > time_thresh:
            no = no+1
        voyage_no.append(no)

    AIS_mon_one_ship['Voyage'] = pd.Series(voyage_no, index=AIS_mon_one_ship.index)


plt.scatter(AIS_mon_one_ship.Longitude, AIS_mon_one_ship.Latitude, c = AIS_mon_one_ship.Voyage)
plt.show()
