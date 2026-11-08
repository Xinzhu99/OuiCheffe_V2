from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()   # argon2

def get_hashed_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed_pass: str) -> bool:
    return password_hash.verify(password, hashed_pass)