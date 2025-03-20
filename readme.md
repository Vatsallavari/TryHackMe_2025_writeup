# Cipher Challenges Write-Up

This repository contains write-ups and proof-of-concept exploits for four challenges provided by Cipher. Each challenge focuses on a different vulnerability or cryptographic puzzle. Below is an overview of each challenge, the vulnerability involved, the exploitation method, and the final outcome.

---

## Challenge 1: Passwordless Vault Exploit (Buffer Overflow)

**Description:**  
A C program implements a vault that uses a disabled password prompt. The program reads the username using the insecure `gets()` function into a 100-byte buffer. Although the password prompt is commented out, a local variable holds the hardcoded password `5up3rP4zz123Byte`.

**Vulnerability:**  
- **Buffer Overflow:** The use of `gets()` allows an attacker to overflow the `username` buffer and overwrite the adjacent `password` variable.
- **Null Byte Injection:** Injecting a null byte after the correct username (`bytereaper`) forces the `strcmp()` in the login function to succeed.

**Exploitation:**  
Construct an input payload as follows:
- **Username:** `"bytereaper"` (10 bytes)
- **Null Byte:** `\x00` (1 byte)  
- **Filler:** Approximately 89–93 filler characters (to pad the 100-byte buffer; adjust based on memory alignment)
- **Password Overwrite:** `"5up3rP4zz123Byte"`
- **Newline:** A terminating newline to complete the input

**Example Exploit Command:**  
```bash
python3 -c 'import sys; sys.stdout.buffer.write(b"bytereaper\x00" + b"A"*93 + b"5up3rP4zz123Byte" + b"\n")' | nc 10.10.211.90 1337
