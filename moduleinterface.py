import inspect
from abc import ABC, abstractmethod, abstractproperty
from typing import Tuple
import pandas as pd


class ModuleInterface(ABC):
    """
    Interface for swat cup modules. Use this as a parent class for your modules. You mus timplement the abstractmethods,
    while the others are optional.
    """

    @abstractmethod
    def get_version(self) -> str:
        """
        Returns the module version
        """
        pass

    @abstractmethod
    def sufi2_pre(self, path: str) -> None:
        """
        Returns the path tho swat executable in linux
        """
        pass

    @abstractmethod
    def sufi2_run(self, path: str) -> None:
        """
        Returns the path tho swat executable in linux
        """
        pass

    @abstractmethod
    def sufi2_post(self, path: str) -> None:
        """
        Returns the path tho swat executable in linux
        """
        pass

    def load_backup(self) -> None:
        self._not_implemented_error()

    def _not_implemented_error(self):
        """
        Raises exception when method is not implemented
        """
        raise Exception("Method '" + inspect.stack()[1].function + "' not implemented. Check module.")
