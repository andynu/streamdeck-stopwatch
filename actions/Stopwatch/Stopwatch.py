import time
from math import floor
from PIL import Image, ImageDraw

from src.backend.DeckManagement.InputIdentifier import Input, InputEvent
from src.backend.PluginManager.ActionBase import ActionBase


def create_elapsed_ring(percentage, size=(200, 200), ring_color=(50, 205, 50), ring_thickness=15):
    """Create a progress ring that fills up as time elapses."""
    image = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    outer_bbox = [ring_thickness // 2, ring_thickness // 2,
                  size[0] - ring_thickness // 2, size[1] - ring_thickness // 2]

    if percentage >= 1:
        draw.ellipse(outer_bbox, fill=(0, 0, 0, 0), width=ring_thickness, outline=ring_color)
    elif percentage > 0:
        end_angle = percentage * 360
        draw.arc(outer_bbox, start=-90, end=-90 + end_angle, fill=ring_color, width=ring_thickness)

    return image


class Stopwatch(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start_time = None
        self.paused_time = None
        self.accumulated = 0  # seconds accumulated before current run

    def get_elapsed_time(self) -> float:
        if self.start_time is None:
            return self.accumulated

        if self.paused_time is not None:
            return self.accumulated + (self.paused_time - self.start_time)

        return self.accumulated + (time.time() - self.start_time)

    def show(self) -> None:
        elapsed = self.get_elapsed_time()

        hours = int(elapsed / 3600)
        minutes = int((elapsed - hours * 3600) / 60)
        seconds = int(elapsed - hours * 3600 - minutes * 60)

        if hours > 0:
            time_string = f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            time_string = f"{minutes:02}:{seconds:02}"

        self.set_center_label(time_string)

        # Ring fills up over 60 seconds, then resets
        ring_pct = (elapsed % 60) / 60
        ring = create_elapsed_ring(floor(ring_pct * 100) / 100,
                                   ring_color=(50, 205, 50),
                                   ring_thickness=15)
        self.set_media(image=ring)

    def on_ready(self) -> None:
        self.on_tick()

    def on_tick(self) -> None:
        self.show()

    def event_callback(self, event: InputEvent, data) -> None:
        if event in (Input.Key.Events.SHORT_UP, Input.Dial.Events.SHORT_UP, Input.Dial.Events.SHORT_TOUCH_PRESS):
            if self.start_time is None:
                # Start
                self.start_time = time.time()
                self.paused_time = None
            else:
                if self.paused_time is None:
                    # Pause
                    self.paused_time = time.time()
                else:
                    # Resume
                    self.accumulated += (self.paused_time - self.start_time)
                    self.start_time = time.time()
                    self.paused_time = None

        elif event in (Input.Key.Events.HOLD_START, Input.Dial.Events.HOLD_START, Input.Dial.Events.LONG_TOUCH_PRESS):
            # Reset
            self.start_time = None
            self.paused_time = None
            self.accumulated = 0

        else:
            return
        self.show()
