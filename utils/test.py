from utils.security import hash_password, verify_password

hashed = hash_password("123456")

print("HASH:", hashed)
print("VERIFY:", verify_password("123456", hashed))