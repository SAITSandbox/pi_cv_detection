import json
import cryptox

with open('data/1.json', 'r') as file:
    cc = json.load(file)

ciphertext = cryptox.encrypt(
    plaintext=json.dumps(cc),
    rsa_pub_key='rsa_public.pem'
)

# Save the encrypted data into file
with open("data/tt.bin", 'w') as file:
    json.dump(ciphertext, file)

with open("data/tt.bin", 'r') as file:
    dd = json.load(file)
