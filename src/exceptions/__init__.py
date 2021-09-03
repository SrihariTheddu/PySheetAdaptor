

class BuildError(RuntimeError):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"Couldn't build the Environment for dir ::{self.message}"


class AuthenticationError(RuntimeError):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"Authentication Failed ::{self.message}"

class TransitionException(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"couldn't transit {self.message}"



























