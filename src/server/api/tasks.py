import pandas as pd
import os
from datetime import datetime

# Path to the CSV-File
file_path = "costs.csv"

# Demo of new row
new_row = {
    "Datum": datetime.today().strftime("%Y-%m-%d"),
    "Uhrzeit": datetime.now().strftime("%H:%M:%S"),
    "Summe_Food": 00.59,
    "Summe_NonFood": 00.39,
    "Foto_Datei": "kassenbon_09.jpeg"
}

# check if existing file-pth
if os.path.exists(file_path):
    # read existing file
    df_old = pd.read_csv(file_path, sep = ";")
    # New row as new DataFrame
    df_new = pd.DataFrame([new_row])
    # Appending new row
    df_all = pd.concat([df_old, df_new], ignore_index=True)
else:
    # if not existing then take the new row as a start of Dataframe
    df_all = pd.DataFrame([new_row])

# Overwrite the file by the df_all
df_all.to_csv(file_path, sep= ";", index=False)

# Print the resulting csv file
print(df_all)