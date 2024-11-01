# -*- coding: utf-8 -*-
"""
@author: UnicornOnAzur

This script dynamically imports modules, installing them if they are not
already present. It utilizes the importlib and subprocess modules to achieve
this functionality while handling potential errors.
"""
# Standard library
import importlib
import subprocess
import sys
import typing
import warnings
# Mapping of common package names to their installable counterparts. The key is
# the import name and the value is the install name.
PACKAGE_MAP: dict = {"bs4": "beautifulsoup4",
                     "dateutil": "python-dateutil",
                     "flask_sqlalchemy": "Flask-SQLAlchemy",
                     "PIL": "Pillow",
                     "sklearn": "scikit-learn",
                     "werkzeug": "Flask"
                     }


def _get_package_name(module_name: str, package: str = None) -> str:
    """


    Parameters
    ----------
    module_name : str
        The name of the module.
    package : str, optional
        The package name if the module is part of a package. The default is
        None.

    Raises
    ------
    TypeError
        If the module name starts with a dot and no package is provided.

    Returns
    -------
    str
        The resolved package name.

    """
    # if it is a relative import check if package is supplied
    if module_name.startswith("."):
        # raise an error if no package is supplied
        if not package:
            raise TypeError(
                "Package must be provided when name starts with a dot.")
        package_name: str = package.split(".")[0]
    else:
        package_name: str = module_name.split(".")[0].strip()
        if not package_name:
            raise TypeError("Module name cannot be resolved.")
    return PACKAGE_MAP.get(package_name, package_name)


def _pip_install_package(package: str) -> bool:
    """
    Install a package using pip.

    Parameters
    ----------
    package : str
        The name of the package to install.

    Returns
    -------
    bool
        True if the installation was successful, False otherwise.

    """
    try:
        subprocess.check_call([sys.executable,
                               "-m", "pip", "install",
                               package])
        return True
    except subprocess.CalledProcessError as e:
        warnings.warn(f"Failed to install package '{package}': {e}",
                      UserWarning)
        return False
    except FileNotFoundError:
        warnings.warn("Pip might not be installed. Please install pip to use this function.",  # noqa E501
                      UserWarning)
        return False


def import_module(name: str, package: str = None,
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

    Returns
    -------
    typing.Optional[typing.types.ModuleType]
        The imported module or None if the import fails.

    """
    try:
        return importlib.import_module(name, package=package)
    except ModuleNotFoundError:
        print(f"Module '{name}' not found. Attempting to install...")
        package_name: str = _get_package_name(name, package=package)
        # Check if installation was successful
        if _pip_install_package(package_name):
            return import_module(name, package=package)

        warnings.warn(
            f"Installation of module '{name}' failed. Cannot import.",
            UserWarning)
        return None


def demo():
    pass


if __name__ == "__main__":
    demo()
