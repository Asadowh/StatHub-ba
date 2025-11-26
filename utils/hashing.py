from passlib.context import CryptContext

# Create a password hashing context using bcrypt
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class Hash:
    @staticmethod
    def bcrypt(password: str):
        """
        Hash a plain text password using bcrypt.
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify(plain_password: str, hashed_password: str):
        """
        Verify that a plain password matches the hashed one.
        """
        return pwd_context.verify(plain_password, hashed_password)
