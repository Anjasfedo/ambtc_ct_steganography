import unittest
import numpy as np
from PIL import Image
from src.ambtc_steganography import AMBTCSteganography

class TestAMBTCSteganography(unittest.TestCase):
    def setUp(self):
        self.seed = 2026
        self.stego = AMBTCSteganography(seed=self.seed)
        # Membuat gambar dummy 64x64
        self.dummy_img = Image.fromarray(np.random.randint(0, 255, (64, 64), dtype=np.uint8))

    def test_integrity(self):
        """Memastikan pesan yang diekstrak sama dengan pesan yang disisipkan"""
        original_message = "Testing 123!"
        st_bmp, hqs, lqs, shape = self.stego.embed(self.dummy_img, original_message)
        recovered_message = self.stego.extract(st_bmp, shape)
        
        self.assertEqual(original_message, recovered_message)

    def test_wrong_seed(self):
        """Memastikan pesan tidak bisa dibaca jika seed salah"""
        original_message = "Secret"
        st_bmp, hqs, lqs, shape = self.stego.embed(self.dummy_img, original_message)
        
        # Gunakan stego engine dengan seed berbeda
        attacker_stego = AMBTCSteganography(seed=9999)
        wrong_message = attacker_stego.extract(st_bmp, shape)
        
        self.assertNotEqual(original_message, wrong_message)

    def test_capacity_limit(self):
        """Memastikan sistem menangani pesan yang melebihi kapasitas"""
        blocks = (64 // 4) * (64 // 4)
        max_chars = (blocks * 4) // 8
        huge_message = "X" * (max_chars + 100)
        
        # Seharusnya tidak error, hanya memotong pesan sesuai kapasitas
        st_bmp, hqs, lqs, shape = self.stego.embed(self.dummy_img, huge_message)
        recovered = self.stego.extract(st_bmp, shape)
        self.assertTrue(len(recovered) <= max_chars)

if __name__ == "__main__":
    unittest.main()