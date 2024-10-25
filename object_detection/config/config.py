from . import sections
from .root import root


class config(root):
    morphology: sections.morphology
    screen_capture: sections.screen_capture
    threshold: sections.threshold
