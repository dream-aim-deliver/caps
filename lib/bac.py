from abc import ABC
import logging


class BaseAbstractClass(ABC):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def __repr__(self):
        return f"{__name__}"

    def __str__(self):
        return f"{__name__}"
