import pandas as pd
from glob import glob

# --------------------------------------------------------------
# Read single CSV file
# --------------------------------------------------------------
single_file_acc = pd.read_csv('../../Data/Raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv')

single_file_gryo = pd.read_csv('../../Data/Raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv')

# --------------------------------------------------------------
# List all data in data/raw/MetaMotion
# --------------------------------------------------------------
files = glob('../../Data/Raw/MetaMotion/*.csv')
print(f"Number of files found: {len(files)}")

# --------------------------------------------------------------
# Extract features from filename
# --------------------------------------------------------------
data_path = '../../Data/Raw/MetaMotion/'
f = files[0]
participant = f.split("-")[0].replace(data_path, "")
label = f.split("-")[1]
category = f.split("-")[2].rstrip("123")
df = pd.read_csv(f)

df["participant"] = participant
df["label"] = label
df["category"] = category


df["participant"] = participant.split('/')[-1].split('\\')[-1]
df.head()

# --------------------------------------------------------------
# Read all files
# --------------------------------------------------------------
acc_df = []  # Initialize empty list for accelerometer DataFrames
gyr_df = []  # Initialize empty list for gyroscope DataFrames

acc_set = 1
gyr_set = 1

for f in files:
    participant = f.split("-")[0].replace(data_path, "")
    label = f.split("-")[1]
    category = f.split("-")[2].rstrip("123").rstrip("_MetaWear_2019")

    df = pd.read_csv(f)

    df["participant"] = participant.split('/')[-1].split('\\')[-1]
    df["label"] = label
    df["category"] = category

    if "Accelerometer" in f:
        df['set'] =acc_set
        acc_set += 1
        acc_df.append(df) # Append the DataFrame to the list
    elif "Gyroscope" in f:
        df['set'] =gyr_set
        gyr_set += 1
        gyr_df.append(df)  # Append the DataFrame to the list

# --------------------------------------------------------------


# --------------------------------------------------------------
# Working with datetimes
# --------------------------------------------------------------
# Concatenate all DataFrames in acc_df and gyr_df respectively
acc_combined = pd.concat(acc_df, ignore_index=True)
gyr_combined = pd.concat(gyr_df, ignore_index=True)

# Set the index for both concatenated DataFrames
acc_combined.index = pd.to_datetime(acc_combined['epoch (ms)'], unit='ms')
gyr_combined.index = pd.to_datetime(gyr_combined['epoch (ms)'], unit='ms')


# Example usage: printing the concatenated DataFrames
print("Accelerometer Data:")
print(acc_combined.head())

print("\nGyroscope Data:")
print(gyr_combined.head())

acc_combined
gyr_combined

del acc_combined["epoch (ms)"]
del acc_combined["time (01:00)"]
del acc_combined["elapsed (s)"]


del gyr_combined["epoch (ms)"]
del gyr_combined["time (01:00)"]
del gyr_combined["elapsed (s)"]
# --------------------------------------------------------------
# Turn into function
# --------------------------------------------------------------
files = glob('../../Data/Raw/MetaMotion/*.csv')

def read_data_from_files(files):
    acc_df = []  # Initialize empty list for accelerometer DataFrames
    gyr_df = []  # Initialize empty list for gyroscope DataFrames

    acc_set = 1 # for the set
    gyr_set = 1 # for the set

    data_path = '../../Data/Raw/MetaMotion/'

    for f in files:
        participant = f.split("-")[0].replace(data_path, "")
        label = f.split("-")[1]
        category = f.split("-")[2].rstrip("123").rstrip("_MetaWear_2019")

        df = pd.read_csv(f)
        df["participant"] = participant.split('/')[-1].split('\\')[-1]
        df["label"] = label
        df["category"] = category

        if "Accelerometer" in f:
            df['set'] = acc_set
            acc_set += 1
            acc_df.append(df)  # Append the DataFrame to the list
        elif "Gyroscope" in f:
            df['set'] = gyr_set
            gyr_set += 1
            gyr_df.append(df)  # Append the DataFrame to the list


    # Concatenate all DataFrames in acc_df and gyr_df respectively
    acc_combined = pd.concat(acc_df, ignore_index=True)
    gyr_combined = pd.concat(gyr_df, ignore_index=True)


    acc_combined.index = pd.to_datetime(acc_combined['epoch (ms)'], unit='ms')
    gyr_combined.index = pd.to_datetime(gyr_combined['epoch (ms)'], unit='ms')

    del acc_combined["epoch (ms)"]
    del acc_combined["time (01:00)"]
    del acc_combined["elapsed (s)"]

    del gyr_combined["epoch (ms)"]
    del gyr_combined["time (01:00)"]
    del gyr_combined["elapsed (s)"]
    # Returning the combined DataFrames
    return acc_combined, gyr_combined

    # Set the index for both concatenated DataFrames



# --------------------------------------------------------------
# List all data in data/raw/MetaMotion
# --------------------------------------------------------------
files = glob('../../Data/Raw/MetaMotion/*.csv')
print(f"Number of files found: {len(files)}")

# Read data from files using the function
acc_combined, gyr_combined = read_data_from_files(files)

# Example usage: printing the concatenated DataFrames
print("Accelerometer Data:")
print(acc_combined.head())

print("\nGyroscope Data:")
print(gyr_combined.head())

gyr_combined.head()

acc_combined.head()
# --------------------------------------------------------------
# Merging datasets
# --------------------------------------------------------------
data_merged=pd.concat([acc_combined.iloc[:,:3],gyr_combined],axis=1)

data_merged

data_merged.dropna()
data_merged.head(50)

data_merged.columns = [
    'acc_x',
    'acc_y',
    'acc_z',
    'gyr_x',
    'gyr_y',
    'gyr_z',
    'participant',
    'label',
    'category',
    'set',

]


# --------------------------------------------------------------
# Resample data (frequency conversion)
#
# --------------------------------------------------------------
data_merged[:100].resample(rule='S').mean()


# Accelerometer:    12.500HZ
# Gyroscope:        25.000Hz
sampling = {'acc_x':'mean',
            'acc_y':'mean',
            'acc_z':'mean',
            'gyr_x':'mean',
            'gyr_y':'mean',
            'gyr_z':'mean',
            'participant': 'last',
            'label':'last',
            'category':'last',
            'set':'last'}

data_merged[:1000].resample(rule='200ms').mean()
data_merged.columns
data_merged[:1000].resample(rule='200ms').apply(sampling)

#split for a day

days= [g for n , g in data_merged.groupby(pd.Grouper(freq='D'))]

#days = {n: g for n, g in data_merged.groupby(pd.Grouper(freq='D'))}

days[1]

# --------------------------------------------------------------
# Example usage: printing the first few rows of the first day




data_resampled = pd.concat(df.resample(rule='200ms').apply(sampling).dropna()for df in days)

# Export dataset
data_resampled.to_pickle('../../Data/interim/01_data_processed.pkt')
# --------------------------------------------------------------