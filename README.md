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
Při splnění této podmínky je bodům zapsáno odpovídající cluster_id a dále již nejsou děleny.
Pokud ale podmínka splněna není, množina bodů je dále rekurzivně dělena. 



## Popis funkcionality použitých funkcí


- _funkce extract_coord_
Z množiny vstupních dat `feats` vybere pro každý bod jeho x a y souřadnici a uloží je do
samostatného seznamu. 


- _funkce calculate_bbox_
Jejím vstupem je opět `feats`. Tato funkce využívá funkci `extract_coord` pro výběr souřadnic
bodů. V seznamu souřadnic poté najde minimální a maximální hodnoty pro každou souřadnici
zvlášť. Výstupem jsou tyto min a max hodnoty. 


- _funkce quadtree_build_
Této funkci je předána vstupní množina bodů `feats`, polovina délky bounding boxu ve směru 
osy x i y, goemtrický střed bounding boxu, pořadí pro zápis `cluster_id` a číslo kvadrantu. 

Funkce má za úkol geometricky dělit data na čtvrtiny. Pomocí geometrického středu původního 
bounding boxu jsou zde definovány nové 4 kvadranty. Každý nový kvadrant po dělení má svůj 
geometrický střed určen pomocí přičítání, resp. odčítání své nové délky (která se rovná 
polovině délky kvadrantu předchozího) od geometrického středu předchozího bounding boxu/kvadrantu. 
Následně je na nové čtyři kvadranty tato funkce rekurzivně volána. 

Koncová podmínka rekurze: pokud množina bodů po dělení obsahuje méně než 50 bodů, je každému bodu 
přidán atribut `cluster_id` a body jsou zapsány do výsledného seznamu. 
