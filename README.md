# Password Strength Tester

A Python-based password analysis tool that evaluates password security using real-world attack techniques and provides a detailed strength score out of 100, along with suggestions to improve weak passwords.

The purpose of this project is to demonstrate practical cybersecurity concepts such as brute-force resistance, dictionary attacks, and human password behavior in a clear and accessible way.

All analysis is performed locally. Passwords are never stored, logged, or transmitted.

---

## Features

- **Length & Character Diversity Analysis**  
  Evaluates password length and checks for the presence of lowercase letters, uppercase letters, numbers, and special characters.

- **100-Point Strength Scoring System**  
  Assigns a security score from 0 to 100, weighted by entropy, character variety, and detected weaknesses.

- **Brute-Force Time Estimation (GPU Based)**  
  Estimates the time required to crack the password, assuming a SHA-256 hash under an offline attack using an NVIDIA RTX 4070 (5,000 MH/s) under an offline attack model.
  (Note: Brute-force estimates assume a fully random password of equivalent length and character set; real-world cracking time may be significantly lower due to dictionary and pattern-based attacks.)

- **RockYou Dictionary Check**  
  Detects whether the password appears in a known breach wordlist, indicating immediate compromise risk.

  A small sample of the RockYou dataset is included by default for lightweight testing.  
  Users may optionally add their own RockYou files or custom wordlists by placing `.txt` files inside the `rockyou/` directory.

  The program will automatically scan and use all `.txt` files found in that directory.

- **Dictionary Word & Name Detection**  
  Checks whether the password contains common dictionary words or names (including substrings), which significantly reduce effective entropy.

- **Special Character Position Analysis**  
  Identifies predictable symbol placement patterns (e.g. symbols only at the end) that reduce effective password strength.

- **Pattern & Repetition Detection**  
  Flags common weaknesses such as sequential characters and repeated characters.

- **Transparent Score Breakdown**  
  Clearly shows how the final score was calculated, improving educational value and transparency.

- **Actionable Security Feedback**  
  Explains detected weaknesses and suggests changes to improve password strength.

---

## Usage & Example Output

```text
~$: python PST.py
Enter password: BruteThis!


Password Analysis:
- Length: 10
- Lowercase letters: True
- Uppercase letters: True
- Digits: False
- Special characters: True
- Estimated entropy: 63.92 bits

- Contains dictionary word: "this"
- Not found in RockYou dataset

Score Breakdown:
- Length Contribution: +40
- Character Diversity: +20
- Entropy Contribution: +31
- Placement Adjustment: 0
- Dictionary Penalty: -10
- Short Password Penalty: 0
- Numeric Suffix Penalty: 0
- Pattern Penalty: 0

Final Score: 81 / 100
Strength: Strong

Estimated brute-force time (RTX 4070, SHA-256 @ 5000 MH/s): ~55 years (average case)

Suggested Improvements:
- Increase password length to at least 12–14 characters.
- Include numbers that are not simple suffixes.
- Avoid placing special characters only at the end.
- Avoid dictionary words, names, or common phrases.
```

## Disclaimer

This tool is intended for educational and demonstration purposes only.  
Do not test real or sensitive passwords.

