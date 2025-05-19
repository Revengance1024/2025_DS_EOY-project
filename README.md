# ParaugdatuSkrāpis

---

_Andris Bremanis [[andris.bremanis@proton.me](andris.bremanis@proton.me)]_

---

## Izmantošana

```bash
# Lejupielādēt bildes pēc URL
uv run src/main.py image-scraper --from-url="https://talsicurling.lv/"

# Lejupielādēt bildes no DuckDuckGo meklētāja pēc atslēgvārda izmantojot Selenium
uv run src/main.py image-scraper --search="potato" -s

# Paātrināt bilžu lejupielādi izmantojot vairākus threads. Saglabāt bilžu failus /tmp/images direktorijā
uv run src/main.py image-scraper --from-url="https://talsicurling.lv/" --threads=16 --output-dir="/tmp/images"
```

## Opcijas

```bash
python3 src/main.py image-scraper -h

Apraksts:
    Lejupielādē attēlus no tīmekļa lapas vai meklēšanas rezultātiem, izmantojot DuckDuckGo.
    Attēli tiek saglabāti norādītajā direktorijā. Ja direktorija neeksistē, tā tiks izveidota.
    Ja tiek izmantots Selenium, tiek izmantots Chrome WebDriver, lai lejupielādētu attēlus.

Lietošana:
  image-scraper [options]

Opcijas:
  -d, --output-dir=OUTPUT-DIR              Bilžu izvaddirektorija [noklusējums: "output/scraped_images"]
      --from-har=FROM-HAR                  Izpildīt pirmo pieprasījumu izmantojot HAR failu [noklusējums: false]
      --from-url=FROM-URL                  Izpildīt pirmo pieprasījumu izmantojot URL [noklusējums: false]
      --search=SEARCH                      Meklēt bildes DuckDuckGo bilžu meklētājā pēc atslēgas vārda [noklusējums: false]
  -s, --selenium                           Izmantot Selenium lai piekļūtu mājas lapai. Izdevīgi, ja nepieciešams JS lai ielādētu saturu
      --download-threads=DOWNLOAD-THREADS  Izmantot vairākus pavedienus paralēlai bilžu lejupielādei [noklusējums: 8]
  -h, --help                               Attēlot komandas palīdzību
  -q, --quiet                              Neizvadīt nekādu informāciju
  -v|vv|vvv, --verbose                     Palielināt informācijas daudzumu: 1 standarta dauzums, 2 vairāk informācijas un 3 problēmu meklēšanai
```

## Instalēšana

```bash
# Instalē uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Noklonē repozitoriju
git clone https://github.com/Revengance1024/2025_DS_EOY-project.git
cd 2025_DS_EOY-project

# Uzstādi virtuālo vidi un instalē atkarības
uv venv
source .venv/bin/activate
uv pip install .

# Notestē, vai komanda strādā
uv run src/main.py
```

## Projekta struktūra

- `input`, `output`: Tukšas direktorijas kas nav iekļautas git ērtības nolūkos. Nav obligāti jāizmanto
- `demo`: Satur demo skriptus, kas parāda dažas no projekta funkcijām
- `src`: Satur projekta kodu
  - `src/main.py`: Galvenais skripts, kas satur komandrindas rīku
  - `src/commands`: Satur komandrindas rīka komandas. Pašreiz ir tikai viena komanda `image-scraper` kas atļauj 
lejupielādēt attēlus no tīmekļa lapas
  - `src/modules`: Šobrīd netiek izmantots. Satur moduļus, kas iespējo atšķirīgi apstrādāt pieprasījumus no dažādām
tīmekļa lapām
  - `src/request_handler`: Satur pieprasījumu apstrādātājus, kas izveido pieprasījumu, un iegūst HTML kodu no atbildes
  - `src/utils`: Satur palīgfunkcijas, kas tiek izmantotas visā projektā


## Izmaontotie resursi/biblotēkas

### [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

Apstrādā saņemto HTML lapu un ļauj to viegli analizēt un meklēt tajā. Tas ir ļoti noderīgi, ja mājas lapā ir
daudz nevajadzīgas informācijas.

### [selenium](https://pypi.org/project/selenium/)

Selenium ir rīks, kas ļauj automatizēt tīmekļa pārlūku. Nepieciešams, ja mājas lapā ir daudz JavaScript, kas jāizpilda,
lai iegūtu lapas saturu. Palīdz arī, ja mājas lapai ir aizsardzība pret botu skrāpēšanu.

### [cleo](https://pypi.org/project/cleo/)

Komandlīnijas rīku izstrādes bibliotēka. Ļauj viegli izveidot komandrindas rīkus ar dažādām opcijām un argumentiem.
Satur palīgrīkus, kā piemēram progresa indikatoru, kas ļauj viegli izsekot lejupielādes progresam.

### [uv](https://github.com/astral-sh/uv)

Uzlabo Python CLI rīku izstrādi. Uv ir rīks, kas ļauj viegli izveidot virtuālās vides un instalēt atkarības.

### [gitignore.io](https://www.toptal.com/developers/gitignore/)

Gitignore.io ir rīks, kas ļauj viegli izveidot .gitignore failus. Pats rīks nav iekļauts projektā, bet tas tika
izmantots, lai uzģenerētu .gitignore failu, kas satur visus nepieciešamos izslēgšanas noteikumus.

### [pyExiftool](https://pypi.org/project/PyExifTool/)

Apvalkprogramma, kas ļauj viegli piekļūt ExifTool funkcijām. ExifTool izmantots projektā, lai analizētu attēlu
formātu failiem, kuriem tas nav viegli nosakāms.

### [requests](https://pypi.org/project/requests/)

Vienkāršots HTTP pieprasījumu izpildes rīks. Izmanto, lai veiktu HTTP pieprasījumus un lejupielādētu attēlus.
Patērē mazāk resursu nekā Selenium, bet nespēj attēlot mājas lapu saturu kas tiek iegūts ar JavaScript.

### [undetected-chromedriver](https://pypi.org/project/undetected-chromedriver/)

Selenium Chrome WebDriver, kas spēj apiet dažādas aizsardzības pret botu skrāpēšanu. Iekļauts, lai
varētu izmantot --headless režīmu, kas ļauj palaist Chrome bez grafiskā interfeisa.


## Atrunājumi

Šis projekts ir izstrādāts kā daļa no 2025. gada Datu struktūras un algoritmi gala projekta. Tas ir paredzēts tikai
izglītojošiem nolūkiem. Autors neuzņemās atbildību, ja projekts tiek izmantots veidā, kas pārkāpj
mājas lapu pakalpojumu sniegšanas noteikumus vai likumus.
