# web_poker

### Odtwarzanie bazy danych

Po sklonowaniu repozytorium i zainstalowaniu SQLite3, uruchom następujące polecenie, aby odtworzyć bazę danych:

```bash
sqlite3 my_database.db < my_database.sql
```

### Uwaga dotycząca kodowania plików SQL

Jeśli podczas importowania pliku SQL pojawią się błędy związane z nieprawidłowymi znakami (np. błąd: "Parse error near line 1: near '??P': syntax error"), problem może wynikać z nieodpowiedniego kodowania pliku. W niektórych przypadkach plik może być zapisany w kodowaniu innym niż UTF-8 (np. UTF-16), co powoduje problemy z odczytem przez SQLite.

Aby rozwiązać ten problem, należy przekonwertować plik SQL na kodowanie **UTF-8**. Poniżej znajdują się kroki i komendy, które można użyć w systemach Linux/macOS oraz Windows:

#### Linux/macOS

1. Sprawdź aktualne kodowanie pliku:
   ```bash
   file db.sql
   ```
2.
```bash
iconv -f UTF-16 -t UTF-8 db.sql > db_utf8.sql


