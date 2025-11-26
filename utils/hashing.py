from passlib.context import CryptContext

# Password hashing using Argon2 (strongest option)
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

class Hash:
    @staticmethod
    def hash(password: str) -> str:
        """
        Hash a plain text password using Argon2.
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        """
        Verify that a plain password matches the hashed one.
        """
        return pwd_context.verify(plain_password, hashed_password)
