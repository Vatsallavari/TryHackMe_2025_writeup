#!/usr/bin/env python3

def decrypt(ciphertext):
    plaintext = ""
    for i, c in enumerate(ciphertext):
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            # Reverse the shift by subtracting the index (mod 26)
            plaintext += chr((ord(c) - base - i) % 26 + base)
        else:
            plaintext += c
    return plaintext

def main():
    # Provided ciphertext for the shifting cipher challenge.
    ciphertext = "a_up4qr_kaiaf0_bujktaz_qm_su4ux_cpbq_ETZ_rhrudm"
    plaintext = decrypt(ciphertext)
    
    print("Decrypted message:")
    print(plaintext)

if __name__ == "__main__":
    main()
