#!/usr/bin/env python3
import sys

def repeating_key_xor_decrypt(ciphertext_bytes, key):
    plaintext = bytearray()
    for i, b in enumerate(ciphertext_bytes):
        plaintext.append(b ^ key[i % len(key)])
    return bytes(plaintext)

def main():
    # The intercepted ciphertext provided as a hex string (two lines)
    hex_ciphertext = (
        "1c1c01041963730f31352a3a386e24356b3d32392b6f6b0d323c22243f6373"
        "1a0d0c302d3b2b1a292a3a38282c2f222d2a112d282c31202d2d2e24352e60"
    )
    
    # Remove any spaces/newlines if present and convert to bytes.
    hex_ciphertext = hex_ciphertext.replace("\n", "").replace(" ", "")
    ciphertext = bytes.fromhex(hex_ciphertext)
    
    # Known plaintext header "ORDER:"
    known_header = b"ORDER:"
    
    # Recover the key by XORing the first few ciphertext bytes with the known header.
    key = bytearray()
    for i in range(len(known_header)):
        key.append(ciphertext[i] ^ known_header[i])
    key = bytes(key)
    
    print("Recovered key:", key)
    
    # Decrypt the full ciphertext using the recovered key.
    plaintext = repeating_key_xor_decrypt(ciphertext, key)
    try:
        decoded = plaintext.decode("utf-8")
    except UnicodeDecodeError:
        decoded = plaintext.decode("utf-8", errors="replace")
    print("\nDecrypted message:")
    print(decoded)

if __name__ == "__main__":
    main()
