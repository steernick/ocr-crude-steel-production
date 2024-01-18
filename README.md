# OCR-ekstrakcja danych dotyczących produkcji stali z tabel z plików .pdf
## Cel i motywacje:
Niniejszy projekt miał na celu pozyskanie danych o wysokości rocznej produkcji stali (crude steel)  
w poszczególnych krajach w latach 1951 - 2022.  

Dane te planuję wykorzystać w innym projekcie, który zamierzam zrealizować w przyszłości.

W czasie mojej kwerendy internetowej okazało się, że nie ma ogólnodostępnych danych w uporządkowanym formacie 
(.csv, .json lub in.) dotyczących produkcji stali w poszczególnych krajach na przestrzeni dłuższego czasu.  

Jedyne dostępne dane zamieszczone były w formie tabel w plikach pdf (w większości zeskanowanych publikacji papierowych) w poniższych źródłach:  
* dla lat **1969 - 2022** - dane publikowane przez [**World Steel Association**](www.worldsteel.org) w [_Steel Statistical Yearbooks_](https://worldsteel.org/wp-content/uploads/Steel-Statistical-Yearbook-1980.pdf)
* dla lat **1951 - 1968** - dane z [roczników statystycznych](https://unstats.un.org/UNSDWebsite/Publications/StatisticalYearbookPastIssue/) **ONZ**

## Użyte technologie:
* _Python_ w wersji 3.11.5
* _Pytesseract_ w wersji 0.3.10
* _pdf2image_ w wersji 1.16.3
* inne biblioteki takie jak: re, _Pathlib_, _collections_, _json_
* na początkowym etapie w celu przygotowania plików użyłem programu _GIMP_ w wersji 2.10.36

## Przebieg:

#### Projekt podzieliłem na kilka etapów:

### Etap 1.
Wstępne przygotowanie plików do użycia w procesie OCR (_Optical Character Recognition_), polegające na eksportowaniu 
konkretnych stron zawierających table z plików PDF, a następnie z pomocą programu do obróbki graficznej GIMP, 
pliki pochodzące z roczników statystycznych ONZ, przyciąłem do odpowiedniego rozmiaru, 
eliminując niepotrzebne części tabel (np. w języku francuskim).  
Przykładowy efekt można zobaczyć 
[**tu**](https://github.com/steernick/ocr-crude-steel-production/blob/master/examples/pdf%20files/UN-statistical-yearbook-1969.pdf).

### Etap 2. 
#### (plik: [pdf-to-text.py](https://github.com/steernick/ocr-crude-steel-production/blob/master/pdf-to-text.py))

Właściwa obróbka w technologii OCR. Z pomocą biblioteki _pdf2image_ następuje konwersja plików PDF w obrazy, 
a następnie przy użyciu metody `.image_to_string` z biblioteki _pytesseract,_ ekstrakcja tekstu oraz zapisanie go 
do oddzielnych plików tekstowych.

Kluczem do uzyskania maksymalnie użytecznego rezultatu jest konfiguracja samego pytesseract:

`custom_config = r'--oem 3 --psm 6 -c preserve_interword_spaces=1'`

Powyższa konfiguracja jest efektem użycia "metody prób i błędów" w sprawdzaniu różnych wariantów ustawień.

### Etap 3. 
#### (plik: [extract-countries-list.py](https://github.com/steernick/ocr-crude-steel-production/blob/master/extract-countries-list.py))

Celem tego etapu było uzyskanie listy państw występujących w tabelach z zamiarem wykorzystania jej w późniejszej 
(właściwej ekstrakcji).  
Poza uzyskaniem listy państw następuje również wstępna filtracja plików tekstowych i zapisanie ich do nowych plików TXT.   
Do tego etapu zaliczyć można również ręczną edycję i filtrację pliku z listą państw, celem usunięcia niepożądanych wyrazów 
(nazw państw), które nie zostały wychwycone przez algorytm.

### Etap 4. 
#### (plik: [main.py](https://github.com/steernick/ocr-crude-steel-production/blob/master/main.py))
Jest to główny etap obróbki plików tekstowych, którego celem ma być powstanie plików w formacie CSV.  

W pliku _main.py_ na początku umieszczone są definicje funkcji użytych zarówno w tym pliku, jak i w innych.  

Następnie zostają wczytana [lista państw](https://github.com/steernick/ocr-crude-steel-production/blob/master/examples/countries_correct_list.txt) 
oraz z [plik w formacie JSON](https://github.com/steernick/ocr-crude-steel-production/blob/master/examples/countries_mapping.json) 
zawierający słownik z mapowaniem występujących w tekście ciągów znaków, które powinny być zamienione na właściwą nazwę 
państwa. Słownik ten stworzyłem ręcznie w trakcie udoskonalania programu, w celu ostatecznego poprawienia ciągów znaków, 
które nie zostały automatycznie poprawione w użytych w programie algorytmach.  

Główna część programu składa się z dwóch pętli 'for', zagnieżdżonych jedna w drugiej. Zewnętrzna iteruje pliki tekstowe, 
znajdujące się folderze, wewnętrzna linie w każdym z tych plików. Każda iteracja pętli zewnętrznej składa się z 
następujących czynności:

* ekstrakcja nagłówka,
* zainicjowanie zmiennej przechowującej liczbę kolumn,
* zainicjowanie zmiennej (listy), która będzie przechowywać poszczególne pola z danymi dla formatu CSV.  

Później następuje przejście do pętli wewnętrznej, gdzie wykonywane są następujące czynności:

* ekstrakcja części ciągu znaków, która po dalszej obróbce stanie się nazwą państwa,
* ekstrakcja ciągów liczbowych, które po dalszej obróbce staną się wartościami produkcji stali w danym roku,
* obróbka ciągów liczbowych w celu wyodrębnienia konkretnych wartości z pomocą wzorów wyrażeń regularnych z biblioteki _re_
oraz instrukcji warunkowych.
* obróbka ciągu znaków w celu wyodrębnienia poprawnej nazwy państwa z użyciem wcześniej zaimportowanych listy państw, 
słownika mapującego oraz funkcji stworzonej z wykorzystaniem [współczynnika Jaccarda](https://pl.wikipedia.org/wiki/Indeks_Jaccarda).
* na końcu uzyskane pola danych łączone są przecinkami w wiersze a te dodawane do zmiennej `csv_fields_list`.  

Następnie wykonywane jest przejście do pętli zewnętrznej, gdzie ostatnią czynnością jest połączenie nagłówka z listą wierszy
ze zmiennej `csv_fields_list` w gotowy tekst w formacie CSV, który zapisywane jest do oddzielnego pliku, również w formacie CSV.

