import re

def check_password_complexity(password):
    # Criteria definitions
    length_criteria = len(password) >= 8
    uppercase_criteria = re.search(r'[A-Z]', password) is not None
    lowercase_criteria = re.search(r'[a-z]', password) is not None
    digit_criteria = re.search(r'\d', password) is not None
    special_criteria = re.search(r'[^A-Za-z0-9]', password) is not None

    # Calculate strength score
    criteria_met = {
        "Length (8+ characters)": length_criteria,
        "Uppercase letter": uppercase_criteria,
        "Lowercase letter": lowercase_criteria,
        "Digit": digit_criteria,
        "Special character": special_criteria
    }
    
    # Determine strength level
    complexity_score = sum(criteria_met.values())

    if complexity_score == 5:
        strength = "Very Strong"
    elif complexity_score == 4:
        strength = "Strong"
    elif complexity_score == 3:
        strength = "Moderate"
    else:
        strength = "Weak"

    return strength, criteria_met

# Example usage
if __name__ == "__main__":
    password = input("Enter your password: ")
    strength, criteria_met = check_password_complexity(password)
    
    print(f"Password complexity: {strength}")
    print("Criteria met:")
    for criteria, met in criteria_met.items():
        print(f" - {criteria}: {'Yes' if met else 'No'}")
