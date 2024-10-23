# -*- coding: utf-8 -*-
"""
@author: UnicornOnAzur


"""
import importlib
import subprocess
import sys
import typing
import warnings


def _pip_install_package(name: str) -> bool:
    """
    Install a package using pip.

    Parameters
    ----------
    name : str
        The name of the package to install.

    Returns
    -------
    bool
        True if the installation was successful, False otherwise.

    """
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', name])
        return True
    except subprocess.CalledProcessError as e:
        warnings.warn(f"Failed to install package '{name}': {e}", UserWarning)
        return False
    except FileNotFoundError:
        warnings.warn(
            "Pip might not be installed. Please install pip to use this function.",
            UserWarning)
        return False


def import_module(name: str,
                  package: str = None,
                  retries: int = 2
                  ) -> typing.Optional[typing.types.ModuleType]:
    """
    Import a module, installing it if not found.

    Parameters
    ----------
    name : str
        The name of the module to import.
    package : str, optional
        The package name if the module is part of a package. The default is
        None.
    retries : int, optional
        The number of retries for importing the module. The default is 2.

    Returns
    -------
    typing.Optional[typing.types.ModuleType]
        The imported module or None if the import fails.

    """
    if retries <= 0:
        warnings.warn(
            "Maximum retries reached without success for module import.",
            UserWarning)
        return None
    try:
        return importlib.import_module(name, package=package)
    except ModuleNotFoundError:
        print(f"Module '{name}' not found. Attempting to install...")
        if _pip_install_package(name):  # Check if installation was successful
            return import_module(name, package=package, retries=retries - 1)
        else:
            warnings.warn(
                f"Installation of module '{name}' failed. Cannot import.",
                UserWarning)
            return None
    except (TypeError, ValueError, ImportError) as e:
        warnings.warn(f"Error importing module '{name}': {e}", UserWarning)
        return None


def demo():
    pass


if __name__ == "__main__":
    demo()
