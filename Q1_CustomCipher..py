
# HIT137 Assignment 2 - Question 1

#Group 7
# Member 1: Swojan Singh Maharjan - s401770
# Member 2: Alan Joshi John - s394323
# Member 3: Sandip Kharel - s401293
# Member 4: Haonan Ding - s394323

#!/usr/bin/env python
# coding: utf-8

# In[7]:


"""
Question 1 - Custom Shift Cipher Program
========================================

This program:
1. Reads text from "raw_text.txt"
2. Encrypts the text using the given custom rules
3. Writes the encrypted text to "encrypted_text.txt"
4. Decrypts the encrypted text
5. Writes the decrypted text to "decrypted_text.txt"
6. Verifies whether the decrypted text matches the original text

Important design note:
To make decryption deterministic and successful, each half of the alphabet
is encrypted within its own 13-letter group using modulo 13.

Lowercase groups:
- a-m  -> stays within a-m
- n-z  -> stays within n-z

Uppercase groups:
- A-M  -> stays within A-M
- N-Z  -> stays within N-Z
"""


def encrypt_char(ch: str, shift1: int, shift2: int) -> str:
    """
    Encrypt a single character according to the specified rules.
    """

    # Lowercase letters
    if ch.islower():
        idx = ord(ch) - ord('a')

        # First half: a-m
        if 0 <= idx <= 12:
            shifted_idx = (idx + (shift1 * shift2)) % 13
            return chr(ord('a') + shifted_idx)

        # Second half: n-z
        else:
            second_half_idx = idx - 13
            shifted_idx = (second_half_idx - (shift1 + shift2)) % 13
            return chr(ord('n') + shifted_idx)

    # Uppercase letters
    elif ch.isupper():
        idx = ord(ch) - ord('A')

        # First half: A-M
        if 0 <= idx <= 12:
            shifted_idx = (idx - shift1) % 13
            return chr(ord('A') + shifted_idx)

        # Second half: N-Z
        else:
            second_half_idx = idx - 13
            shifted_idx = (second_half_idx + (shift2 ** 2)) % 13
            return chr(ord('N') + shifted_idx)

    # Other characters remain unchanged
    else:
        return ch


def decrypt_char(ch: str, shift1: int, shift2: int) -> str:
    """
    Decrypt a single character by reversing the encryption rules.
    """

    # Lowercase letters
    if ch.islower():
        idx = ord(ch) - ord('a')

        # First half: a-m
        if 0 <= idx <= 12:
            original_idx = (idx - (shift1 * shift2)) % 13
            return chr(ord('a') + original_idx)

        # Second half: n-z
        else:
            second_half_idx = idx - 13
            original_idx = (second_half_idx + (shift1 + shift2)) % 13
            return chr(ord('n') + original_idx)

    # Uppercase letters
    elif ch.isupper():
        idx = ord(ch) - ord('A')

        # First half: A-M
        if 0 <= idx <= 12:
            original_idx = (idx + shift1) % 13
            return chr(ord('A') + original_idx)

        # Second half: N-Z
        else:
            second_half_idx = idx - 13
            original_idx = (second_half_idx - (shift2 ** 2)) % 13
            return chr(ord('N') + original_idx)

    # Other characters remain unchanged
    else:
        return ch


def encryption_function(shift1: int, shift2: int) -> None:
    """
    Reads from 'raw_text.txt', encrypts its contents,
    and writes the result to 'encrypted_text.txt'.
    """
    try:
        with open("raw_text.txt", "r", encoding="utf-8") as infile:
            original_text = infile.read()

        encrypted_text = "".join(encrypt_char(ch, shift1, shift2) for ch in original_text)

        with open("encrypted_text.txt", "w", encoding="utf-8") as outfile:
            outfile.write(encrypted_text)

        print("[Done] Encryption completed. Output written to 'encrypted_text.txt'.")

    except FileNotFoundError:
        print("[Error] 'raw_text.txt' was not found.")


def decryption_function(shift1: int, shift2: int) -> None:
    """
    Reads from 'encrypted_text.txt', decrypts its contents,
    and writes the result to 'decrypted_text.txt'.
    """
    try:
        with open("encrypted_text.txt", "r", encoding="utf-8") as infile:
            encrypted_text = infile.read()

        decrypted_text = "".join(decrypt_char(ch, shift1, shift2) for ch in encrypted_text)

        with open("decrypted_text.txt", "w", encoding="utf-8") as outfile:
            outfile.write(decrypted_text)

        print("[Done] Decryption completed. Output written to 'decrypted_text.txt'.")

    except FileNotFoundError:
        print("[Error] 'encrypted_text.txt' was not found.")


def verification_function() -> None:
    """
    Compares 'raw_text.txt' and 'decrypted_text.txt'
    and prints whether decryption was successful.
    """
    try:
        with open("raw_text.txt", "r", encoding="utf-8") as original_file:
            original_text = original_file.read()

        with open("decrypted_text.txt", "r", encoding="utf-8") as decrypted_file:
            decrypted_text = decrypted_file.read()

        if original_text == decrypted_text:
            print("[Result] SUCCESS: Decrypted text matches the original text.")
        else:
            print("[Result] FAILURE: Decrypted text does not match the original text.")

            # Show first mismatch for easier debugging
            min_length = min(len(original_text), len(decrypted_text))
            for i in range(min_length):
                if original_text[i] != decrypted_text[i]:
                    print(f"First mismatch at position {i}:")
                    print(f"  Original : {repr(original_text[i])}")
                    print(f"  Decrypted: {repr(decrypted_text[i])}")
                    break

            if len(original_text) != len(decrypted_text):
                print("The file lengths are also different.")

    except FileNotFoundError:
        print("[Error] Verification could not be completed because one or both files are missing.")


def get_positive_integer(prompt: str) -> int:
    """
    Repeatedly asks the user for a positive integer until valid input is entered.
    """
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("Please enter a positive integer greater than 0.")
        except ValueError:
            print("Invalid input. Please enter an integer.")


def main() -> None:
    """
    Main driver function.
    """
    print("=" * 60)
    print("           Custom Shift Cipher Program")
    print("=" * 60)

    # Step 1: Prompt the user for shift values
    shift1 = get_positive_integer("Enter shift1: ")
    shift2 = get_positive_integer("Enter shift2: ")

    # Step 2: Encrypt the contents of raw_text.txt
    encryption_function(shift1, shift2)

    # Step 3: Decrypt the encrypted file
    decryption_function(shift1, shift2)

    # Step 4: Verify whether the decrypted file matches the original
    verification_function()

    print("=" * 60)


# In[ ]:


if __name__ == "__main__":
    main()


# In[ ]:




