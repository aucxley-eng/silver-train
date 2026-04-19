import enum


class Role(str, enum.Enum):
    """
    Inheriting str means SQLAlchemy stores the human-readable label
    ("guest", "member", "admin") so the DB column is readable without
    a join and safe to query with raw SQL.
    """
    
    GUEST  = "guest"
    MEMBER = "member"
    ADMIN  = "admin"
