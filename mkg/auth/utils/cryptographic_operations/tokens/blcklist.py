
_revoked = set()


def blacklist_jti(jti):
    _revoked.add(jti)


def is_blacklisted(jti):
    return jti in _revoked
