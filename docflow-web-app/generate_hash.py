from werkzeug.security import generate_password_hash

default_password = "default_password" # Replace with your actual default password
hashed = generate_password_hash(default_password)
print(hashed)
