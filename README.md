# Password Strength Tester

A Python-based password analysis tool that evaluates password security using real-world attack techniques and provides a detailed strength score out of 100, along with suggestions to improve weak passwords.

The purpose of this project is to demonstrate practical cybersecurity concepts such as brute-force resistance, dictionary attacks, and human password behavior in a clear and accessible way.

Passwords are analyzed locally only; they are never stored, logged, or transmitted.

---

## Features

- **Length & Character Diversity Analysis**  
  Evaluates password length and checks for the presence of lowercase letters, uppercase letters, numbers, and special characters.

- **100-Point Strength Scoring System**  
  Assigns a security score from 0 to 100, weighted by entropy, character variety, and detected weaknesses.

- **Brute-Force Time Estimation (GPU Based)**  
  Estimates the time required to crack the password, assuming the password hash is SHA-256 and is being attacked using an NVIDIA RTX 4070 (5,000 MH/s) under an offline attack model.
  (Note: Brute-force estimates assume a fully random password of equivalent length and character set; real-world cracking time may be significantly lower due to dictionary and pattern-based attacks.)

- **RockYou Dictionary Check**  
  Detects whether the password appears in the `rockyou.txt` password list, indicating immediate compromise risk.

- **Dictionary Word & Name Detection**  
  Checks whether the password contains common dictionary words or names (including substrings), which significantly reduce effective entropy.

- **Special Character Position Analysis**  
  Identifies predictable symbol placement patterns (e.g. symbols only at the end) that reduce effective password strength.

- **Pattern & Repetition Detection**  
  Flags common weaknesses such as sequential characters (`1234`), repeated characters (`aaa`), and keyboard patterns (`qwerty`, `asdf`).

- **Actionable Security Feedback**  
  Explains detected weaknesses and suggests changes to improve password strength.

---

## Usage & Example Output

```text
~$: python PST.py
Enter password: Hackme1

Password Strength: Very Weak
Score: 18 / 100

- Password is too short
- Contains dictionary word: "hack"
- Capitalized dictionary word detected
- Predictable digit suffix ("1")
- No special characters detected
- Password not found in common breach datasets

Estimated brute-force time (RTX 4070, SHA-256): ~2 hours (average)

Suggested Improvements:
- Increase password length to at least 12 characters
- Avoid dictionary words or common phrases
- Add special characters in non-predictable positions
- Avoid simple digit suffixes

```

## Disclaimer

This tool is intended for educational and demonstration purposes only.  
Do not test real or sensitive passwords.

