# Cieższe rzeczy przeniosłem na OneDrive:
https://putpoznanpl-my.sharepoint.com/:f:/g/personal/piotr_kontowicz_put_poznan_pl/EpxFXjgjMXJHoesM0Th_-NYBsmkXtHzCgy_8689qD7UcMA?e=dkCzBg

## jeśli dodać wpis 127.0.0.1 noc-naukowcow.pl w pliku C:\Windows\System32\drivers\etc\hosts
To będzie można się w przeglądarce odwoływać po nazwie.

Zrobiłem też to repozytorium tak żeby można sobie to spakować w kontener dockerowy. Jak ktoś chce przetestować działanie to: docker pull piotrrtoip/noc-naukowcow (powinno działać)

### Podstawowe zadania:
    1. Flaga ukryta w źródle strony. (gotowe)
    2. Aby zdobyć flagę będzie trzeba się zalogować, dane do logowania będą na stronie w komentarzu, login w pliku strony, hasło w czymś dodatkowym. (gotowe)
    3. Flaga ukryta w źródle strony, ale zakodowane w base64. (gotowe)
    4. Prosty IDOR np lista postów i jeden "ukryty". (można powiedziec ze gotowe - postów zawsze może być więcej)
    5. Jakiś błąd z directory traversal. (gotowe)
    6. Ciasteczko z polem admin 0, zmiana na 1 i po odświeżeniu dostanie się flagę. Dodałem jeszcze brute force logowania. (gotowe) 
    7. Strona posiada pole tekstowe, atakujący ma zapytać sie o flagę wtedy ją dostanie, jednak słowo będzie to blokowane na froncie, będzie musiał zmodyfikować sobie request. (gotowe)

### Dodatkowe zadania (będzie trzeba ich sobie poszukać samemu):
    8. Jakiś bardzo prosty xss. (gotowe)
    9. bardzo proste sqlin (do zrobienia)

# TODO: Zliczanie punktów
# TODO: Pomoc: opis tego jak należy zgłaszać flagi, format flagi
# TODO: Opis podatności/błędów: information disclosure, idor, directory travelsal, ciasteczka, potrzebne narzędzia: przeglądarka, burp 