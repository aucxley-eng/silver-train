from extensions import seriliazer
from mkg.auth.auth_models.domain_entity.auth_domain import Member
from mkg.auth.auth_models.domain_entity.roles import Role

from marshmallow import fields, validate, validates, ValidationError
import re

class MemberSchema(seriliazer.SQLAlchemyAutoSchema):

    class Meta:
        model         = Member
        load_instance = True

    email = fields.Email(
        required = True,
        validate = validate.Length(max=100)

    )
    username = fields.Str(
        required = True,
        validate = validate.Length(min=2, max=100)

    )
    password = fields.Str(
        required  = True,
        load_only = True,
        validate  = validate.Length(min=8)
    )
    role = fields.Enum(
        Role,
        by_value  = True,
        dump_only = True,
    )
    created_at = fields.DateTime(
        dump_only = True
    )

    @validates("email")
    def validate_email(self, email_value, **_):        
        blocked = {"test.com", "mailinator.com", "guerrillamail.com"}
        domain  = email_value.split("@")[-1].lower()
        if domain in blocked:
            raise ValidationError("Disposable email addresses are not permitted.")
        
    @validates("password")
    def validate_password(self, value, **_):
        if not re.search(r"[A-Z]", value):
            raise ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", value):
            raise ValidationError("Password must contain at least one integer")
        if not re.search(r"[!@#$%^&*]", value):
            raise ValidationError("Password must contaion at least one special character (!@#$%^&*)")

