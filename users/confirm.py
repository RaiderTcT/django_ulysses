from itsdangerous import URLSafeTimedSerializer as usts
import base64
from django_ulysses import settings as django_settings

class Token:

    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.encodebytes(security_key.encode())

    def generate_validate_token(self, username):
        serializer = usts(self.security_key)
        return serializer.dumps(username, self.salt)

    def confirm_validate_token(self, token, expiration=3600):
        serializer = usts(self.security_key)
        return serializer.loads(token, salt=self.salt, max_age=expiration)

    def remove_validate_token(self, token):
        """验证不通过删除用户"""
        serializer = usts(self.security_key)
        print(serializer.loads(token, salt=self.salt))
        return serializer.loads(token, salt=self.salt)

token_confirm =Token(django_settings.SECRET_KEY)
