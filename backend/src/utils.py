from typing import Any

from typeguard import typechecked


@typechecked
def reassign_module_names(package_name: str, locals_: dict[str, Any]) -> None:
    """Reassign the `__module__` attribute of objects to the current package.

    This function iterates through all local objects and adjusts their
    `__module__` attribute if it starts with the name of the current module.
    This ensures that objects are displayed as part of the current package.

      Parameters
    ----------
    package_name : str
        The name of the current package to assign to the `__module__` attribute
        of relevant objects.

    locals_ : dict[str, Any]
        A dictionary representing the local objects.

    Notes
    -----
    This is particularly useful for dynamically created objects or objects
    imported from other modules that need to appear as if they belong to the
    current package.

    Examples
    --------
    >>> reassign_module_names()
    """
    for value in list(locals_.values()):
        if getattr(value, "__module__", "").startswith(package_name):
            value.__module__ = package_name
