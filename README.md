# IngatlanEladov034

Ingatlan befektetés játék

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

© Copryright 2024 - Tatár Mátyás Bence, Kennedi Nadja
