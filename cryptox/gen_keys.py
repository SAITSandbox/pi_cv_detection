from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Sandbox script to create keys to play around with.

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

private_key_pem = private_key.private_bytes(
   encoding=serialization.Encoding.PEM,
   format=serialization.PrivateFormat.PKCS8,
   encryption_algorithm=serialization.NoEncryption()
)

public_key = private_key.public_key()

public_key_pem = public_key.public_bytes(
   encoding=serialization.Encoding.PEM,
   format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with open('rsa_private.pem', 'wb') as file:
    file.write(private_key_pem)

with open('rsa_public.pem', 'wb') as file:
    file.write(public_key_pem)