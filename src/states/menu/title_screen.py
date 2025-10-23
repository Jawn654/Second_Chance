import pygame as pg

import src.states.menu.menus as menus
from .menus import StartMenu
from .menus import UsernamePrompt
from ..state import State
import redditwarp.SYNC

class TitleScreen(State):
    """State for the title screen."""

    def __init__(self):
        client = redditwarp.SYNC.Client()
        m = next(client.p.subreddit.pull.top('Temple', amount=1, time='day'))
        super().__init__("ForestBackground.png")

        self.title_logo = pg.image.load("assets/backgrounds/title_logo.png")
        self.title_logo = pg.transform.scale(self.title_logo, (450, 250))

        self.reddit_title = pg.font.Font(None, 36).render(m.title, True, "white")
        self.reddit_post = pg.font.Font(None, 36).render(m.permalink, True, "white")

        # Load background music
        pg.mixer.music.load('assets/music/titlescreenmusic.mp3')
        # Set initial volume
        self.volume = menus.volume  # Initial volume level (between 0 and 1)
        pg.mixer.music.set_volume(menus.volume)
        pg.mixer.music.play(-1)  # Start playing background music on a loop

    def handle_events(self, events: list[pg.event.Event]):
        for event in events:
            if event.type != pg.KEYDOWN:
                return
            if event.key == pg.K_RETURN:
                if self.game.username == "":
                    self.manager.set_state(UsernamePrompt)
                else:
                    self.manager.set_state(StartMenu)

    def draw(self):
        super().draw()
        self.screen.blit(
            pg.font.Font(None, 36).render("Press 'Enter' to start", True, "white"),
            (self.screen.get_width() / 2, self.screen.get_height() - 100)
        )
        self.screen.blit(self.title_logo, (170, 150))
        self.screen.blit(self.reddit_title, (10, 10))
        self.screen.blit(self.reddit_post, (10, 50))

