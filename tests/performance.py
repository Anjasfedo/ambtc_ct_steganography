import numpy as np
import math
import requests
from PIL import Image
from io import BytesIO
from src.ambtc_steganography import AMBTCSteganography

def calculate_psnr(base_img, target_img):
    mse = np.mean((base_img.astype(float) - target_img.astype(float)) ** 2)
    if mse == 0:
        return float('inf'), 0
    max_pixel = 255.0
    psnr = 20 * math.log10(max_pixel / math.sqrt(mse))
    return psnr, mse

def run_benchmark():
    image_urls = {
        "Lena": "https://raw.githubusercontent.com/Anjasfedo/Cover-Image-Steganography/main/01.lena.png",
        "Baboon": "https://raw.githubusercontent.com/Anjasfedo/Cover-Image-Steganography/main/02.Baboon.png",
        "Splash": "https://raw.githubusercontent.com/Anjasfedo/Cover-Image-Steganography/main/03.Splash.png",
        "Airplane": "https://raw.githubusercontent.com/Anjasfedo/Cover-Image-Steganography/main/04.Airplane.png",
        "Sailboat": "https://raw.githubusercontent.com/Anjasfedo/Cover-Image-Steganography/main/05.Sailboat.png",
        "Peppers": "https://raw.githubusercontent.com/Anjasfedo/Cover-Image-Steganography/main/06.Peppers.png"
    }

    stego_engine = AMBTCSteganography(seed=2026)
    # Fill capacity (65536 bits / 8 = 8192 characters)
    test_message = "A" * 8192 

    print("Comparison: AMBTC Compressed vs. Stego Image")
    print(f"{'Image':<12} | {'MSE':<10} | {'PSNR (dB)':<10} | {'Capacity (bits)':<15}")
    print("-" * 55)

    for name, url in image_urls.items():
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content)).convert('L')
            
            # 1. Generate Pure AMBTC Compressed Image
            pure_bmp, pure_hqs, pure_lqs, shape = stego_engine.ambtc.compress(img)
            pure_ambtc_img = np.array(stego_engine.ambtc.decompress(pure_bmp, pure_hqs, pure_lqs, shape))
            
            # 2. Generate Stego Image
            stego_bmp, st_hqs, st_lqs, _ = stego_engine.embed(img, test_message)
            stego_img = np.array(stego_engine.ambtc.decompress(stego_bmp, st_hqs, st_lqs, shape))
            
            # 3. Compare Stego vs Pure AMBTC
            psnr, mse = calculate_psnr(pure_ambtc_img, stego_img)
            
            blocks_h, blocks_w = stego_bmp.shape[0], stego_bmp.shape[1]
            capacity = blocks_h * blocks_w * stego_engine.b
            
            print(f"{name:<12} | {mse:<10.4f} | {psnr:<10.4f} | {capacity:<15}")
        except Exception as e:
            print(f"Failed to process {name}: {e}")

if __name__ == "__main__":
    run_benchmark()