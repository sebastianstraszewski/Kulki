# Gra w kulki napisana w Pythonie

### ZASADY GRY
- Gra jest jednoosobowa,
- Gra odbywa się na planszy złożonej ze 100 pól ( 10×10 pól),
- Istnieje 5 rodzajów kul (kulka1, kulka2, kulka3, kulka4, kulka5),
- Na początku komputer w losowych punktach plaszy umiesza 50 wylosowanych kul,

Następnie rozpoczyna się rozgrywka:
- Użytkownik, klikając myszką, zmienia położenie wybranej przez siebie kuli na inne (wskazane przez siebie) puste pole,
- Jeśli 5 kul o identycznym kolorze tworzy linię (pionową, poziomą, lub ukośną) to zostają usunięte z planszy,
- Komputer losuje trzy nowe kule, umieszcza je w losowo wybranych wolnych polach,
  
Ilość zdobytych punktów równa jest ilości ruchów wykonanych przez gracza (liczba przestawionych przez niego kul).

> #### Uwaga
> Kule można przestwiać na dowolne puste pole.

<br></br>
### INTERFEJS
- Pojedyncze pole planszy ma wielkość 40×40 pikseli,
- Obrazek wczytany do pola planszy ma wielkość 35×35 pikseli,
- Pojedyncze pole zaimplementowane jest jako Gtk.ToggleButton,
- Po lewej stronie u góry, program wyświetla aktualną liczbę punktów,
- Po lewej stronie, program wyświetla listę rankingową, która zawiera 5 najlepszych wyników (lub mniej, jeśli odbyło się mniej rozgrywek), posortowanych od największego,
- Przycisk "Graj od początku" może zostać wciśnięty w każdej chwili i resetuje rozgrywkę.

<br></br>
### MECHANIKA GRY
Przebieg rozgrywki można przedstawić następująco:
- losujemy 50 kul,
- ustawiamy licznik punktów zdobytych przez gracza na 0,
- dopóki na planszy istnieją puste pola, kolejno:
  * użytkownik przestawia kulę,
  * zwiększamy ilość punktów zdobytych przez gracza o 1
  * jeśli kule o tym samym kolorze tworzą linię składającą się z 5 kul to usuwamy je,
  * losujemy trzy nowe kule (jeśli na planszy zostało mniej miejsc wolnych to losujemy mniej kul),
  * jeśli kule o tym samym kolorze tworzą linię składającą się z 5 kul to usuwamy je,
- uaktualniamy listę rankingową

> #### Uwaga
> Program musi używać przygotowanych obrazków kul (kulka1, kulka2, kulka3, kulka4, kulka5) i wczytuje je z katalogu w którym znajduje się plik programu (tzn. katalogu bieżącego).
