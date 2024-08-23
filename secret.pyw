byte_data = b''
import os
import sys
import base64
try:
    import easygui
except:
    os.system('pip install easygui')
    import easygui

try:
    from Crypto.Cipher import AES
except:
    os.system('pip install pycryptodome')
    from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

def derive_key(password, salt):
    return PBKDF2(password, salt, dkLen=16, count=1000000)

def encrypt(plain_text, password):
    if plain_text == "":
        return b''
    salt = get_random_bytes(16)
    key = derive_key(password, salt)
    
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(plain_text.encode(), AES.block_size))
    return salt + iv + encrypted_data

def decrypt(encrypted_data, password):
    # decode the base64 encoded bytes
    encrypted_data = base64.b64decode(encrypted_data)
    salt = encrypted_data[:16]
    iv = encrypted_data[16:32]

    key = derive_key(password, salt)
    
    # Create cipher object and decrypt the data
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data[32:]), AES.block_size)
    return decrypted_data.decode()


    
# Function to get password input
def get_password():
    return easygui.passwordbox("Enter the password to encrypt and decrypt the file:", "Password Input")

# Function to display a textbox with a default message for multi-line input
def show_message(title, message):
    return easygui.textbox("Edit the message or press OK to continue:", title, text=message)

    
def modify_self(bytes):
    # Path to the current script
    script_path = __file__
    # Read the current contents of the script
    with open(script_path, 'r') as file:
        content = file.readlines()
    content.pop(0)
    # save bytes similar to byte_data = b'\x00\x01\x02\xfa\xfb\xfc'
    content.insert(0,f"byte_data = { base64.b64encode(bytes)}\n")
    # Write the modified content back to the script
    with open(script_path, 'w') as file:
        file.writelines(content)


os.chdir(os.path.dirname(os.path.abspath(__file__)))
password = get_password()
if password == None:
    sys.exit(0)

decryption = ""
if byte_data != b'':
    try:
        decryption = decrypt(byte_data,password)
    except:
        easygui.msgbox("Decryption Failed, please try again", "Decryption Failed")
        sys.exit(0)
newtext = show_message("Decryption Successful", decryption)
if newtext == None:
    sys.exit(0)


encrypted_data = encrypt(newtext,password)
modify_self(encrypted_data)




