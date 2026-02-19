import math
from rockyou_config import ROCKYOU_FILES

# get password
def get_password():
    return input("Enter password: ")

# analyze length and character type
def analyze_characters(password):
    analysis = {
        "length": len(password),
        "lowercase": False,
        "uppercase": False,
        "digits": False,
        "special": False,
    }

    for char in password:
        if char.islower():
            analysis["lowercase"] = True
        elif char.isupper():
            analysis["uppercase"] = True
        elif char.isdigit():
            analysis["digits"] = True
        else:
            analysis["special"] = True

    return analysis

# analyze character placement patterns
def analyze_placement(password):
    length = len(password)

    middle_upper = False
    middle_special = False
    special_positions = []
    upper_positions = []

    for i, char in enumerate(password):
        if char.isupper():
            upper_positions.append(i)
            if 1 < i < length - 1:
                middle_upper = True

        if not char.isalnum():
            special_positions.append(i)
            if 1 < i < length - 2:
                middle_special = True

    return {
        "middle_upper": middle_upper,
        "middle_special": middle_special,
        "special_positions": special_positions,
        "upper_positions": upper_positions
    }

# detect repeated characters and sequential patterns
def analyze_patterns(password):
    repeated = False
    sequential = False

    repeat_count = 1
    for i in range(1, len(password)):
        if password[i] == password[i - 1]:
            repeat_count += 1
            if repeat_count >= 3:
                repeated = True
        else:
            repeat_count = 1

    for i in range(len(password) - 2):
        a, b, c = password[i], password[i + 1], password[i + 2]

        if a.isalnum() and b.isalnum() and c.isalnum():
            if ord(b) == ord(a) + 1 and ord(c) == ord(b) + 1:
                sequential = True
            if ord(b) == ord(a) - 1 and ord(c) == ord(b) - 1:
                sequential = True

    return {
        "repeated": repeated,
        "sequential": sequential
    }

# load smaller wordlists into memory
def load_wordlist(filepath):
    words = set()
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                word = line.strip().lower()
                if len(word) >= 3:
                    words.add(word)
    except FileNotFoundError:
        print(f"[!] Wordlist not found: {filepath}")
    return words

# check large breach files line-by-line
def check_large_wordlist(password, filepath):
    password_lower = password.lower()
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                if password_lower == line.strip().lower():
                    return True
    except FileNotFoundError:
        print(f"[!] Wordlist not found: {filepath}")
    return False

# detect dictionary words inside password
def find_dictionary_words(password, wordlists):
    password_lower = password.lower()
    matches = []

    for word in wordlists:
        if word and word in password_lower:
            matches.append(word)

    matches.sort(key=len, reverse=True)

    filtered = []
    for word in matches:
        if not any(word in kept for kept in filtered):
            filtered.append(word)

    return filtered

# calculate theoretical entropy
def calculate_entropy(password, analysis):
    pool_size = 0

    if analysis["lowercase"]:
        pool_size += 26
    if analysis["uppercase"]:
        pool_size += 26
    if analysis["digits"]:
        pool_size += 10
    if analysis["special"]:
        pool_size += 32

    if pool_size == 0:
        return 0

    return len(password) * math.log2(pool_size)

# estimate brute-force cracking time
def estimate_bruteforce_time(entropy):
    if entropy <= 0:
        return "Instantly"

    hash_rate = 5_000_000_000

    total_guesses = 2 ** entropy
    average_guesses = total_guesses / 2
    seconds = average_guesses / hash_rate

    return format_time(seconds)

def format_time(seconds):
    if seconds < 1:
        return "< 1 second"

    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24
    years = days / 365

    if seconds < 60:
        return f"{round(seconds)} seconds"
    elif minutes < 60:
        return f"{round(minutes)} minutes"
    elif hours < 24:
        return f"{round(hours)} hours"
    elif days < 365:
        return f"{round(days)} days"
    else:
        rounded_years = round(years)
        if rounded_years < 100_000:
            return f"{rounded_years:,} years"
        else:
            return f"{years:.2e} years"

# generate actionable suggestions
def generate_suggestions(password, analysis, placement, patterns, found_words, rockyou_hit):
    suggestions = []

    if rockyou_hit:
        suggestions.append("Do not use passwords found in breach datasets.")

    if analysis["length"] < 12:
        suggestions.append("Increase password length to at least 12–14 characters.")

    if not analysis["special"]:
        suggestions.append("Add special characters in non-predictable positions.")

    if not analysis["uppercase"]:
        suggestions.append("Include uppercase letters beyond the first position.")

    if not analysis["digits"]:
        suggestions.append("Include numbers that are not simple suffixes.")

    if placement["special_positions"] and all(
        pos >= analysis["length"] - 2 for pos in placement["special_positions"]
    ):
        suggestions.append("Avoid placing special characters only at the end.")

    if password and password[-1].isdigit():
        suggestions.append("Avoid predictable numeric suffixes.")

    if patterns["repeated"]:
        suggestions.append("Avoid repeated character sequences (e.g., aaa, 111).")

    if patterns["sequential"]:
        suggestions.append("Avoid sequential patterns (e.g., 123, abc).")

    if found_words:
        suggestions.append("Avoid dictionary words, names, or common phrases.")

    return suggestions

# calculate final strength score WITH breakdown
def calculate_score(password, analysis, placement, patterns, entropy, found_words, rockyou_hit):
    score = 0
    breakdown = {}

    length = analysis["length"]

    if rockyou_hit:
        breakdown["RockYou Match"] = -100
        return 0, breakdown

    # length
    length_score = min(length * 4, 40)
    score += length_score
    breakdown["Length Contribution"] = length_score

    # diversity
    diversity_score = 0
    if analysis["lowercase"]:
        diversity_score += 5
    if analysis["uppercase"]:
        diversity_score += 5
    if analysis["digits"]:
        diversity_score += 5
    if analysis["special"]:
        diversity_score += 10

    score += diversity_score
    breakdown["Character Diversity"] = diversity_score

    # entropy
    entropy_score = min(int(entropy / 2), 40)
    score += entropy_score
    breakdown["Entropy Contribution"] = entropy_score

    # placement
    placement_score = 0
    if placement["middle_upper"]:
        placement_score += 5
    elif placement["upper_positions"] == [0]:
        placement_score -= 3

    if placement["middle_special"]:
        placement_score += 8
    elif placement["special_positions"] and all(pos >= length - 2 for pos in placement["special_positions"]):
        placement_score -= 5

    score += placement_score
    breakdown["Placement Adjustment"] = placement_score

    # dictionary
    dictionary_penalty = -len(found_words) * 10
    score += dictionary_penalty
    breakdown["Dictionary Penalty"] = dictionary_penalty

    # short password
    short_penalty = -10 if length < 8 else 0
    score += short_penalty
    breakdown["Short Password Penalty"] = short_penalty

    # numeric suffix
    suffix_penalty = -5 if password and password[-1].isdigit() else 0
    score += suffix_penalty
    breakdown["Numeric Suffix Penalty"] = suffix_penalty

    # patterns
    pattern_penalty = 0
    if patterns["repeated"]:
        pattern_penalty -= 10
    if patterns["sequential"]:
        pattern_penalty -= 10

    score += pattern_penalty
    breakdown["Pattern Penalty"] = pattern_penalty

    score = max(0, min(score, 100))

    return score, breakdown

def get_strength_label(score):
    if score == 0:
        return "COMPROMISED"
    elif score < 30:
        return "Very Weak"
    elif score < 50:
        return "Weak"
    elif score < 70:
        return "Moderate"
    elif score < 85:
        return "Strong"
    else:
        return "Very Strong"

# print analysis report
def print_analysis(analysis, placement, patterns, found_words, rockyou_hit, entropy, score, breakdown, crack_time, suggestions):
    print("Password Analysis:")
    print(f"- Length: {analysis['length']}")
    print(f"- Lowercase letters: {analysis['lowercase']}")
    print(f"- Uppercase letters: {analysis['uppercase']}")
    print(f"- Digits: {analysis['digits']}")
    print(f"- Special characters: {analysis['special']}")
    print(f"- Estimated entropy: {entropy:.2f} bits")
    print()

    if found_words:
        for word in found_words:
            print(f"- Contains dictionary word: \"{word}\"")
    else:
        print("- No dictionary words detected")

    if rockyou_hit:
        print("- EXACT match found in RockYou breach dataset")
    else:
        print("- Not found in RockYou dataset")

    print()
    print("Score Breakdown:")
    for key, value in breakdown.items():
        sign = "+" if value > 0 else ""
        print(f"- {key}: {sign}{value}")

    print()
    print(f"Final Score: {score} / 100")
    print(f"Strength: {get_strength_label(score)}")
    print()
    print(f"Estimated brute-force time (RTX 4070, SHA-256 @ 5000 MH/s): ~{crack_time} (average case)")

    if rockyou_hit:
        print("Real-world attack time: Instant (password exists in breach datasets)")

    print("\nSuggested Improvements:")
    if suggestions:
        for suggestion in suggestions:
            print(f"- {suggestion}")
    else:
        print("- No major weaknesses detected. This password follows strong security practices.")

# main execution
def main():
    password = get_password()
    print()

    wordlist_files = [
        "wordlists/surnames.txt",
        "wordlists/forenames.txt",
        "wordlists/10000_words_(long).txt",
        "wordlists/10000_words_(short).txt",
    ]

    combined_words = set()
    for filepath in wordlist_files:
        combined_words.update(load_wordlist(filepath))

    rockyou_files = ROCKYOU_FILES

    rockyou_hit = False

    import os

    for filepath in rockyou_files:
        if os.path.exists(filepath):
            if check_large_wordlist(password, filepath):
             rockyou_hit = True
             break


    if rockyou_hit:
        print("PASSWORD COMPROMISED")
        print("This password appears in known breach datasets.")
        print()
        input("Press Enter to view full security report or Ctrl+C to exit")

    analysis = analyze_characters(password)
    placement = analyze_placement(password)
    patterns = analyze_patterns(password)
    found_words = find_dictionary_words(password, combined_words)
    entropy = calculate_entropy(password, analysis)
    crack_time = estimate_bruteforce_time(entropy)
    score, breakdown = calculate_score(password, analysis, placement, patterns, entropy, found_words, rockyou_hit)
    suggestions = generate_suggestions(password, analysis, placement, patterns, found_words, rockyou_hit)

    print()
    print_analysis(analysis, placement, patterns, found_words, rockyou_hit, entropy, score, breakdown, crack_time, suggestions)

if __name__ == "__main__":
    main()
