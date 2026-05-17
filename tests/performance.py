import numpy as np
import math
import requests
from PIL import Image
from io import BytesIO
from src.ambtc_steganography import AMBTCSteganography

def calculate_psnr(original, stego):
    mse = np.mean((original.astype(float) - stego.astype(float)) ** 2)
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
    # Gunakan pesan panjang untuk mengisi kapasitas maksimal (65536 bit / 8 = 8192 karakter)
    test_message = "A" * 8000 

    print(f"{'Image':<12} | {'MSE':<10} | {'PSNR (dB)':<10} | {'Capacity (bits)':<15}")
    print("-" * 55)

    for name, url in image_urls.items():
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content)).convert('L')
            img_arr = np.array(img)
            
            stego_bmp, hqs, lqs, shape = stego_engine.embed(img, test_message)
            stego_img = stego_engine.ambtc.decompress(stego_bmp, hqs, lqs, shape)
            stego_arr = np.array(stego_img)
            
            psnr, mse = calculate_psnr(img_arr, stego_arr)
            
            # Hitung kapasitas berdasarkan total blok x b
            blocks_h, blocks_w = stego_bmp.shape[0], stego_bmp.shape[1]
            capacity = blocks_h * blocks_w * stego_engine.b
            
            print(f"{name:<12} | {mse:<10.4f} | {psnr:<10.4f} | {capacity:<15}")
        except Exception as e:
            print(f"Failed to process {name}: {e}")

if __name__ == "__main__":
    run_benchmark()