from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def rsa_encrypt(data: str, filename: str, public_key_file: str):
    """Take a string and encrypt it, then save it.
    https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/?highlight=rsa

    :param data: String of dat to be encrypted.
    :param filename: String of the file name to be saved.
    :returns:
    """
    # Encode the str data into bytes
    data = str.encode(data)

    if public_key_file is None:
        public_key_file = "rsa_public.pem"

    # Load the RSA public key
    with open(public_key_file, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
        )
    # Create the cipher text
    cipher = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    file_out = open(filename, "wb")
    file_out.write(cipher)
    file_out.close()

def rsa_decrypt(filename: str) -> str:
    """Sandbox function for testing"""
    with open("rsa_private.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    with open(filename, 'rb') as file:
        ciphertext = file.read()

    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext



if __name__ == "__main__":
    dummy_data = "{'test': 'hello world'}"
    rsa_encrypt(dummy_data, 'test.bin', None)
    print(rsa_decrypt('test.bin'))
