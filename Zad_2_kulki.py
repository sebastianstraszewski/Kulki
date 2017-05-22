#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

# losowanie kul
import random

# wymagamy biblioteki w wersji min 3.0
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from gi.repository import GdkPixbuf


class GameBoard(Gtk.Grid):
    """Klasa implementujaca plansze gry."""

    def __init__(self, parent, size):
        """ Konstruktor tworzacy plansze do gry.

        Parameters:
            parent  - odnosnik do klasy, ktora utworzyla plansze, wykorzystywany
                      w celu wywolania funkcji move_ball po kliknieciu w pole
            size    - rozmiar planszy
        """
        Gtk.Grid.__init__(self)

        self.parent = parent
        self.size = size

        # Zmienna przechowujaca przyciski bedace polami planszy
        self.fields = []

        # utworzenie pol planszy
        self.generate_board()

    def generate_board(self):
        """ Metoda generujaca plansze."""

        # tworzenie pól planszy
        for i in xrange(self.size):
            self.fields.append([])

            for j in xrange(self.size):
                b = Gtk.ToggleButton()
                b.set_size_request(40, 40)
                self.fields[i].append(b)
                self.attach(b, i, j, 1, 1)
                self.handle_id = b.connect("clicked", self.clicked, i, j)

        self.set_column_homogeneous(True)
        self.set_row_homogeneous(True)

    def clicked(self, button, x, y):
        """ Metoda wywolywana w momencie gdy wcisnieto pole."""
        field = (x, y)

        # wywolanie metody move_ball z mechaniki gry ktora znajduje sie
        # w klasie App
        self.parent.move_ball(field)

    # ponizsze metody odpowiednio blokuja i odblokowuja
    # mozliwosc klikania w pole. Napisalem je by w mechanice gry
    # bylo bardziej czytelne, co sie dzieje z polem na planszy
    def lock_field(self, field, is_locked):
        """ Metoda pozwalajaca na zmiande mozliwosc klikania w pole.

        Parameters:
            field - tupla w postaci (x, y) przechowujaca pozycje przycisku
            is_active - zmienna typu True/False
                True jezeli pole ma byc odblokowane
                False jezeli pole ma byc zablokowane
        """
        x = field[0]
        y = field[1]

        # zmiana mozliwosci klikania w pole
        self.fields[x][y].set_sensitive(is_locked)

    def active_field(self, field, is_active):
        """Metoda ustawiajaca aktywnosc pola.

        Aktywnosc pola oznacza czy pole ma byc zaznaczone jako wybrane (aktywne

        Parameters:
            field - tupla w postaci (x, y) przechowujaca pozycje pola
            is_active - zmienna typu True/False
                True jezeli pole ma byc aktywne,
                False jezeli pole ma bycnieaktywne

        """
        x = field[0]
        y = field[1]

        # zablokowanei sygnalu by nie zostala wywolana metoda clicked
        self.fields[x][y].handler_block_by_func(self.clicked)
        # zmiana aktywnosci pola
        self.fields[x][y].set_active(is_active)
        # odblokowanie sygnalu
        self.fields[x][y].handler_unblock_by_func(self.clicked)

    def reset_field(self, field):
        """ Metoda resetujaca wlasnosci pola na planszy.

        Parameters:
            field - tupla w postaci (x, y) przechowujaca pozycje pola
        """

        x = field[0]
        y = field[1]

        # usuniecie obrazka kuli z pola
        if self.fields[x][y].get_image() is not None:
            self.fields[x][y].get_image().clear()

        # umozliwienie klikania w pole
        self.fields[x][y].set_sensitive(True)

    # Ta funkcja robi to samo co powyzsza ale na wszystkich polach
    def reset_board(self):
        """ Metoda resetujaca plansze."""

        for row in self.fields:
            for button in row:
                if button.get_image() is not None:
                    button.get_image().clear()
                button.set_sensitive(True)

    def set_ball(self, field, texture):
        """ Metoda wstawia na wybrane pole, kule o wybranej teksturze.

        Parameters:
            field   - tupla w postaci (x, y) przechowujaca pozycje pola
            texture - tekstura typu Gtk.Pixbuff
        """

        x = field[0]
        y = field[1]

        ball_image = Gtk.Image()
        ball_image.set_from_pixbuf(texture)
        ball_image.show()

        self.fields[x][y].set_image(ball_image)


class App(Gtk.Window):
    """Klasa implementujaca okno oraz mechanike gry."""

    def __init__(self):
        """ Konstruktor tworzacy nowe okno gry i ustawiajacy rozgrywke."""

        Gtk.Window.__init__(self)

        # ustawienie tytulu okna oraz rozmiaru
        self.set_title("Kulki")
        self.set_default_size(250, 250)

        self.connect("delete-event", Gtk.main_quit)

        box = Gtk.VBox()

        # utworzenie label z aktualnym wynikiem
        self.score_lbl = Gtk.Label()
        self.score_lbl.set_markup("Liczba punktów: <b>0</b>")
        self.score_lbl.set_alignment(0, 0.5)

        box.pack_start(self.score_lbl, False, False, 0)

        # utworzenie label z najelpszymi wynikami
        self.high_scores_lbl = Gtk.Label("<b>Ranking:</b>")
        self.high_scores_lbl.set_justify(Gtk.Justification.CENTER)
        self.high_scores_lbl.set_use_markup(True)
        self.high_scores_lbl.set_alignment(0, 0)

        box2 = Gtk.HBox()

        box2.pack_start(self.high_scores_lbl, False, False, 0)

        # ustawienie gry
        self.setup_game()

        # utworzenie planszy rozgrywki
        self.game_board = GameBoard(self, self.size)

        box2.pack_end(self.game_board, True, True, 0)

        box.pack_start(box2, True, True, 0)

        # utworzenie przycisku "Nowa gra"
        self.n_game_btn = Gtk.Button.new_with_label("Graj od poczatku")
        self.n_game_btn.connect("clicked", self.new_game)

        box.pack_end(self.n_game_btn, True, True, 0)

        self.add(box)

        # wylosowanie kul
        self.randomize_balls()

        self.show_all()

    # implementacja mechaniki gry

    # W tej metodzie znajduja sie zmienne, dzieki ktorym mozna
    # zmienic wlasciwosci gry
    def setup_game(self):
        """Metoda ustawiajaca wlasciwosci gry."""

        # zmienna przechowujaca rozmiar planszy
        self.size = 10

        # zmienna przechowujaca ilosc tekstur
        # musi byc zgodna z iloscia plikow tekstur w folderze
        self.num_of_tex = 5

        # lista zawierajaca wczytane z pliku tekstury kulek
        self.ball_tex = []

        # wczytanie tekstur z plikow
        self.read_balls()

        # ile kul ma byc wylosowanych na poczatku gry
        self.start_balls = 50

        # po ile kul ma byc usuwanych
        self.del_balls = 5

        # po ile kul ma byc dodawanych na kazdy ruch
        self.add_balls = 3

        # slownik przechowujacy zajete pola przez kule
        self.busy_fields = dict()

        # zmienna przechowujaca texture wybranej kuli
        self.ball_selected = None

        # zmienna przechowujaca tekst na labelce score_lbl
        self.score_txt = "Liczba punktów: <b>{}</b>"

        # zmienna przechowujaca aktualna liczbe punktow
        self.score = 0

        # ile maksymalnie najlepszych wynikow ma byc wyswietlonych
        self.max_high_scores_len = 5

        # zmienna przechowujaca tekst na labelce high_scores_lbl
        self.high_scores_txt = "<b>Ranking:</b>\n"

        # lista 5 najlepszych wynikow
        self.high_scores = []

    def high_scores_update(self):
        """Metoda aktualizujaca pole z najlepszymi wyniki."""

        tmp = self.high_scores_txt

        # dodanie aktualnego wyniku listy najlepszych wynikow
        self.high_scores.append(self.score)

        # usuniecie duplikatow z listy
        self.high_scores = list(set(self.high_scores))

        # posortowanie wynikow
        self.high_scores.sort(reverse=True)

        # zapamietanie maksymalnie 5 najlepszych wynikow
        self.high_scores = self.high_scores[0:self.max_high_scores_len]

        # utworzenie napisu do wyswietlenia
        for i in xrange(len(self.high_scores)):
            tmp += "<b>{}.</b> {}\n".format(i + 1, self.high_scores[i])

        # wyswietlenie napisu na labelce
        self.high_scores_lbl.set_markup(tmp)

    def read_balls(self):
        """ Metoda wczytujaca tekstury z plikow."""

        for i in xrange(1, self.num_of_tex + 1):
            file_name = "kulka{}.svg".format(i)
            ball_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(file_name, 35, 35)
            self.ball_tex.append(ball_pixbuf)

    def new_game(self, button):
        """ Metoda tworzaca nowa rozgrywke."""

        # czyszczenie slownika
        self.busy_fields.clear()

        # czyszczenie planszy
        self.game_board.reset_board()

        # wylosowanie poczatkowych kul
        self.randomize_balls()

        # aktualizacja listy rankingowej
        self.high_scores_update()

        # reset aktualnego wyniku i aktualizacja labeli
        self.score = 0

        # wyswietlenie wyniku na labelce
        self.score_lbl.set_markup(self.score_txt.format(self.score))

    def randomize_ball(self):
        """Funkcja losujaca pojedyncza kule.

        Return:
            -1 - gdy wszystkie pola zostana zajete i nie ma mozliwosci dodania
                nowej kulki
            0  - w przeciwnym przypadku
        """

        while len(self.busy_fields) < self.size ** 2:
            # losowanie pola
            field = (random.randint(0, self.size - 1),
                     random.randint(0, self.size - 1))

            # losowanie numeru tekstury
            tex_id = random.randint(0, self.num_of_tex - 1)

            # wyjscie z petli w momencie wylosowania
            # nowej kuli, ktora nie znajduje sie w slowniku
            # oraz dodanie jej do slownika
            if field not in self.busy_fields:
                # wstawienie nowej kuli do slownika
                self.busy_fields.update({field: tex_id})
                # wstawienie nowej kuli na plansze
                self.game_board.set_ball(field, self.ball_tex[tex_id])

                break

        # sprawdzenie czy sa jeszcze wolne pola
        # jezeli nie to wyswietlenie komunikatu o przegranej
        # oraz aktualizacja najlepszych wynikow
        if len(self.busy_fields) >= self.size ** 2:
            self.set_title("PRZEGRANA!")

            # utworzenie okna popup z informacja o przegranej
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.OK, "PRZEGRANA")
            dialog.run()

            dialog.destroy()

            # zablokowanie pol z kulami
            [self.game_board.lock_field(fi, False) for fi in self.busy_fields.keys()]

            return -1
        return 0

    def randomize_balls(self):
        """Funkcja losujaca poczatkowe ustawienie kul."""

        for i in xrange(self.start_balls):
            self.randomize_ball()

        self.del_five()

    def move_ball(self, field):
        """ Funkcja wywolywana gdy zostanie wybrane pole.

        Funkcja ta odpowiedzialna jest za przesuniecie kuli,
        oraz dodanie nowych kul przy kazdym ruchu uzytkownika
        """
        if field in self.busy_fields:
            # zapisanie polozenia i tekstury wybranej kuli
            self.ball_selected = [field,
                                  self.busy_fields[field]]

            # wyrzucenie kuli z listy zajetych pol
            del self.busy_fields[field]

            # wyczyszczenie przycisku kuli
            self.game_board.reset_field(field)

            # ustawienie pola jako aktywne w celu
            # udostepnienia mozliwosci odlozenia kuli w te
            # samo miejsce co byla
            self.game_board.active_field(field, False)

            # zablokowanie pol z kulami
            [self.game_board.lock_field(fi, False) for fi in self.busy_fields.keys()]

        else:
            # ustawienie pola jako aktywnego w razie
            # gdyby uzytkownik sie rozmyslil
            self.game_board.active_field(field, False)

            if self.ball_selected is not None:
                # wyczyszczenie przycisku kuli
                self.game_board.reset_field(field)

                # dodanie kuli do listy zajetych pol
                self.busy_fields[field] = self.ball_selected[1]

                # wstawienie kuli na plansze
                tex = self.ball_tex[self.ball_selected[1]]
                self.game_board.set_ball(field, tex)

                # odblokowanie pol z kulami
                [self.game_board.lock_field(fi, True) for fi in self.busy_fields.keys()]

                # aktualizacja wyniku i wyswietlenie na labelce
                # ale tylko wtedy gdy przestawiono kule
                if field != self.ball_selected[0]:
                    # aktualizacja wyniku i wyswietlenie na labelce
                    self.score += 1
                    self.score_lbl.set_markup(self.score_txt.format(self.score))

                    # usuniecie ewentualnych dopasowan kul
                    self.del_five()

                    # wylosowanie 3 nowych kul
                    for _ in xrange(0, self.add_balls):
                        if self.randomize_ball() == -1:
                            break

                    # usuniecie ewentualnych dopasowan kul po dodaniu 3 nowych
                    self.del_five()

                self.ball_selected = None

    def del_five(self):
        """ Metoda odpowiedzialna za usuwanie kul znajdujacych sie obok siebie."""

        for x in xrange(0, self.size):
            for y in xrange(0, self.size):
                # utworzenie list z wzorcami kulek
                # odpowiednio w rzedzie kolumnie i na skos
                row_pattern = []
                column_pattern = []
                crosswise_left_pattern = []
                crosswise_right_pattern = []

                for i in xrange(0, self.del_balls):
                    row_pattern.append((x + i, y))
                    column_pattern.append((x, y + i))
                    crosswise_left_pattern.append((x + i, y + i))
                    crosswise_right_pattern.append((x + i, y - i))

                patterns = [row_pattern, column_pattern, crosswise_left_pattern, crosswise_right_pattern]

                # iterujac po wszystkich dostepnych wzorcach
                # sprawdzam ile kul zgadza sie z aktualnie sprawdzanym polem
                # i jezeli jest ona rowna ilosci pol do usuniecia (self.del_balls)
                # usuwam wszystkie dopasowane kule
                for pattern in patterns:
                    ball_matched = 0
                    for field in pattern:
                        if self.busy_fields.get(field, -1) == self.busy_fields.get((x, y)):
                            ball_matched += 1

                    if ball_matched == self.del_balls:
                        for field in pattern:
                            del self.busy_fields[field]
                            self.game_board.reset_field(field)


if __name__ == "__main__":
    a = App()
    Gtk.main()
