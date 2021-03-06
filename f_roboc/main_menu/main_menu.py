"""Interface of the main menu."""

from f_roboc.interface import Interface

from f_roboc.main_menu.sprites import SpritesController
from f_roboc.main_menu.events import EventsController


class MainMenu(Interface):
    """Main menu's main class."""

    def __init__(self, images, connection, error=False):
        """Init."""
        super().__init__()

        # NAME
        self.name = 'main_menu'

        # CONNECTION
        self.connection = connection

        # SPRITES AND EVENTS
        self.sprt = SpritesController(images)
        self.events = EventsController(self.sprt.button_list,
                                       self.sprt.lost_connexion)

        # BOOLEAN GAME STATUS
        self._game_init = False

        # SHOW ERROR CONNECTION IF ERROR
        if error:
            self.sprt.lost_connexion.activated = True

    def start_events(self, event, mouse):
        """Call of events."""
        self.events.start(event, mouse, self._game_init)

    @Interface._secured_connection
    def transfer_datas(self):
        """Connect to the server and try to know if a game is running."""
        if not self._is_timer_over(100):
            return

        if not self.connection.connected:
            self.connection.connect()

        elif not self._game_init:
            self._ask_if_game_init_is_running()

    def _ask_if_game_init_is_running(self):
        """Ask to the server if a game is in initialization.

        If it is, _game_init will be True.
        """
        msg = self.connection.receive()
        if 'game_init_yes' in msg:
            self._game_init = True
            return

        self.connection.send('is_game_init')

    def update(self):
        """Sprite update."""
        self._refresh_timer()

        self.go_to = self.events.go_to
        if self.go_to == "game_init":
            self.connection.send('joining_game')

        if not self.sprt.lost_connexion.activated:
            self.sprt.button_list.update(self._game_init)
        self.sprt.background.update()
        self.sprt.lost_connexion.update()

    def draw(self):
        """Sprite drawing."""
        self.sprt.main_surface.blit(self.sprt.background.image, (0, 0))
        self.sprt.button_list.draw(self.sprt.main_surface)

        if self.sprt.lost_connexion.activated:
            self.sprt.main_surface.blit(self.sprt.lost_connexion.image, (0, 0))
