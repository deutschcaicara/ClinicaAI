from cryptography.fernet import Fernet

ENCRYPTION_KEY = 'IpmmvITSPLun5m6lOtUPHszQ7yTKRlmAHQ9JC47XMKg='
cipher_suite = Fernet(ENCRYPTION_KEY)

# Substitua pelos valores reais
db_password = 'Mouse2250@#86'

encrypted_db_password = cipher_suite.encrypt(db_password.encode()).decode()

print(f'Encrypted DB_PASSWORD: {encrypted_db_password}')