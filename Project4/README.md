1. Napisz skrypt, który wyświetli na wyjście standardowe listę wszystkich zmiennych
środowiskowych.
    a. Niech skrypt umożliwia uruchomienie go z dowolną liczbą parametrów linii
komend. W takim przypadku, należy przeltrować zmienne do wyświetlenia na
wyjściu standardowym. Warunkiem wyświetlania zmiennej i jej wartości jest
istnienie parametru, którego wartość zawiera się w nazwie zmiennej.
    b. Zmienne powinny być wyświetlone w porządku alfabetycznym.

Przykładowe uruchomienie: ``` python scripts/env_var.py ``` or ``` python scripts/env_var.py HOME ``` or ``` python scripts/env_var.py HOME PATH ```

2. Napisz skrypt, który operuje na zmiennej środowiskowej PATH. Zmienna ta
wykorzystywana jest w różnych systemach operacyjnych, m.in. Windows, Linux, Mac OS
X. Zmienna ta zawiera katalogi, w których znajdują się pliki wykonywalne, które mogą
być uruchamiane bez wpisywania pełnej ścieżki do pliku. Skrypt powinien umożliwić, z
wykorzystaniem samodzielnie ustalonych parametrów linii komend, na realizację
poniższych funkcjonalności :
    a. Wypisanie na wyjście standardowe wszystkich katalogów znajdujących się w
zmiennej środowiskowej PATH, każdy w osobnej linii.
    b. Wypisanie na wyjście standardowe każdego katalogu znajdującego się w
zmiennej środowiskowej PATH wraz z listą wszystkich plików wykonywalnych
znajdujących się w tym katalogu.

Przykładowe uruchomienie: 

Aby wypisać tylko katalogi ze zmiennej PATH:
``` python scripts/path_var.py ```
Aby dla każdego katalogu wypisać również listę plików wykonywalnych:
``` python scripts/path_var.py -e ```


3. Napisz własną, uproszczoną wersję uniksowego programu tail, który będzie wypisywał
na wyjście standardowe ostatnie linie zadanego pliku lub danych przekazanych mu na
wejście standardowe. Program powinien:
    a. móc być wywołany z argumentem ```--lines=n```, gdzie ```n``` jest liczbą naturalną
określającą liczbę linii do wypisania.
        i. w przypadku wywołania programu bez tego parametru, program powinien
wypisać 10 ostatnich linii.
        ii. w przypadku, gdy plik ma mniej linii, należy wypisać całą zawartość pliku.
    b. móc być wywołany:
        i. przekazując mu danych na wejście standardowe, np.
``` cat plik.txt | python scripts/tail.py ```
        ii. z argumentem określającym ścieżkę pliku, który ma być wypisany np.
``` python scripts/tail.py plik.txt ```
        iii. w przypadku wywołania łączącego te dwa sposoby, np.
``` cat plik.py | python scripts/.py plik.txt ```
program powinien zignorować dane z wejścia standardowego i wyświetlić
dane z pliku.

Przykładowe uruchomienie: ```  python scripts/tail.py --lines=5 test.txt ``` or ``` cat test.txt | python scripts/tail.py ```


4. Napisz program w ulubionym języku programowania (dowolnym np. C, C++, Rust, Go,
Java, Python, PHP, …), który:
    a. czyta z wejścia standardowego ścieżkę do pliku tekstowego
    b. analizuje plik tekstowy pod kątem statystycznym, a następnie dla oblicza
następujące informacje:
        i. ścieżka do pliku,
        ii. całkowita liczba znaków,
        iii. całkowita liczba słów,
        iv. liczba wierszy,
        v. znak występujący najczęściej,
        vi. słowo występujące najczęściej.
    c. wynik obliczeń wypisywany jest na wyjście standardowe powinien w formacie *.tsv, *.csv, lub *.json
    d. Następnie, napisz skrypt w języku Python, który:
        i. przyjmuje jako argument linii komend ścieżkę do katalogu w systemie
plików,
        ii. z wykorzystaniem modułu subprocess uruchamia napisany powyżej
program do obliczeń, przesyłając na wejście standardowe ścieżki do
kolejnych plików,
        iii. przetwarza dane wyjściowe kolejnych wywołań programu, zapisując
wynik jako listę słowników,
        iv. wypisuje na wyjście standardowe w dowolnym formacie:
            ● liczbę przeczytanych plików, sumaryczną liczbę znaków,
sumaryczną liczbę słów, sumaryczną liczbę wierszy, znak
występujący najczęściej, słowo występujące najczęściej.

Przykładowe uruchomienie: ```  python main.py files ``` or ``` echo "files\test1.txt" | python analyze_file.py ```


5. ``` python mediaconvert.py . --format webm ``` or ``` python mediaconvert.py . --format mp3 ```
