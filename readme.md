# Cipher Challenges Write-Up

This repository contains write-ups and proof-of-concept exploits for four challenges. Each challenge focuses on a different vulnerability or cryptographic puzzle. Below is an overview of each challenge, the vulnerability involved, the exploitation method, and the final outcome. Challenges were part of game, rev and cryptography.

---

## Challenge 1: Flag Vault 
Passwordless Vault Exploit (Buffer Overflow)

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

## Challenge 2: Flag Vault 2 
Upgraded Vault with Format String Vulnerability

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

`Flag = THM{format_issue}`

---

## Challenge 3: Order
Repeating-Key XOR Cipher Challenge

**Description:**
A message was intercepted that was encrypted using a repeating-key XOR cipher. Every message always starts with the header "ORDER:".

**Vulnerability/Insight:**
The known plaintext header "ORDER:" allows recovery of the XOR key.
XORing the ciphertext’s first bytes with "ORDER:" recovers the repeating key.

### Exploitation:
Script - [XOR Decryption](Order/xor_decrypt.py)

**Key Recovery:**
XOR the first 6 bytes of ciphertext with "ORDER:" to recover the key. This yields SNEAKY.
Decryption:
Decrypt the full intercepted ciphertext (across both lines) with the key "SNEAKY".
Decrypted Message (Example):

**Outcome:**
The intercepted message reveals Cipher’s next target:

`Flag = THM{the_hackfinity_highschool}`

---

## Challenge 4: Cipher's Secret Message
Shifting Cipher Challenge

**Description:**
An old secret message and its encryption algorithm were recovered. The algorithm shifts each alphabetical character by its index in the plaintext (a position-dependent Caesar cipher).

**Encryption Algorithm (Python snippet):**

```python
def enc(plaintext):
    return "".join(
        chr((ord(c) - (base := ord('A') if c.isupper() else ord('a')) + i) % 26 + base) 
        if c.isalpha() else c
        for i, c in enumerate(plaintext)
    )
```
Note: The message is encrypted using the above function on the flag (FLAG variable).

**Exploitation:**
Decryption: Reverse the process by subtracting the character’s index (mod 26) for letters, while leaving non‑letters unchanged.

Script - [Shifting Decryption](Ciphers_Secret_Message/shifting_decrypt.py)

`Given Ciphertext: a_up4qr_kaiaf0_bujktaz_qm_su4ux_cpbq_ETZ_rhrudm`

`Decrypted Message: a_sm4ll_crypt0_message_to_st4rt_with_THM_cracks`

**Final Flag:**
Wrap the plaintext within the flag format:

`Flag = THM{a_sm4ll_crypt0_message_to_st4rt_with_THM_cracks}`

---

## Challenge 5: The Game – Tetris Hidden Data

**Description:**
Cipher has gone dark, hiding critical secrets inside Tetris—a popular video game. In this challenge, the target was to hack Tetris and uncover encrypted data buried within its code.

**Exploitation:**

By running tools called strings on the Tetris binary and searching for the initials of the flag (e.g., THM{), the flag was located.
Example Command:

```bash
strings tetris | grep "THM{"
```

You can check out the file strings used in the game:- [File Strings](The_game/File_strings.txt)

**Outcome:**
This simple approach revealed the hidden flag embedded within the game’s code.

`Flag = THM{I_CAN_READ_IT_ALL}`
