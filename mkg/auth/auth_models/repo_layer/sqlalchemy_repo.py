from extensions import db
from mkg.auth.auth_models.domain_entity.auth_domain import Member


class MemberRepository:
 
    def get_by_id(self, Member_id: int) -> Member | None:
        return db.session.get(Member, Member_id)
 
    def get_by_email(self, email: str) -> Member | None:
        return Member.query.filter_by(email=email).first()
 
    def get_by_username(self, username: str) -> Member | None:
        return Member.query.filter_by(username=username).first()
 
    def get_all(self) -> list[Member]:
        return Member.query.order_by(Member.id).all()
 
    def save(self, Member: Member) -> Member:
        db.session.add(Member)
        db.session.commit()
        return Member
 
    def commit(self) -> None:
        db.session.commit()
