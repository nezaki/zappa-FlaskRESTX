
class NotFound(Exception):
    pass


class Conflict(Exception):
    pass


class Unauthorized(Exception):
    pass


class Forbidden(Exception):
    pass


class BadRequest(Exception):
    def __init__(self, errors):  # noqa
        self.errors = errors
