# PUTcyberCONF
## OneDrive:
https://putpoznanpl-my.sharepoint.com/:f:/g/personal/piotr_kontowicz_put_poznan_pl/EpxFXjgjMXJHoesM0Th_-NYBsmkXtHzCgy_8689qD7UcMA?e=dkCzBg

## 127.0.0.1 ctf.pl w pliku C:\Windows\System32\drivers\etc\hosts
To będzie można się w przeglądarce odwoływać po nazwie.

## Podstawowe zadania:
   1. Grzebanie w kodzie źródłowym strony - śmietnik html
   2. admin true/false - włamanie admina - Work in Progress
   3. Robots.txt - odzyskanie pieska. 
       - Lokalizacja pieska/flagi pieskowej w tym pliku.
       - Następnie udać się do wskazanego subdir
   4. Sqli - kod do drzwi w bazie więźniów - Work in Progress
   5. File upload - plik zastępujący nagranie z kamer. Chcemy dodać mp4 a się nie da
   6. JWT token - stały secretkey - zawartość karty z prisoner na guard - Work in Progress
   7. IDOR - subdomena  - wychodzi z więzienia i na podglądzie karty widać jego dane i trzeba je zmienić. ID więźniów jest for example od 10-50 a strażników od 0-10. - Work in Progress
   8. Zrobić stronkę z wyświetlaniem profilu więźnia i po zmianie id w url-u zmieniać profile na inne.

### Dodatkowe zadania (będzie trzeba ich sobie poszukać samemu):
   Ukryte zakończenie:
   Wysłanie metody FLAG w burpie - do pomyślenia

## Co jest teraz? Spis zadań:
   1. Flaga ukryta w źródle strony. (gotowe)
   2. Aby zdobyć flagę będzie trzeba się zalogować, dane do logowania będą na stronie w komentarzu, login w pliku strony, hasło w czymś dodatkowym. (gotowe)
   3. Flaga ukryta w źródle strony, ale zakodowane w base64. (gotowe)
   4. Prosty IDOR np lista postów i jeden "ukryty". (można powiedziec ze gotowe - postów zawsze może być więcej)
   5. Jakiś błąd z directory traversal. (gotowe)
   6. Ciasteczko z polem admin 0, zmiana na 1 i po odświeżeniu dostanie się flagę. Dodałem jeszcze brute force logowania. (gotowe) 
   7. Strona posiada pole tekstowe, atakujący ma zapytać sie o flagę wtedy ją dostanie, jednak słowo będzie to blokowane na froncie, będzie musiał zmodyfikować sobie request. (gotowe)
   8. jedno zadanie hidden

# TODO: Zliczanie punktów dla adminów
# TODO: Pomoc: opis tego jak należy zgłaszać flagi, format flagi
# TODO: Opis podatności/błędów: information disclosure, idor, directory travelsal, ciasteczka, potrzebne narzędzia: przeglądarka, burp 