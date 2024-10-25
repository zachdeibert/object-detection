from . import sections
from .root import root


class config(root):
    screen_capture: sections.screen_capture
    threshold: sections.threshold
