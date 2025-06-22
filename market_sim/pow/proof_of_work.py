import hashlib
import time

class ProofOfWork:
    def __init__(self, difficulty_bits=20):
        self.difficulty_bits = difficulty_bits
        self.target = 2 ** (256 - difficulty_bits)

    def mine(self, data: str):
        nonce = 0
        start = time.time()
        while True:
            text = f"{data}|{nonce}".encode()
            hash_int = int(hashlib.sha256(text).hexdigest(), 16)
            if hash_int < self.target:
                elapsed = time.time() - start
                return nonce, hash_int, elapsed
            nonce += 1

    def validate(self, data: str, nonce: int):
        text = f"{data}|{nonce}".encode()
        hash_int = int(hashlib.sha256(text).hexdigest(), 16)
        return hash_int < self.target
