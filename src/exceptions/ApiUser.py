class UserDoestNotExists(Exception):
    pass
class PasswordDoesNotMatch(Exception):
    pass
class RevokedTokenException(Exception):
    pass