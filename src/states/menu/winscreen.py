import pygame as pg
from PIL import Image
from ..state import State


class WinScreen(State):
    """State for the win screen."""

    def __init__(self):
        super().__init__()
        self.frames = []
        self.frame_durations = []
        self.current_frame = 0
        self.last_update = pg.time.get_ticks()


        gif = Image.open("assets/backgrounds/YIPPEE.gif")
        for frame in range(gif.n_frames):
            gif.seek(frame)
            frame_surface = pg.image.fromstring(
                gif.tobytes(), gif.size, gif.mode
            ).convert()
            frame_surface = pg.transform.scale(frame_surface, self.screen.get_size())
            self.frames.append(frame_surface)
            duration = gif.info.get("duration", 100)
            self.frame_durations.append(duration)

    def handle_events(self, events: list[pg.event.Event]):
        from .title_screen import TitleScreen
        for event in events:
            if event.type != pg.KEYDOWN:
                return
            if event.key == pg.K_RETURN:
                self.manager.set_state(TitleScreen)

    def draw(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_durations[self.current_frame]:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = now


        frame = self.frames[self.current_frame]
        self.screen.blit(frame, (0, 0))
        self.screen.blit(
            pg.font.Font(None, 36).render("You win!", True, "black"),
            (self.screen.get_width() / 2, self.screen.get_height() - 100)
        )
