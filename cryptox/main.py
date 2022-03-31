from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet
from cryptography.hazmat.backends.openssl.rsa import _RSAPublicKey
import base64


def encrypt(plaintext: str, rsa_pub_key: _RSAPublicKey):
    """Take a plaintext and encrypt it using fernet and then encrypt the
    key using RSA.

    Example of the data:
    {
        "key_cipher": base64 encoded RSA encrypted fernet-key
        "data_cipher": base64 fernet encrypted data
    }
    """
    # Load the RSA key if it has not been passed in the argument
    if type(rsa_pub_key) == str:
        # Assume the given argument is the file name if not the actual key
        with open(rsa_pub_key, "rb") as key_file:
            rsa_pub_key = serialization.load_pem_public_key(
                key_file.read(),
            )

    # Fernet encryption
    key = Fernet.generate_key()
    f = Fernet(key)
    token = f.encrypt(str.encode(plaintext))
    key_cipher = rsa_encrypt(key, rsa_pub_key)
    # Key cipher is the above key encrypted in

    # Manually create a JSON data structure
    # Using [2:-1] to get rid of unwanted chars when converting to string from bytes
    data = "{"
    data += '"key_cipher":' + '"' + str(base64.b64encode(key_cipher))[2:-1] + '",'
    data += '"data_cipher":' + '"' + str(base64.b64encode(token))[2:-1] + '"'
    data += "}"
    # x = json.loads(data)['d']
    # t = base64.b64decode(x)
    # pl = f.decrypt(t)
    # write the data to file
    return data


def rsa_encrypt(data: bytes, public_key_rsa: _RSAPublicKey):
    """Take a string and encrypt it, then save it.
    https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/?highlight=rsa

    :param data: String of dat to be encrypted.
    :param public_key_rsa: RSA public key in _RSAPublicKey class format.
    :returns: RSA ciphertext
    """
    if type(data) == str:
        data = str.encode(data)

    # Create the cipher text
    cipher = public_key_rsa.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return cipher


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
    # Load the RSA public key
    with open('../rsa_public.pem', "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
        )
    print(public_key)
    # rsa_encrypt(dummy_data, 'test.bin', None)
    # print(rsa_decrypt('test.bin'))
    # print(rsa_encrypt(dummy_data, public_key))
    ct = encrypt(dummy_data, public_key)
    print(ct)
