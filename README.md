### Podstawowe zadania:
    1. Flaga ukryta w źródle strony
    2. Aby zdobyć flagę będzie trzeba się zalogować, dane do logowania będą na stronie w komentarzu, 
    login w pliku strony, hasło w czymś dodatkowym
    3. Flaga ukryta w źródle strony, ale zakodowane w base64
    4. Prosty IDOR np lista postów i jeden "ukryty"
    5. Jakiś błąd z directory traversal
    6. Ciasteczko z polem admin 0, zmiana na 1 i po odświeżeniu dostanie się flagę
    7. Strona posiada pole tekstowe, atakujący ma zapytać sie o flagę wtedy ją dostanie, jednak słowo będzie to blokowane na froncie, będzie musiał zmodyfikować sobie request, gdy już to zrobi w odpowiedzi nie dostanie flagi pytanie czy to na pewno wszystkie

### Dodatkowe zadania (będzie trzeba ich sobie poszukać samemu):
    8. Jakiś bardzo prosty xss
    9. bardzo proste sqlin