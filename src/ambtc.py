import numpy as np
from PIL import Image

class AMBTC:
    def __init__(self, block_size=4):
        self.block_size = block_size

    def compress(self, image):
        img_arr = np.array(image, dtype=np.float32)
        h, w = img_arr.shape
        k = self.block_size * self.block_size
        blocks_h, blocks_w = h // self.block_size, w // self.block_size
        
        bitmaps = np.zeros((blocks_h, blocks_w, self.block_size, self.block_size), dtype=np.uint8)
        hqs = np.zeros((blocks_h, blocks_w), dtype=np.uint8)
        lqs = np.zeros((blocks_h, blocks_w), dtype=np.uint8)
        
        for i in range(blocks_h):
            for j in range(blocks_w):
                r_s, r_e = i * self.block_size, (i + 1) * self.block_size
                c_s, c_e = j * self.block_size, (j + 1) * self.block_size
                block = img_arr[r_s:r_e, c_s:c_e]
                
                mean = np.mean(block)
                std_dev = np.std(block)
                bitmap = (block >= mean).astype(np.uint8)
                q = np.sum(bitmap)
                
                if q == 0 or q == k:
                    hq = lq = np.round(mean)
                else:
                    hq = np.round(mean + std_dev * np.sqrt((k - q) / q))
                    lq = np.round(mean - std_dev * np.sqrt(q / (k - q)))
                
                bitmaps[i, j] = bitmap
                hqs[i, j] = np.clip(hq, 0, 255)
                lqs[i, j] = np.clip(lq, 0, 255)
                
        return bitmaps, hqs, lqs, (h, w)

    def decompress(self, bitmaps, hqs, lqs, img_shape):
        h, w = img_shape
        blocks_h, blocks_w = h // self.block_size, w // self.block_size
        recon = np.zeros((h, w), dtype=np.uint8)
        for i in range(blocks_h):
            for j in range(blocks_w):
                r_s, r_e = i * self.block_size, (i + 1) * self.block_size
                c_s, c_e = j * self.block_size, (j + 1) * self.block_size
                recon[r_s:r_e, c_s:c_e] = np.where(bitmaps[i, j] == 1, hqs[i, j], lqs[i, j])
        return Image.fromarray(recon)