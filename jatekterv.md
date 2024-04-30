# Ingatlan befektetés játék

## Cél

A játékosoknak minnél több pénze legyen, az ingatlan kereskedésből.

## Lehetőségek

- Vásárlás
- Eladás
- Passzolás

3 db kölönböző ingatlan típus van:

- Lakóingatlan
- Családi ház
- Tégla építésű ház
- Panellakás
- Sorház

## Játékmenet

A program szimulálja az utolsó x év m^2 árait, és a játékosoknak lehetősége van vásárolni, eladni, vagy passzolni kölümböző ingatlanokat.
A játék elején a játékosok meghatázornak egy nehézségi szintet (1-10), és egy kezdő összeget (>0).

A játék folyamán egymás után telnek el a hónapok, és a játékosnak dönteni kell, hogy az adott hónapban vásárol, elad, vagy passzol.

Amikor a játékos vásárolni vagy eladni szeretne, akkor ki kell választania, hogy melyik típusú ingatlannal (1-5) tenné azt.

A játékosnak, lehetősége van megnézni, a birtokában lévő ingatlanokat, azt hogy ezeket mennyiért vette, és jelenleg mennyiért tudná eladni.

## Program működése

1. Betölti a xslx fájlt, és kiszedi belőle az ingatlanonkénti Átlagos m^2 árakat, és a mellé tartozó dátumokat.
   1. megnézi, hogy létezik e a `xslxPath` fájl, és ha igen, akkor betölti a következő módon:
      1. Létrehoz egy `Ingatlanok` objektumot, amiben tárolja az ingatlanokat, és azok árait, és dátumait.
      2. Megnyitja a fájlt.
      3. Megkeresi a `Lakóingatlanok` nevű táblát.
      4. Betölti a táblát az `Ingatlanok.Lakoingatlan.arak` listába.
      5. Elismétli ezt a folyamatot a többi táblára is (Családi házak, Téglalakások, Panellakások, Sorház).
2. Bekéri a nehézséget és a kezdő összeget.
3. Elindítja a játékot, és a játékosoknak lehetősége van vásárolni, eladni, vagy passzolni kölümböző ingatlanokat.
4. A `startDate`-tól kezdve elindul, havonta léptet, és addik ameddig a háztípushoz tartozik ingatlan ár adat, avval számolja az ingatlan árat az adott hónapra. Ha nem tartozik hozzá, akkor meghívha a GenerateAr() függvényt.
5. Ha az ingatlan piac bedől (avagy 0 lesz az értéke valamely m2-es árnak), akkor vége a játéknak, és a játékosoknak kiírja, hogy ki mennyi pénzzel rendelkezik.

## Osztályok

### Ingatlanok

- Lakoingatlan:ingatlan
- Csaladihaz:ingatlan
- Teglaepitesuhaz:ingatlan
- Panellakas:ingatlan
- Sorhaz:ingatlan

### Ingatlan

- id: int
- tipus:string (Lakóingatlan, Családi ház, Tégla építésű ház, Panellakás, Sorház)
- arak[int]
- Dates[date]

### OwnedIngatlan

- tipus:string (Lakóingatlan, Családi ház, Tégla építésű ház, Panellakás, Sorház)
- BoyPrice
- BuyDate

### Fa struktúra

- Ingatlan adatok
  - Lakóingatlan
    - tipus
    - Árak
    - Dátumok
  - CsaládiHáz
    - tipus
    - Árak
    - Dátumok
  - TéglaépítésűHáz
    - tipus
    - Árak
    - Dátumok
  - Panellakás
    - tipus
    - Árak
    - Dátumok
  - Sorház
    - tipus
    - Árak
    - Dátumok

## Változók

- `xslxPath`: string
- `nehezseg`: int
- `kezdoOsszeg`: int
- `IngatalAdatok`: Ingatlanok
- `startDate`: date # A játék kezdő dátuma, xslx fájlból beolvasva
- `ownedIngatlans`: list[OwnedIngatlan] # A játékos által birtokolt ingatlanok
  - Ebben az esetben az Ingatlan osztály dátuma a vásárlás hónapjára értendő

## Metódusok / Függvények

- `GenerateAr()`: int # Az adott hónapra számolja az ingatlan árát. Alapvetően próbálja követni az eddigi árak alapján rajzolódó görbét, amit megszoroz a nehézségi szinttől függően egy random számmal 0.2 és 3 között.
  - Képlet válztozók:
    - `predictedAr`: int # Az előző hónap ára
    - `alsoHatar`: float
      - Ha `nehezseg`: akkor `1-(nehezseg/10)`
      - Ha `nehezseg` > 5 : akkor `(1-(nehezseg/10))**2`
    - `felsoHatar`: float
      - Ha `nehezseg` < 5: akkor `1+(nehezseg/10)`
      - Ha `nehezseg` > 5 : akkor `(1+(nehezseg/10))**2`
  - Nehézségi képlet: `ar = (predictedAr * (random.uniform(0.2, 3))`
- `GeneratePredictedAr(arak[int])`:
  - implementálás alatt...
- `GenerateIngatlan(tipus:str)`: Egy ingatlan árat generál a megadott típushoz tartozó m2 határok között, és visszaadja azt.


© Copryright 2024 - Tatár Mátyás Bence, Kennedi Nadja