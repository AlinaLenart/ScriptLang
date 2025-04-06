1. Napisz skrypt, który wyświetli na wyjście standardowe listę wszystkich zmiennych
środowiskowych.
    a. Niech skrypt umożliwia uruchomienie go z dowolną liczbą parametrów linii
komend. W takim przypadku, należy przeltrować zmienne do wyświetlenia na
wyjściu standardowym. Warunkiem wyświetlania zmiennej i jej wartości jest
istnienie parametru, którego wartość zawiera się w nazwie zmiennej.
    b. Zmienne powinny być wyświetlone w porządku alfabetycznym.

Przykładowe uruchomienie: ``` python env_var.py ``` or ``` python python env_var.oy HOME ``` or ``` python python env_var.oy HOME PATH ```

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
``` bash python path_var.py ```
Aby dla każdego katalogu wypisać również listę plików wykonywalnych:
``` bash python path_var.py -e ```


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
``` bash cat plik.txt | python tail.py ```
        ii. z argumentem określającym ścieżkę pliku, który ma być wypisany np.
``` bash python tail.py plik.txt ```
        iii. w przypadku wywołania łączącego te dwa sposoby, np.
``` bash cat plik.py | python tail.py plik.txt ```
program powinien zignorować dane z wejścia standardowego i wyświetlić
dane z pliku.

Przykładowe uruchomienie: ``` bash  python tail.py --lines=5 test.txt ``` or ``` bash cat test.txt | python tail.py ```
