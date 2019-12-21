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
splněna je, jsou body zapsány do výsledného seznamu  `points_out `.

Přidávání atributu  `cluster_id ` je realizováno pomocí zanoření se do původního seznamu bodů
a přidání nového atrubutu. Při cyklu, který prochází body a zkoumá jejich náležitost k nově 
vytvořeným kavdrantům, je pak bodům v novém kvadrantu přidáno číslo do atributu  `cluster_id ` 
odpovídající příslušnému kvadrantu.


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
- této funkci je předána vstupní množina bodů `feats`, polovina délky bounding boxu ve směru 
osy x i y, goemtrický střed bounding boxu a číslo kvadrantu
- funkce má za úkol geometricky dělit data na čtvrtiny
- pomocí geometrického středu původního bounding boxu jsou zde definovány nové 4 kvadranty
- každý nový kvadrant po dělení má svůj geometrický střed určen pomocí přičítání, resp. odčítání své 
nové délky (která se rovná polovině délky kvadrantu předchozího) od geometrického středu předchozího bounding boxu/kvadrantu
- přitom je bodům také přidán nový atribut  `cluster_id ` 
- následně je na nové čtyři kvadranty tato funkce rekurzivně volána
- koncová podmínka rekurze: pokud množina bodů po dělení obsahuje méně než 50 bodů, jsou body jsou 
zapsány do výsledného seznamu  `points_out `
