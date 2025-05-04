import json
import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

class EncryptionManager:

    def get_user_input() -> list[str]:
        # TODO: Add some error-handling in here...
        username = str(input('Enter Carleton username: '))
        password = str(input('Enter Carleton password: '))
        return [username, password]
    
    def credentials_padder(credentials: list[str]) -> list[str]:
        PADDER = padding.PKCS7(128).padder()
        PADDED_USERNAME = PADDER.update(credentials[0]) + PADDER.finalize()
        PADDED_PASSWORD = PADDER.update(credentials[1]) + PADDER.finalize()
        return [PADDED_USERNAME, PADDED_PASSWORD]

    def encrypt_credentials(credentials: list[str]):
        # 256-bit AES key
        KEY = os.urandom(32)
        # 16-byte IV for AES
        IV = os.urandom(16)

        # Encrypt the credentails
        CIPHER = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
        ENCRYPTOR = CIPHER.encryptor()
        ENCRYPTED_DATA = [
            ENCRYPTOR.update(credentials[0]) + ENCRYPTOR.finalize(),
            ENCRYPTOR.update(credentials[1]) + ENCRYPTOR.finalize()
        ]

        # Encode encrypted data under base64 to be able to store in JSON
        DECODE_FORMAT = 'utf-8'
        JSON_DATA = {
            "username": base64.b64encode(ENCRYPTED_DATA[0]).decode(DECODE_FORMAT),
            "password": base64.b64encode(ENCRYPTED_DATA[1]).decode(DECODE_FORMAT),
            "key": base64.b64encode(KEY).decode(DECODE_FORMAT),
            "iv": base64.b64encode(IV).decode(DECODE_FORMAT)
        }

        # Write data to cridentials.json
        with open('cridentials.json', 'w') as output_destination:
            json.dump(JSON_DATA, output_destination, indent=4)
        print('Encrypted data written to cridentials.json')
    
    # TODO: Write a decryption algorithm to be able to retrieve the plaintext