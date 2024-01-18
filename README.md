# cs2-item-parser
Programma, kas paredzēta Steam Community Market skrapēšanai
## Dažu terminu pārskats
### Kas ir CS2 Skins?
Counter Strike 2 ir vairāku spēlētāju taktiskā pirmās personas šāvēja videospēle (multiplayer tactical first-person shooter video game), viena no tās raksturīgākajām iezīmēm ir weapon skins. Weapon skins ir krāsojumu modeļi, kurus ir iespējams dabūt kā atlīdzību spēles laikā, kā arī nopirkt un pārdot Steam Community tirdzniecības platformā (Marketplace). Weapon skins izmaina ieroču izskatu spēles laika, kas padara spēles pieredzi krāsaināku un interesantāku. Daži weapon skins piemēri: ![image](https://github.com/alekssdanielssipicins/cs2-item-parser/assets/144723311/fc4f22fc-ad9f-4f5e-a87f-37fdd052654b)
### Kas ir skins float vērtība?
Float value ir mainīgais, kas tiek piešķirts katrai CS2 precei (unikāls katrai precei), tā vērtība var būt jebkurš float tipa skaitlis no 0 līdz 1. Float vērtība parāda nolietošanas pakāpi, jo lielāka tā ir, jo vairāk noskrāpēts izskatās ieroča modelis. Piemērs: ![image](https://github.com/alekssdanielssipicins/cs2-item-parser/assets/144723311/9d2fd37f-b25f-42dc-a206-526059dddf01)
### Kā var uzzināt float vērtību ieroča modelim?
Float vērtība glābājas CS2 spēles serveros un parasti to var iegūt tikai atvērot CS2 spēli un apskatot tajā attiecīgo preci. Savukārt bez papildus rīkiem to nevar uzzināt Steam Community tirdzniecības platformā (attiecīgi nevar nopirkt preci ar noteiktu float vērtību).
Tomēr spēlētājiem ir pieejami vairāki Chrome paplašinājumi (extensions), kā "CSFloat Market Checker" un "Steam Inventory Helper", kas ļauj atspoguļot float vērtību Steam Community tirdzniecības platformā.
## Projekta uzdevuma apraksts
Starp CS2 spēlētājiem ir pieņemts augstāk novērtēt ieroču modeļus ar mazāko float vērtību. Tomēr šādu preču meklēšana, pat izmantojot SIH un CSFloat paplašinājumus, ir laikietilpīgs process. Tāpēc bija nolemts uzrakstīt programmu, kas var skrapēt vairākas CS2 preces, pārbaudīt to float vērtību, un nopirkt preces, kuriem float vērtība atbilst prasītai.
## Problēmas programmas izstrādes laikā
Programmas izstrādes laikā izrādījas, ka Steam Community Marketplace ir relatīvi labi aizsargāta pret skrāpēšanu. Ja īsā laika periodā tiek veikti vairāki pieprasījumi no vienas IP adreses, Steam automātiski nobloķē visus pieprasījumus no šīs IP adreses, rezultātā uz kādu laiku Steam Community tirdzniecības platformu nevar izmantot pat personīgiem mērķiem. ![image](https://github.com/alekssdanielssipicins/cs2-item-parser/assets/144723311/1e3c758d-1ba1-4f63-b4c7-6edef6213352)
Tas rādīja noteiktas grūtības un bija nepieciešams piesaistīt proksi serverus un eksperimentēt ar gaidīšanas laikiem starp pieprasījumiem.
## Izmantoto bibliotēku saraksts
1. selenium - bibliotēka, lai automatizētu darbību ar pārlūkprogrammu
2. time - bibliotēka, lai nodrošinātu gaidīšanas laikus starp pieprasījumiem uz serveri
3. sys - no System bija nepieciešams tikai sys.exit(), lai apstadītu programmu, ja rodas requests error (varētu arī neizmantot bibliotēku, bet kods būtu garāks)
4. pandas - lai atvieglotu URL un vēlāmas float vērtības nodošanu programmai, bija nolemts noformēt tos .xslx failā. pandas bibliotēka nepieciešama, lai programma varētu nolasīt informāciju no .xslx faila.
Jāpiemin, ka bija uzrakstīti 2 python faili, viens no kuriem satur tikai sekojošās funkcijas: *open_listing* - šī funkcija pieprasa noteiktas preces marketplace lapu, kamēr tā neatveras bez kļūdām (lai gan videodemonstrācijā tas nenotika, bet bieži pieprasot preces lapu notiek kļūda, pat manuālā darba laikā); *find_item* - šī funkcija iegūst visas float vērtības un salīdzina tās ar float_cap, kā arī satur kodu, kas nodrošina preces nopirkšanu; *steam_login* - šī funkcija automātiski ielogojas Steam akauntā un konfigurē SIH paplašinājuma parametrus.
## Izmantošanas metodes un uzlabošanas iespējas
Programmu var izmantot, lai nopirktu ieroču modeļus ar zemāko float vērtību. Šādi ieroču modeļi tiek augstāk vērtēti spēlētāju lokā, spēles laika izskatās labāk un trešo pusu tīrdzniecības platformās tiek tirgotas par augstāku cenu.
Programmas kodā var redzēt, ka tā pārbauda tikai katra ieroča modeļa 100 lētākos un jaunākos pārdošanas piedāvājumus. Bija meģinājumi nodrošināt pārslegšanos starp lapām, bet tas gandrīz momentāli noveda pie IP bloķēšanas (pat ar rotating proxy). Iespējams, ka modificējot gaidīšanas laikus šo problēmu varētu novērst
Veicot nelielas izmaiņas *find_item* funkcijas kodā ir iespējams meklēt ne tikai preces ar noteiktu float vērtību, bet arī preces ar noteiktu pattern index. Piemēram šeit ir 2 weapon skins ar vienādu nosaukumu un samērā vienādu float vērtību, bet dažādiem pattern index: ![image](https://github.com/alekssdanielssipicins/cs2-item-parser/assets/144723311/db57da55-8cde-4b32-bfb3-be8beaf09abc)
## Videodemonstrācija
https://youtu.be/n0x13Mp3ps4
6 min ilga videodemonstrācija (var skatīt ar palielinātu atskaņošas ātrumu)
