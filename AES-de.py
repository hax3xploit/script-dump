import binascii
import base64
from Crypto.Cipher import AES
from colorama import init, Fore, Style

init(autoreset=True)

def hex_to_bytes(hex_string):
    try:
        byte_data = binascii.unhexlify(hex_string)
        return byte_data
    except binascii.Error as e:
        print(f"{Fore.RED}Error converting hex to bytes: {e}")
        return None

def decrypt_data(encrypted_base64_data, key, iv):
    try:
        encrypted_data = base64.b64decode(encrypted_base64_data)
        key_bytes = hex_to_bytes(key)
        iv_bytes = hex_to_bytes(iv)

        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)

        decrypted_data = cipher.decrypt(encrypted_data)

        return decrypted_data
    except Exception as e:
        print(f"{Fore.RED}Error during decryption: {e}")
        return None

banner = f"""
{Fore.CYAN}
          ___    .                         +
*  .      \  \     _ _       *        ,---------------------------,
           \**\ ___\/ \...............|        Abdullah K         | .
   .     X*######*+~\__\              `---------------------------'
      +    o/\  \           .           *      .
              \__\                     .                  .
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ______ _______                         ________        
                ___  //_/__  /_______ ___      _______ ______(_)_____ _
                __  ,<  __  __ \  __ `/_ | /| / /  __ `/____  /_  __ `/
                _  /| | _  / / / /_/ /__ |/ |/ // /_/ /____  / / /_/ / 
                /_/ |_| /_/ /_/\__,_/ ____/|__/ \__,_/ ___  /  \__,_/  
                                                       /___/           
                                                               
                        [*] AES Decryption on FLY!✈️
{Style.RESET_ALL}
"""

print(banner)

# ADD KEYS HERE
iv = "---ADD-YOUR--IV--"
key = '---ADD-YOUR--KEY--'

enc_data = input(f"{Fore.YELLOW}Enter Encrypted Data: {Style.RESET_ALL}")
encrypted_data_base64 = str(enc_data)

decrypted_data = decrypt_data(encrypted_data_base64, key, iv)

print(f"\n{Fore.GREEN}Key in hex:{Style.RESET_ALL} {iv}")
print(f"\n{Fore.GREEN}IV in hex:{Style.RESET_ALL} {key}")

print('\n-------------------')
print(f"\n{Fore.GREEN}Decrypted Data:{Style.RESET_ALL} {decrypted_data.decode('utf-8')}")
