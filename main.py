from PIL import Image
from src.ambtc_steganography import AMBTCSteganography

def main():
    stego = AMBTCSteganography(seed=2026)
    cover = Image.open('assets/cover.png').convert('L')
    
    secret = "Hello"
    stego_bmp, hqs, lqs, shape = stego.embed(cover, secret)
    
    recovered = stego.extract(stego_bmp, shape)
    print(f"Secret message: {recovered}")

    stego_img = stego.ambtc.decompress(stego_bmp, hqs, lqs, shape)
    stego_img.save('output_stego.png')

if __name__ == "__main__":
    main()