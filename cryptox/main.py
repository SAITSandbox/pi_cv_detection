from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def aes256_encrypt(data: str, filename: str):
    """Take a string and encrypt it, then save it.

    :param data: String of dat to be encrypted.
    :param filename: String of the file name to be saved.
    :returns:
    """
    # Encode the str data into bytes
    data = str.encode(data)
    key = get_random_bytes(32)
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    file_out = open(filename, "wb")
    [ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
    file_out.close()



if __name__ == "__main__":
    dummy_data = "{'test': 'hello world'}"
    aes256_encrypt(dummy_data, 'test.bin')
    