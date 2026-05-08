class UserAlreadyExistsException(Exception):
    pass


class DatabaseException(Exception):
    pass


class GuestNotFoundException(Exception):
    pass


class demographicsNotFound(Exception):
    pass


class reportIdNotFound(Exception):
    pass


class reportNotFound(Exception):
    pass


class reportNotAllowed(Exception):
    pass
