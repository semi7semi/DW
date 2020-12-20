# WFB_Django v2 (DW) - Heroku deploy

## Aplikacja do Warhamera/T9A
### Changelog
1. Dodawanie do DB jednostek. <br>
2. Symulowanie walki. <br>
3. Wynikiem jest ilosc zadanych ran. <br>
4. Dodany CSS
5. ModelForm dla edycji i dodawania jednostek
6. Dodane brakujace modele.
7. Dodawanie uzytkownika
8. Ranking
9. Dodawanie wyniku
10. Edycja rankingu

## Opis

Aplikacja bedzie dostepna dla zalogowanych i nie zalogowanych uzytkownikow.

Aplikacja bedzie sluzyla do prowadzenia rankingu wewnatrzklubowego, zliczanie punktow z bitew (Warhammer / The Ninth Age),
Druga funkcionalnosc to bedzie kalkulator do symulowania wyniku walki.
Uzytkownicy beda mogli przegladac ranking, dodawac wyniki i kozystac z kalkulatora.
Zalogowani beda mogli dodawac nowe jednostki do bazy w kalkulatorze.

### Widoki:
* Index - strona glowna z wyswietlonym menu i 5 najlepszymi graczami w rankingu, lista graczy, nowy gracz, ranking, kalkulator<br>
* RankingList - widok z pelnym rankingiem, mozliwosc sortowania i dodania nowego wyniku, szczegoly gracza <br>
* Calc - formularz obslugujacy sumulacje walki, podajemy dane wejsciowe i otrzymujemy wynik. <br>
* List - lista wszsytkich jednostek utworzynych przez uzytkownikow <br>
* LoginView - logowanie <br>
* LogoutView - wylogowanie <br>
* UsersList - list wszsytkich graczy <br>
* CreateUserView - dodaj nowego gracza do rankingu <br>

dla zalogowanych: <br>
* EditUnitView - edycja charakterystyk jednostek <br>
* AddUnitView - dodawnie nowych jednostek <br>
* EditUserView - edytuj dane uzytkownika, email, armia <br>
* AddGameResultView - dodawanie nowego wyniku do rankingu <br>
* EditGameResultView - edycja wyniku w rankingu <br>


### Baza Danych:

User (django.auth) - <br>

Profile - <br>
* user - (j:j z User) <br>
* usr_army - Char, choices <br>

GameResults - <br>
* game_rank(char), 3 mozliwosci choices=("master", "local", "home")
* battle_points(int), <br>
* objective(bool), <br>
* objective_type(char, choices), <br>
* user(foreinkey do User)<br>
* oponenet(char), imie przeciwnika <br>
* date(date), data dodania wyniku <br>

Armys - <br>
* name(char) <br>
* short_name(char) <br>
* description(text) [Definicja frakcji / rasy, jest 12]<br>

Units - <br>
* name(str), <br>
* off, str, ap, reflex (4 charakterystyki potrzebna do kalkulatora(int, int, int, int)), <br>
* army (foreinkey do Army (kazda Armia moze miec wiele Jednostek)),<br>

Objectives - <br>
* name(char, choices(6 mozliwosci))<br>



