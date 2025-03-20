# Cipher Challenges Write-Up

This repository contains write-ups and proof-of-concept exploits for four challenges. Each challenge focuses on a different vulnerability or cryptographic puzzle. Below is an overview of each challenge, the vulnerability involved, the exploitation method, and the final outcome. Challenges were part of game, rev and cryptography.

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
```


**Outcome:**
If the payload is crafted with the correct offset, the vault’s check is bypassed and the flag from flag.txt is printed.

`Flag = THM{password_0v3rfl0w}`

---

## Challenge 2: Upgraded Vault with Format String Vulnerability

**Description:**
The vault program was upgraded so that the flag is no longer printed. Instead, it now mocks the user by calling:

```c
printf(username);
```
This introduces a classic format string vulnerability because the unsanitized user input is used directly as a format string.

**Vulnerability:**

Format String Exploit: By supplying format specifiers (e.g., %7$s), the attacker can leak data from the stack—including the flag stored in a local variable.
Exploitation:
Iterate through different offsets to locate the stack slot containing the flag. For instance, sending %7$s, %8$s, etc., as the username may reveal the flag.

Example Automation Script (Python 2.7):

**Outcome:**
Once the correct offset is found, the output will include the flag leaked from the stack.
