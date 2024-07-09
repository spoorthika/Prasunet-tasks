def caesar_encrypt(text, shift):
  cipher = ""
  for char in text:
    if char.isalpha():
      code = ord(char)
      code = (code - ord('a' if char.islower() else 'A') + shift) % 26 + ord('a' if char.islower() else 'A')
      cipher += chr(code)
    else:
      cipher += char
  return cipher

def caesar_decrypt(cipher, shift):
  text = ""
  for char in cipher:
    if char.isalpha():
      code = ord(char)
      code = (code - ord('a' if char.islower() else 'A') - shift) % 26 + ord('a' if char.islower() else 'A')
      text += chr(code)
    else:
      text += char
  return text

text = input("Enter message: ")
shift = int(input("Enter shift value (1-25): "))

encrypted = caesar_encrypt(text, shift)
decrypted = caesar_decrypt(encrypted, shift)

print("Encrypted:", encrypted)
print("Decrypted:", decrypted)
