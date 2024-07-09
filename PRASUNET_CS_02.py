from PIL import Image
import numpy as np
import os

def encrypt_image(image_path, key):
    try:
        img = Image.open(image_path)
    except IOError:
        print(f"Error: Cannot open image file {image_path}")
        return None

    pixels = np.array(img)
    np.random.seed(key)
    random_indices = np.random.permutation(pixels.size // 3)
    
    encrypted_pixels = pixels.reshape(-1, 3).copy()
    for i in range(len(random_indices)):
        j = random_indices[i]
        encrypted_pixels[i], encrypted_pixels[j] = encrypted_pixels[j], (encrypted_pixels[i] + key) % 256

    encrypted_pixels = encrypted_pixels.reshape(pixels.shape)
    encrypted_img = Image.fromarray(encrypted_pixels.astype(np.uint8))

    encrypted_path = image_path.rsplit('.', 1)[0] + '_encrypted.jpeg'
    encrypted_img.save(encrypted_path)
    return encrypted_path

def decrypt_image(image_path, key):
    try:
        img = Image.open(image_path)
    except IOError:
        print(f"Error: Cannot open image file {image_path}")
        return None

    pixels = np.array(img)
    np.random.seed(key)
    random_indices = np.random.permutation(pixels.size // 3)
    
    decrypted_pixels = pixels.reshape(-1, 3).copy()
    for i in range(len(random_indices) - 1, -1, -1):
        j = random_indices[i]
        decrypted_pixels[i], decrypted_pixels[j] = (decrypted_pixels[i] - key) % 256, decrypted_pixels[j]

    decrypted_pixels = decrypted_pixels.reshape(pixels.shape)
    decrypted_img = Image.fromarray(decrypted_pixels.astype(np.uint8))

    decrypted_path = image_path.rsplit('_encrypted', 1)[0] + '_decrypted.jpeg'
    decrypted_img.save(decrypted_path)
    return decrypted_path

if __name__ == "__main__":
    image_path = input("Enter the path to the image file (JPEG format): ").strip()
    if not os.path.isfile(image_path):
        print(f"Error: The file {image_path} does not exist.")
    else:
        key = int(input("Enter the encryption key (an integer value): "))
        
        encrypted_path = encrypt_image(image_path, key)
        if encrypted_path:
            print(f"Encrypted image saved as: {encrypted_path}")
            
            decrypted_path = decrypt_image(encrypted_path, key)
            if decrypted_path:
                print(f"Decrypted image saved as: {decrypted_path}")
