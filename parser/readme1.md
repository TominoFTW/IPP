Implementační dokumentace k 1. první úloze do IPP 2022/2023\
Jméno a příjmení: Tomáš Běhal\
Login: xbehal02


## Zpracovani argumentu
První část skriptu začíná zpracováním argumentů z příkazové řádky. Po jejich vyhodnocení se vytvoří proměnná `$input` typu array, do které se načítá po řádcích ze standardního vstupu. Jednotlivé řádky před přídaním od `$input` zbaví komentářů a přebytečných mezer. Dále pokud mi zůstane prázdný řádek, který kontroluji pomocí funkce `empty()`, tak ho přeskakuji a neukládám. 

## Zpracovani instrukci
Před zpracováním instrukcí skript kontroluje správnost hlavičky. Pokud je hlavička v nepořádku, skript vypíše na standardní chybový výstup hlášku o chybné hlavičce a ukončí se s návratovým kódem 21. Pokud je vše v pořádku, tak se začínají zpracovávat jednotlivé instrukce. Nejdříve se jednotlivé řádky s instrukcemi uloží do asociativního pole.
Pomocí `foreach ($lines as $line)` skript iteruje přes jednotlivé řádky a za pomoci `switch-e` kontroluje, zdali je instrukce validní. Pokud ano, tak pokračuje na kontrolu argumentů. Kdyby tomu tak nebylo, skript je ukončen s návratovým kódem 22. Nejdříve skript kontroluje jejich správný počet, což umožňuje kontrola prvků v asociativním poli, pod klíčem `args`. Pokud je počet argumentů v pořádku, tak se začíná provádět kontrola jednotlivých argumentů. Argumenty jsou kontrolovány pomocí jednotlivých funkcí, kde se využívá regulárních výrazů. Pokud je vše validní, tak se vypíše na standardní výstup v adekvátním tvaru XML element. Pokud instrukce není validní, tak se vypíše na standardní chybový výstup hláška o chybě a skript se ukončí s návratovým kódem 23. Inkrementuje se proměnná `$order`, která slouží pro uchování pořadí instrukcí.

## Ukončení skriptu
Jakmile skript úspěšně zpracuje všechny instrukce, tak se vypíše na standardní výstup XML z proměnné `$xml` a skript se ukončí s návratovým kódem 0.
