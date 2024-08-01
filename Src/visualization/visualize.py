import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from IPython.display import display

# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------
df = pd.read_pickle('../../Data/interim/01_data_processed.pkt')

# --------------------------------------------------------------
# Plot single columns
# --------------------------------------------------------------
set_df = df[df['set'] == 1]

plt.plot(set_df['acc_y'])
plt.plot(set_df['acc_y'].reset_index(drop=True))
# --------------------------------------------------------------
# Plot all exercises
# --------------------------------------------------------------
df.info()
for label in df['label'].unique():
  subset = df[df['label']== label]
  display(subset.head(2))
  fig, ax = plt.subplots()
  plt.plot(subset["acc_y"].reset_index(drop=True),label=label)
  plt.legend()
  plt.show()
# for the first 100
for label in df['label'].unique():
  subset = df[df['label']== label]
  display(subset.head(2))
  fig, ax = plt.subplots()
  plt.plot(subset[:100]["acc_y"].reset_index(drop=True),label=label)
  plt.legend()
  plt.show()
# --------------------------------------------------------------
# Adjust plot settings
# --------------------------------------------------------------
mpl.style.use('seaborn-v0_8-deep') # styling
mpl.rcParams["figure.figsize"] = (20, 5) # to extened the size of the diagram
mpl.rcParams['figure.dpi'] = 100 # for resolution

# --------------------------------------------------------------
# Compare medium vs. heavy sets
# --------------------------------------------------------------
category_df = df.query("label == 'squat'").query ("participant == 'A'").reset_index ()


category_df.groupby(["category"]) ["acc_y"].plot()# using groupby
ax.set_ylabel("acc_y")
ax.set_xlabel("Samples")
plt.legend()
# --------------------------------------------------------------
# Compare participants
# --------------------------------------------------------------

participant_df =df.query("label == 'bench'").sort_values("participant").reset_index ()
participant_df.groupby(["participant"]) ["acc_y"].plot()# using groupby
ax.set_ylabel("acc_y")
ax.set_xlabel("Samples")
plt.legend()

# --------------------------------------------------------------
# Plot multiple axis
# --------------------------------------------------------------
label = "squat"
participant= "A"
all_axis_df = df.query(f"label == '{label}'").query(f"participant == '{participant}'").reset_index()

fig, ax = plt.subplots()
all_axis_df[["acc_x", "acc_y","acc_z"]].plot(ax=ax)
ax.set_ylabel("acc_y")
ax.set_xlabel("Samples")
plt.legend()
# --------------------------------------------------------------
# Create a loop to plot all combinations per sensor
# --------------------------------------------------------------
labels = df["label"].unique()
participants = df ["participant"].unique()

for label in labels:
  for paritcipant in participants:
    all_axis_df = (
      df.query(f"label == '{label}'")
      .query(f"participant == '{participant}'").reset_index ()
    )
    if len (all_axis_df) > 0:

      fig, ax = plt.subplots()
      all_axis_df[["acc_x", "acc_y","acc_z"]].plot(ax=ax)
      ax.set_ylabel("acc_y")
      ax.set_xlabel("Samples")
      plt.title(f"{label} ({participant})".title())
      plt.legend


for label in labels:
  for paritcipant in participants:
    all_axis_df = (
      df.query(f"label == '{label}'")
      .query(f"participant == '{participant}'").reset_index ()
    )
    if len (all_axis_df) > 0:

      fig, ax = plt.subplots()
      all_axis_df[["gyr_x", "gry_y","gry_z"]].plot(ax=ax)
      ax.set_ylabel("gry_y")
      ax.set_xlabel("Samples")
      plt.title(f"{label} ({participant})".title())
      plt.legend



# --------------------------------------------------------------
# Combine plots in one figure
# --------------------------------------------------------------


# --------------------------------------------------------------
# Loop over all combinations and export for both sensors
# --------------------------------------------------------------