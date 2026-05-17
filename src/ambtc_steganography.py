import numpy as np
import math
from .ambtc import AMBTC

class AMBTCSteganography:
    def __init__(self, seed=2026, block_size=4):
        self.ambtc = AMBTC(block_size)
        self.seed = seed
        self.block_size = block_size
        self.k = block_size * block_size
        self.b = math.floor(math.log2(self.k + 1))
        self.matrix_p = self._generate_p_matrix()

    def _generate_p_matrix(self):
        np.random.seed(self.seed)
        vals = np.arange(self.k)
        np.random.shuffle(vals)
        return vals.reshape((self.block_size, self.block_size))

    def _text_to_bits(self, text):
        bits = []
        for char in text:
            bits.extend([int(b) for b in format(ord(char), '08b')])
        bits.extend([0] * 8)
        return bits

    def _bits_to_text(self, bits):
        chars = []
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            if len(byte) < 8: break
            val = int("".join(map(str, byte)), 2)
            if val == 0: break
            chars.append(chr(val))
        return "".join(chars)

    def embed(self, image, secret_text):
        bitmaps, hqs, lqs, shape = self.ambtc.compress(image)
        bits = self._text_to_bits(secret_text)
        
        msg_decimals = []
        for i in range(0, len(bits), self.b):
            chunk = bits[i:i+self.b]
            dec = sum(chunk[r] * (2**r) for r in range(len(chunk)))
            msg_decimals.append(dec)
            
        blocks_h, blocks_w = bitmaps.shape[0], bitmaps.shape[1]
        stego_bitmaps = bitmaps.copy()
        
        idx = 0
        for i in range(blocks_h):
            for j in range(blocks_w):
                if idx >= len(msg_decimals): break
                p_base = self.matrix_p * stego_bitmaps[i, j]
                res_dec = 0
                for r in range(self.b):
                    cnt = sum(1 for v in p_base.flatten() if (v >> r) & 1)
                    res_dec += (cnt % 2) * (2**r)
                
                feature = msg_decimals[idx] ^ res_dec
                if feature != 0:
                    pos = np.where(self.matrix_p == feature)
                    stego_bitmaps[i, j, pos[0][0], pos[1][0]] ^= 1
                idx += 1
        return stego_bitmaps, hqs, lqs, shape

    def extract(self, stego_bitmaps, shape):
        blocks_h, blocks_w = stego_bitmaps.shape[0], stego_bitmaps.shape[1]
        extracted_bits = []
        for i in range(blocks_h):
            for j in range(blocks_w):
                p_prime = self.matrix_p * stego_bitmaps[i, j]
                for r in range(self.b):
                    cnt = sum(1 for v in p_prime.flatten() if (v >> r) & 1)
                    extracted_bits.append(cnt % 2)
        return self._bits_to_text(extracted_bits)