# Password Strength Tester – Scoring Model

This document explains how the 0–100 password strength score is calculated.

The scoring system combines theoretical entropy estimation with practical attack heuristics such as dictionary detection, structural analysis, pattern detection, and breach validation. The goal is to balance mathematical strength with real-world attack behavior.

---

## Entropy Model (Foundation)

The theoretical entropy of a password is calculated as:

H = L × log₂(N)

Where:

- L = password length  
- N = character pool size  

Character pool size is determined by detected character classes:

- +26 if lowercase letters are present  
- +26 if uppercase letters are present  
- +10 if digits are present  
- +32 if special characters are present  

This assumes uniform randomness and equal probability distribution.

Entropy is later scaled before contributing to the final score.

---

## Score Calculation Logic

The final score begins at 0 and is adjusted step-by-step through additive contributions and subtractive penalties.

---

## 1. Length Contribution

For each character:

+4 points per character

Capped at 40 points maximum.

This rewards longer passwords while preventing length from dominating the score.

---

## 2. Character Diversity Contribution

Points are added if the following categories are present:

- +5 if lowercase letters exist  
- +5 if uppercase letters exist  
- +5 if digits exist  
- +10 if special characters exist  

Maximum possible diversity contribution: 25 points.

Special characters are weighted more heavily because they expand the theoretical search space more significantly.

---

## 3. Entropy Contribution

Entropy contributes proportionally:

Entropy contribution = min(floor(H / 2), 40)

Entropy is divided by 2 to prevent exponential growth from overwhelming other scoring factors.

---

## 4. Dictionary Word Penalty

For each detected dictionary word:

−10 points per word detected

This models reduced effective entropy due to predictable language patterns.

---


## 5. Short Password Penalty

If length < 8:

−10 points

Short passwords are highly vulnerable to brute-force attacks.

---

## 6. Numeric Suffix Penalty

If the final character is a digit:

−5 points

This models extremely common password mutation patterns (e.g., "Password1").

---

## 7. Pattern Penalty

- Repeated character sequence (3+ in a row): −10  
- Sequential characters (ascending or descending, 3+): −10  

Each detected pattern subtracts 10 points.

---

## 8. RockYou Breach Override

If the password exactly matches an entry in the RockYou breach dataset:

Final score = 0

This represents immediate real-world compromise regardless of theoretical strength.

---

## Final Bounding

After all additions and penalties, the score is limited to the range 0-100.

---

This hybrid model intentionally combines theoretical entropy with real-world attack simulation to produce a practical and educational strength score.
