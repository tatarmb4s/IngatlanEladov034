import pandas as pd
import random as rnd
from rich import print
from pymenu import Menu
import math
class Ingatlan:
    def __init__(self, tipus, arak, Dates, dataCount):
        self.tipus = tipus
        self.arak = arak
        self.Dates = pd.to_datetime(Dates, format='%Y-%m')  # Convert Dates column to datetime
        self.dataCount = dataCount

class KeszIngatlan:
    def __init__(self, meret, tipus, ar):
        self.id = rnd.randint(1000, 9999)
        self.meret = generate_size(tipus)
        self.tipus = tipus
        self.ar = ar

class Ingatlanok:
    def __init__(self, Lakoingatlan, Csaladihaz, Teglaepitesuhaz, Panellakas, Sorhaz):
        self.Lakoingatlan = Lakoingatlan
        self.Csaladihaz = Csaladihaz
        self.Teglaepitesuhaz = Teglaepitesuhaz
        self.Panellakas = Panellakas
        self.Sorhaz = Sorhaz

ownedIngatlans: list[KeszIngatlan] = []

# Specify the path to your XLSX file
file_path = "statisztika_18megye.xlsx"

# Load the XLSX file
xls = pd.ExcelFile(file_path)

# Initialize empty dictionaries to store data for each property type
ingatlan_data = {
    "Lakóingatlanok": [],
    "Családi házak": [],
    "Téglalakások": [],
    "Panellakások": [],
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
lakStDate = ingatlanok.Lakoingatlan.Dates.min()
csalStDate = ingatlanok.Csaladihaz.Dates.min()
teglaStDate = ingatlanok.Teglaepitesuhaz.Dates.min()
panelStDate = ingatlanok.Panellakas.Dates.min()
sorStDate = ingatlanok.Sorhaz.Dates.min()
startDate = max(lakStDate, csalStDate, teglaStDate, panelStDate, sorStDate)


print(f"Start date: {startDate}")

# # Example usage:
# print(ingatlanok.Sorhaz.dataCount)  # Output: Number of data points for Sorház
# print(ingatlanok.Lakoingatlan.tipus)  # Output: "Lakóingatlan"
# print(ingatlanok.Csaladihaz.arak)    # Output: List of average prices for Családi ház
# print(ingatlanok.Panellakas.Dates)   # Output: List of dates for Panellakás
nehezseg:int
penz:int
currentDate:pd.Timestamp = startDate
currentStore: dict[str, list[KeszIngatlan]] = {}
currentPrices: dict[str, int] = {}

def GenerateAr(predictedAr, nehezseg, tipus):
    global currentPrices
    
    if currentPrices.get(tipus) is not None:
        return currentPrices[tipus]
    
    if nehezseg <= 5:
        alsoHatar = 1 - (nehezseg / 10)
        felsoHatar = 1 + (nehezseg / 10)
    else:
        alsoHatar = (1 - (nehezseg / 10)) ** 2
        felsoHatar = (1 + (nehezseg / 10)) ** 2

    ar = predictedAr * rnd.uniform(alsoHatar, felsoHatar)
    currentPrices[tipus] = int(ar)
    return currentPrices[tipus]



def generate_size(property_type):
    sizes = {
        "Lakóingatlanok": 111,
        "Családi házak": 143,
        "Téglalakások": 130,  # átlag a 110 és 150 között
        "Panellakások": 55,  # átlag a 50 és 60 között
        "Sorház": 75  # átlag a 50 és 100 között
    }

    base_size = sizes.get(property_type)
    if base_size is None:
        return "Ismeretlen ingatlan típus"

    min_size = base_size * 0.7
    max_size = base_size * 1.3

    return rnd.uniform(min_size, max_size)

def GetStats():
    return f"\n\n-----\nJelenlegi dátum: {currentDate}\tPénzed: {penz}\n\n----"

def GenerateIngatlan(tipus):
    global nehezseg
    global currentDate
    # Return: Egy új ingatlan objektum, amelynek a mérete random generált a megadott határok között. Attól függ az ingatlan mérete, hogy milyen a típus.
    meret = generate_size(tipus)
    
    ar:int
    
    sikeres = False
    failTimes = 0
    while not sikeres:
        try:
            if currentDate is None or currentDate > ingatlan_data[tipus].Dates.max() or failTimes > 0:
                ar = meret*GenerateAr(ingatlan_data[tipus].arak[-1], nehezseg, tipus)
            else:
                index = ingatlan_data[tipus].Dates.get_loc(currentDate)
                gotar = GenerateAr(ingatlan_data[tipus].arak[index], nehezseg, tipus)
                ar = gotar*meret
            sikeres = True
        except Exception as e:
            failTimes += 1
    
    
    return KeszIngatlan(meret, tipus, ar)

def GenerateStore(tipus, db=10):
    # Legenerál egy db ingatlanból álló boltot, az adott hónaphoz, és visszaadja
    store = []
    for _ in range(db):
        store.append(GenerateIngatlan(tipus))
    return store

def GenerateStores(db=10):
    # Legenerálja az összes boltot
    global currentStore
    global penz
    
    currentStore = {
        "Lakóingatlanok": GenerateStore("Lakóingatlanok", db),
        "Családi házak": GenerateStore("Családi házak", db),
        "Téglalakások": GenerateStore("Téglalakások", db),
        "Panellakások": GenerateStore("Panellakások", db),
        "Sorház": GenerateStore("Sorház", db)
    }
    return currentStore    

def HandlePurchase(tipus:str):
    global penz
    global currentStore
    global ownedIngatlans
    
    if len(currentStore[tipus]) == 0:
        print("Nincs több ingatlan a boltban!")
        input("Nyomj Entert a folytatáshoz..")
        return
    
    print(f"{GetStats()}\n\nElérhető {tipus.lower()}:")
    for i, ingatlan in enumerate(currentStore[tipus]):
        print(f"ID: {i}, Méret: {round(ingatlan.meret)}, Típus: {ingatlan.tipus}, Vétel ár Ár: {ingatlan.ar}")
    
    while True:
        selected_id = input("Adja meg az ingatlan ID-jét, amelyet meg szeretne vásárolni: ")
        if not selected_id.isdigit() or int(selected_id) >= len(currentStore[tipus]):
            
            if selected_id == "n":
                StartGame()
            
            print("Érvénytelen ID! Kérem, adjon meg egy létező ID-t.")
        else:
            break
    ingatlan = currentStore[tipus][int(selected_id)]
    
    if penz < ingatlan.ar:
        print("Nincs elég pénzed az ingatlan megvásárlásához!")
        input("Nyomj Entert a folytatáshoz..")
        return
    ingatlan = currentStore[tipus].pop(int(selected_id))
    
    penz -= ingatlan.ar
    ownedIngatlans.append(ingatlan)
    
    print(f"Az ingatlan megvásárlásra került! {GetStats()}")
    
    akarmeg = input("Szeretne még vásárolni? (I/N): ").lower()
    if akarmeg == "i":
        HandlePurchase(tipus)
    else:
        return
    

visszaSell:bool = False
    
def HandleSell():
    # Eladás: Listázza az összes tulajdonban lévő ingatlant, és lehetővé teszi az eladását, menüz nyit meg, és ott lévő opciókból lehet választani. 
    global penz
    global visszaSell
    eladoMenu = Menu(f"{GetStats()} \n\n Eladás")
    
    visszaSell = False
    
    def HandleVissza():
        global visszaSell
        print("Vissza")
        # StartGame()
        visszaSell = True
        return "Vissza"
        
    
    eladoMenu.add_option("Vissza", HandleVissza)
    for i, ingatlan in enumerate(ownedIngatlans):
        jelenar = ingatlan.meret*GenerateAr(ingatlan.ar, nehezseg, ingatlan.tipus)
        eladoMenu.add_option(f" JelÁr: {jelenar}, {round(ingatlan.meret)} m2, {ingatlan.tipus} ", lambda ingatlan=ingatlan: SellProperty(ingatlan))
    
    
    while not visszaSell:
        
        eladoMenu.show()
        if visszaSell:
            return "Vissza"
    
    
def SellProperty(ingatlan:KeszIngatlan):
    global penz
    global currentPrices
    
    price = currentPrices[ingatlan.tipus] * ingatlan.meret
    penz += price
    ownedIngatlans.remove(ingatlan)
    
    print(f"Az ingatlan eladásra került! Kapott összeg: {price}.{GetStats()}")
    
    akarmeg = input("Szeretne még eladni? (I/N): ").lower()
    if akarmeg == "i":
        HandleSell()
    else:
        StartGame()
    

def HandleNextMonth():
    global currentDate
    global currentStore
    
    currentDate += pd.DateOffset(months=1)
    GenerateStores()
    currentPrices.clear()
    # StartGame()

def Exit():
    print("Kilépés...")
    exit()

def StartGame(isTrueStart=False):
    global currentDate
    global currentPrices
    
    if isTrueStart:
        currentDate = startDate
        GenerateStores()
    
    vege = False
    
    def setVege():
        vege = True
    def NextMonth():
        vege = True
    
    
    try: 
        Lakóingatlanok = currentPrices["Lakóingatlanok"]
        Családi = currentPrices["Családi házak"]
        Téglalakások = currentPrices["Téglalakások"]
        Panellakások = currentPrices["Panellakások"]
        Sorház = currentPrices["Sorház"]
    except:
        GenerateStores()
        Lakóingatlanok = currentPrices["Lakóingatlanok"]
        Családi = currentPrices["Családi házak"]
        Téglalakások = currentPrices["Téglalakások"]
        Panellakások = currentPrices["Panellakások"]
        Sorház = currentPrices["Sorház"]
    
    vasarlas = Menu(f"{GetStats()}Vásárlás")
    vasarlas.add_options([
        (f"Lakóingatlanok {Lakóingatlanok}", lambda: HandlePurchase("Lakóingatlanok")),
        (f"Családi házak {Családi}", lambda: HandlePurchase("Családi házak")),
        (f"Téglalakások {Téglalakások}", lambda: HandlePurchase("Téglalakások")),
        (f"Panellakások {Panellakások}", lambda: HandlePurchase("Panellakások")),
        (f"Sorház {Sorház}", lambda: HandlePurchase("Sorház")),
        (f"Vissza", StartGame)
    ])
    
    fomenu = Menu(f"Ingóságeladászati kikapcsolódóalkalmatosság{GetStats()}")
    fomenu.add_options([
        ("Vásárlás", vasarlas),
        ("Eladás", HandleSell),
        # ("Boltok", Stores),
        ("Következő hónap", HandleNextMonth),
        ("Kilépés", Exit)
    ])
    
    while not vege:
        fomenu.title = f"Ingóságeladászati kikapcsolódóalkalmatosság{GetStats()}"
        fomenu.show()
    
    print(GenerateIngatlan("Lakóingatlanok").ar)
    
    currentPrices = {}

"-----------------------------------------------"

# nehezseg bekerese
sikeres = False
while not sikeres:
    try:
        nehezseg:int = int(input("Milyen nehézségű feladatot szeretnél? (1-10): "))
        # nehezseg:int = 1
        if nehezseg < 1 or nehezseg > 10:
            raise ValueError("A megadott nehézség nem megfelelő!")
        sikeres = True
    except ValueError as e:
        print(e)

print(f"A megadott nehézség: {nehezseg}")

# pénz bekerese

sikeres = False
while not sikeres:
    try:
        penz:int = int(input("Mennyi pénzed van? (Ft): "))
        # penz:int = 20000000
        if penz < 0:
            raise ValueError("A megadott pénzösszeg nem megfelelő!")
        sikeres = True
    except ValueError as e:
        print(e)
        
        
StartGame(isTrueStart=True)



# © Copryright 2024 - Kennedi Nadja