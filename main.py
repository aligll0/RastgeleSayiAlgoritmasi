import hashlib
import os
import time

class SecureRNG:
    """
    Kriptografik Olarak Güvenli Sözde Rastgele Sayı Üreteci (CSPRNG).
    SHA-256 Hash Chaining ve OS Entropisi kullanır.
    """
    def __init__(self):
        self.state = os.urandom(32)
        self.reseed_counter = 0

    def _reseed(self):
        new_entropy = os.urandom(32)
        timestamp = str(time.time_ns()).encode()
        self.state = hashlib.sha256(self.state + new_entropy + timestamp).digest()
        self.reseed_counter = 0

    def generate_bytes(self, n):
        """n bayt uzunluğunda rastgele veri üretir."""
        result = b''
        while len(result) < n:
            self.reseed_counter += 1
            if self.reseed_counter > 1000: # Her 1000 üretimde bir zorunlu reseed
                self._reseed()
            
            # State'i güncelle ve çıktı üret
            self.state = hashlib.sha256(self.state + str(self.reseed_counter).encode()).digest()
            result += self.state
            
        return result[:n]

    def get_int(self, min_val, max_val):
        """Belirli bir aralıkta tam sayı üretir."""
        range_size = max_val - min_val + 1
        byte_len = (range_size.bit_length() + 7) // 8
        random_bytes = self.generate_bytes(byte_len)
        random_int = int.from_bytes(random_bytes, 'big')
        return min_val + (random_int % range_size)

if __name__ == "__main__":
    rng = SecureRNG()
    print("Rastgele Sayı (1-100):", rng.get_int(1, 100))
    print("Rastgele Hex (32 char):", rng.generate_bytes(16).hex())
    