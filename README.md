# Program na dělení adresních bodů

Tento neinteraktivní program dělí data (body) do skupin tak, aby po dělení žádná z výsledných 
skupin neobsahovala více než 50 bodů. Dělení probíhá pomocí metody quadtree. Atributy 
vstupních bodů tento program zachovává, přestože s nimi nepracuje. Pracuje pouze se 
souřadnicemi (atribut `coordinates`). Ke každému bodu navíc přibude atribut `cluster_id`,
který určuje, do které skupiny po dělení pomocí quadtree jednotlivé body patří. 



## Vstup
Vstupem je soubor dat s názvem `input.geojson`, který je uložen ve formátu GeoJSON jako 
FeatureColection bodů. 



## Výstup
Výstup je také uložen ve formátu GeoJSON jako FeatureColection bodů s názvem `output.geojson`.



## Metoda quadtree
Kolem vstupní množiny bodů je vytvořen bounding box, který je geometricky dělen na čtvrtiny. 
Po každém dělení na čtvrtiny je testováno, zda je počet bodů v novém kvadrantu menší než 50.
Pokud podmínka splněna není, množina bodů je dále rekurzivně dělena. V případě, že podmínka 
je splněna, je bodům přidán atribut `cluster_id ` a jsou zapsány do výsledného seznamu  `points_out `.

Přidávání atributu  `cluster_id ` je realizováno pomocí definování pomocného seznamu, který má 
pouze jeden prvek na začátku rovný 0. Při testování koncové podmínky rekurze je poté z tohoto 
seznamu hodnota vybrána a zapsána bodům splňujícím danou podmínku. Hned poté je zapsaná hodnota
z pomocného seznamu odstraněna a uložena do pomocné proměnné, která je následně do seznamu opět
vrácena, ale je již s hodnotou o 1 větší. Toto se opakuje při každém zapsání nové skupiny bodů, 
která splňuje koncovou podmínku rekurze. Proto každá skupina méně než 50 bodů obsahuje 
jedinečné `cluster_id ` .


## Popis funkcionality použitých funkcí


_funkce extract_coord_
- z množiny vstupních dat `feats` vybere pro každý bod jeho x a y souřadnici a uloží je do
samostatného seznamu


_funkce calculate_bbox_
- jejím vstupem je opět `feats`
- tato funkce využívá funkci `extract_coord` pro výběr souřadnic bodů; v seznamu souřadnic poté 
najde minimální a maximální hodnoty pro každou souřadnici zvlášť
- výstupem jsou tyto min a max hodnoty


_funkce quadtree_build_
- této funkci je předána vstupní množina bodů `feats`, seznam pro zápis výsledných bobů, krajní 
hodnoty bounding boxu, pomocný seznam pro přidávání `cluster_id ` 
- funkce má za úkol geometricky dělit data na čtvrtiny
- ve funkci je počítán střed bounding boxu z jeho krajních hodnot
- následně jsou určeny krajní hodnoty 4 nových kvadrantů vzniklých po dělení původního bounding boxu
- poté jsou vytvořeny nové seznamy pro body spadající do 4 nových kvadrantů
- na nové čtyři kvadranty tato funkce rekurzivně volána
- koncová podmínka rekurze: pokud množina bodů po dělení obsahuje méně než 50 bodů, je bodům přidán
nový atribut  `cluster_id ` jsou body jsou zapsány do výsledného seznamu  `points_out `
