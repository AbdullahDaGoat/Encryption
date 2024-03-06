####################################################################
# Updated Code + Added More Robust handelling and Scalability
# Version 5.2.3 -- Added better Regex + Error handeling

# Learn about Fernet here: https://cryptography.io/en/latest/fernet/

# General Code Overview: https://docs.google.com/document/d/1mtiNfVGaAkVxM46NkgIrwxyl2WuoGZvPRzXUYXADArc/edit

# Video of Explanation here if you somehow dont get it still: https://youtu.be/ecdjnyhnLpE

# BIG NOTE: IF YOU CHANGE THE ENCRYPTION KEY, THEN YOU MUST REUPLOAD ALL THE IMAGE DATASET BECAUSE OTHERWISE THE SYSTEM WILL BLOCK YOU FROM ACCESSING THE DATA

# inline commenting has been done so you can understand the code, please read it, and look at all the resources

# Todo: If one key is removed inform the user that (hopsital [name]) key is removed and deny access


#        /\_/\
#       ( o.o )
#        > ^ <
#       (__|__)

# Designed and Tested by Abdullah Khan in conjungation with the MIT Liscence: https://opensource.org/license/mit

############################################################

# I imported the following functions using “pip install cryptography time shutil re os”: (Just for safe practies you dont need to import os, re, and time but its better if you do anyway)


import os
# This is pythons standard function allows me to use most of python standard functions. This makes up almost 65% of the code
# Learn more of Python Os import here → https://docs.python.org/3/library/os.html

import re
# Re is short for regex which helps me look for patterns in the url identified pngs so that even if the test.png case sensitively isnt there it will use regex to find a similar test.png
# like a test.png.encrypted and run the code anyway
# You can learn more of Python Regex here → https://www.w3schools.com/python/python_regex.asp

from cryptography.fernet import Fernet
# Fernet is a high level dynamically used enterprise level cryptography library that can encode, and cryptography certain datasets.
# In this instance we used it to encrypt the images and add the .encrypt extension accordingly, aswell as to decrypt and do most of the logic and handeling in this code
# Learn more of Fernet here → https://cryptography.io/en/latest/fernet/

import time

# Time is a standard and commonly used python function to tell time, it is used to ensure that the images can only be seen for a certain allocated time period to ensure privacy and security
# Learn more of python time standard module here → https://docs.python.org/3/library/time.html

import shutil
# Shutil as it sounds is a Shuttle program library that communicates with the directory system to move files around in python, this helps us move the decrypted image
# to a temporary secure location where they can be accessed once in there they will be self destructed automatically, almost like a Shuttle system that instead of transporting passengers
# transports files
# Learn more of Shutil here → https://docs.python.org/3/library/shutil.html

# Set the path to the directory containing the MRI dataset
path = "./MRI_Parent/MRI_Dataset/"

# Set the path to the directory where the **encryption keys** will be stored
key_dir = "./MRI_Parent/MRI_Dataset/MRI_Dataset_Keys/"

# Set the file paths for the keys of hospital A and hospital B
hospital_a_key_path = os.path.join(key_dir, "hospital_a_key.key")
hospital_b_key_path = os.path.join(key_dir, "hospital_b_key.key")

# Check if the key files for hospital A and hospital B already exist
if os.path.exists(hospital_a_key_path) and os.path.exists(hospital_b_key_path):
    # If the key files exist, read the keys from the files
    with open(hospital_a_key_path, "rb") as f:
        hospital_a_key = f.read()
    with open(hospital_b_key_path, "rb") as f:
        hospital_b_key = f.read()
else:
    print("The Hospitals IT Adminsitration has not generated encryption keys yet, please contact them to resolve this")
    # If the key files don't exist, generate new keys for hospital A and hospital B
    hospital_a_key = Fernet.generate_key()
    hospital_b_key = Fernet.generate_key()
    # Write the keys to the key files
    with open(hospital_a_key_path, "wb") as f:
        f.write(hospital_a_key)
    with open(hospital_b_key_path, "wb") as f:
        f.write(hospital_b_key)
        exit()

# Create a dictionary to store the keys for each hospital
hospital_keys = {
    "A": hospital_a_key,
    "B": hospital_b_key
}

# Define a function to encrypt an image file


def encrypt_image(image_path, hospital_prefix):
    # Get the encryption key based on the hospital prefix
    key = hospital_keys.get(hospital_prefix)
    if not key:
        raise ValueError("Invalid hospital prefix")
    # Check if the image file exists
    if not os.path.exists(image_path):
        # If the image file does not exist, check for files with similar regex patterns
        image_regex = re.compile(r"^.*\.png$")
        for file in os.listdir(os.path.dirname(image_path)):
            if image_regex.match(file):
                image_path = os.path.join(os.path.dirname(image_path), file)
                break
    # Read the image file
    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
    except FileNotFoundError:
        print(f"File not found: {image_path}")
        return
    # Encrypt the image data using the key
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(image_data)
    # Set the encrypted file path
    encrypted_path = image_path + ".encrypted"
    # Write the encrypted data to the encrypted file
    try:
        with open(encrypted_path, "wb") as f:
            f.write(encrypted_data)
    except PermissionError:
        print(f"Permission denied: {encrypted_path}")
        return
    # Print the path of the encrypted file
    print(f"Encrypted: {encrypted_path}")
    # Return the path of the encrypted file
    return encrypted_path

# Define a function to decrypt an encrypted image file


def decrypt_image(encrypted_path, hospital_prefix):
    # Get the decryption key based on the hospital prefix
    key = hospital_keys.get(hospital_prefix)
    if not key:
        raise ValueError("Invalid hospital prefix")
    # Read the encrypted data
    try:
        with open(encrypted_path, "rb") as f:
            encrypted_data = f.read()
    except FileNotFoundError:
        print(f"File not found: {encrypted_path}")
        return
    # Decrypt the encrypted data using the key
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data)
    # Set the decrypted file path
    decrypted_path = encrypted_path.replace(".encrypted", "")
    # Write the decrypted data to the decrypted file
    try:
        with open(decrypted_path, "wb") as f:
            f.write(decrypted_data)
    except PermissionError:
        print(f"Permission denied: {decrypted_path}")
        return
    # Print the path of the decrypted file
    print(f"Decrypted: {decrypted_path}")
    # Return the path of the decrypted file
    return decrypted_path


# Encrypt all the image files in the MRI dataset
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".png"):
            # Get the full path of the image file
            image_path = os.path.join(root, file)
            # Get the hospital prefix from the directory name
            hospital_prefix = os.path.basename(root)
            try:
                # Encrypt the image file using the hospital prefix
                encrypted_path = encrypt_image(image_path, hospital_prefix)
            except Exception as e:
                # Print an error message if encryption fails
                print(f"Encryption failed for '{image_path}': {str(e)}")

# Decrypt all the encrypted image files in the MRI dataset
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".encrypted"):
            # Get the full path of the encrypted image file
            image_path = os.path.join(root, file)
            # Get the hospital prefix from the directory name
            hospital_prefix = os.path.basename(root)[0]
            try:
                # Decrypt the encrypted image file using the hospital prefix
                decrypted_path = decrypt_image(image_path, hospital_prefix)
            except Exception as e:
                # Print an error message if decryption fails
                print(f"Decryption failed for '{image_path}': {str(e)}")

hospital_key_input = input("Enter your hospital's encryption key: ")
hospital_key = hospital_key_input.encode()
if hospital_key not in hospital_keys.values():
    print("Invalid hospital key. Access denied.")
    exit()

# Get the path to the image file
user_defined_folder = input("Enter the folder name (CASE SENSITIVE): ")
user_defined_image = input(
    "Enter the image name without the extension (CASE SENSITIVE): ")

# Set the path to the image file
image_path = f"./MRI_Parent/MRI_Dataset/{user_defined_folder}/{user_defined_image}.png"

# Get the hospital prefix from the directory name
hospital_input_prefix = input("Enter the hospital name here (A or B): ")
hospital_prefix = hospital_input_prefix

# Get the hospital key for the encrypted image
hospital_key = hospital_keys.get(hospital_prefix)
if not hospital_key:
    raise ValueError("Invalid hospital prefix")

# Encrypt the image using the hospital key
encrypted_path = encrypt_image(image_path, hospital_prefix)

# Get the path to the encrypted image
encrypted_path = f"./MRI_Parent/MRI_Dataset/{user_defined_folder}/{user_defined_image}.png.encrypted"

# Decrypt the image using the hospital key
decrypted_path = decrypt_image(encrypted_path, hospital_prefix)


# Set the path to the decrypted image folder
decrypted_image_folder = "./Decrypted_Image_Storage/"

# Move the decrypted image to the decrypted image folder and reinitalize the decrypted path for self-destruction
decrypted_path = shutil.move(decrypted_path, decrypted_image_folder)

# Set the time limit for the decrypted image to remain accessible
time_limit = 10  # in seconds

# Start a timer
start_time = time.time()

# Continuously check if the time limit has been reached
while True:
    # Get the current time
    current_time = time.time()
    # Calculate the elapsed time
    elapsed_time = current_time - start_time
    # Check if the time limit has been reached
    if elapsed_time > time_limit:
        # If the time limit has been reached, check if the decrypted image still exists
        if os.path.exists(decrypted_path):
            # If the decrypted image still exists, delete it
            os.remove(decrypted_path)
        # Break out of the loop
        break
    # Sleep for 1 second
    time.sleep(1)

# Re-encrypt the original PNG file
new_encrypted_path = encrypt_image(image_path, hospital_prefix)

# Print the path of the newly encrypted file
print(f"Re-encrypted: {new_encrypted_path}")
