import pandas as pd

class Ingatlan:
    def __init__(self, tipus, arak, Dates, dataCount):
        self.tipus = tipus
        self.arak = arak
        self.Dates = pd.to_datetime(Dates, format='%Y-%m')  # Convert Dates column to datetime
        self.dataCount = dataCount

class Ingatlanok:
    def __init__(self, Lakoingatlan, Csaladihaz, Teglaepitesuhaz, Panellakas, Sorhaz):
        self.Lakoingatlan = Lakoingatlan
        self.Csaladihaz = Csaladihaz
        self.Teglaepitesuhaz = Teglaepitesuhaz
        self.Panellakas = Panellakas
        self.Sorhaz = Sorhaz

# Specify the path to your XLSX file
file_path = "statisztika_18megye.xlsx"

# Load the XLSX file
xls = pd.ExcelFile(file_path)

# Initialize empty dictionaries to store data for each property type
ingatlan_data = {
    "Lakóingatlan": [],
    "Családi ház": [],
    "Tégla építésű ház": [],
    "Panellakás": [],
    "Sorház": []
}

# Iterate through each sheet in the XLSX file
for sheet_name in xls.sheet_names:
    df = xls.parse(sheet_name, skiprows=1)
    selected_columns = df.iloc[:, :2]
    data_count = len(selected_columns)
    arak = selected_columns["Átlagos négyzetméter ár"].tolist()
    Dates = selected_columns["Dátum"].tolist()

    # Create an instance of Ingatlan for each property type
    ingatlan = Ingatlan(tipus=sheet_name, arak=arak, Dates=Dates, dataCount=data_count)
    ingatlan_data[sheet_name] = ingatlan

# Create an instance of Ingatlanok
ingatlanok = Ingatlanok(
    Lakoingatlan=ingatlan_data["Lakóingatlanok"],
    Csaladihaz=ingatlan_data["Családi házak"],
    Teglaepitesuhaz=ingatlan_data["Téglalakások"],
    Panellakas=ingatlan_data["Panellakások"],
    Sorhaz=ingatlan_data["Sorház"],
)

# Set the global variable startDate
startDate = ingatlanok.Lakoingatlan.Dates.min()

print(f"Start date: {startDate}")
# © Copryright 2024 - Tatár Mátyás Bence