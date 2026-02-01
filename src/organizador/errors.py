class OrganizadorError(Exception):
    """Base error for this project."""


class InvalidPathError(OrganizadorError):
    pass


class NothingToUndoError(OrganizadorError):
    pass
