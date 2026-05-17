# AMBTC Steganography based on Combination Theory

This repository provides a pure Python implementation of the AMBTC-based steganography method using Combination Theory. Unlike traditional pixel-domain steganography, this method operates within the compressed domain of Absolute Moment Block Truncation Coding (AMBTC).

---

### Academic Attribution

This code is an independent implementation of the following research:

**"A Robust and High-Capacity Coverless Information Hiding Based on Combination Theory"** by Kurnia Anggriani, Shu-Fen Chiou, Nan-I Wu, and Min-Shiang Hwang (2023).

DOI: [10.20944/preprints202304.0341.v1](https://doi.org/10.20944/preprints202304.0341.v1)

---

### How it Works
1. **AMBTC Compression**: The cover image is compressed into bitplanes and quantizer values (High/Low).
2. **Combination Theory Mapping**: A pseudo-random Matrix P is generated using a shared seed.
3. **Parity Modification**: Secret bits are embedded by flipping at most one bit per 4x4 block to match the desired parity of the block's features.

![Result Comparison](assets/Result%20Comparison.png)

---

### Experimental Results (Base Implementation)
The following results were obtained using 4x4 blocks (4 bits/block) on 512x512 grayscale images:

| Image    | MSE      | PSNR (dB) | Capacity (bits) |
|----------|----------|-----------|-----------------|
| Lena     | 33.3143  | 32.9045   | 65,536          |
| Baboon   | 142.7971 | 26.5836   | 65,536          |
| Splash   | 14.6467  | 36.4734   | 65,536          |
| Airplane | 44.6739  | 31.6303   | 65,536          |
| Sailboat | 76.0594  | 29.3193   | 65,536          |
| Peppers  | 34.9454  | 32.6969   | 65,536          |

---

### Requirements

* Python 3.x
* NumPy
* Pillow (PIL)
* Requests

### Usage

1. **Quickstart Demo** Run the main script to demonstrate the embedding and extraction process using the message "Hello" on the Lena image.
```bash
python main.py

```


2. **Performance Benchmarking** Use this script to replicate the experimental results table (MSE, PSNR, and Capacity) across 6 standard test images (Lena, Baboon, Splash, etc.).
```bash
python -m tests.performance

```


3. **Unit Testing** Run the test suite to ensure all functions are operating correctly, including data integrity checks and key (seed) security validation.
```bash
python test_all.py

```

---

*Developed for academic research purposes. Last updated May 2026.*
