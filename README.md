# OneDrive:
https://putpoznanpl-my.sharepoint.com/:f:/g/personal/piotr_kontowicz_put_poznan_pl/EpxFXjgjMXJHoesM0Th_-NYBsmkXtHzCgy_8689qD7UcMA?e=dkCzBg

## 127.0.0.1 ctf.pl w pliku C:\Windows\System32\drivers\etc\hosts
To będzie można się w przeglądarce odwoływać po nazwie.

### Podstawowe zadania:
   1. Grzebanie w kodzie źródłowym strony - śmietnik html
   2. admin true/false - włamanie admina ->
   3. Robots.txt - odzyskanie pieska. 
       - Lokalizacja pieska/flagi pieskowej w tym pliku.
       - Następnie udać się do wskazanego subdir
   4. Sqli - kod do drzwi w bazie więźniów
   5. File upload - plik zastępujący nagranie z kamer. Chcemy dodać mp4 a się nie da
   6. JWT token - stały secretkey - zawartość karty z prisoner na guard
   7. IDOR - subdomena  - wychodzi z więzienia i na podglądzie karty widać jego dane i trzeba je zmienić. ID więźniów jest for example od 10-50 a strażników od 0-10.
   8. Zrobić stronkę z wyświetlaniem profilu więźnia i po zmianie id w url-u zmieniać profile na inne.


### Dodatkowe zadania (będzie trzeba ich sobie poszukać samemu):
   Ukryte zakończenie:
   Wysłanie metody FLAG w burpie - do pomyślenia

# TODO: Zliczanie punktów dla adminów
# TODO: Pomoc: opis tego jak należy zgłaszać flagi, format flagi
# TODO: Opis podatności/błędów: information disclosure, idor, directory travelsal, ciasteczka, potrzebne narzędzia: przeglądarka, burp 