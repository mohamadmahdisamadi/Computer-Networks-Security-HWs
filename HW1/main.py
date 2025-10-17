from BitVector import *
from DES import DES
import os
import re

def receive_encryption_key():
    ENCRYPTION_KEY_EXPECTED_SIZE = 8
    print(f"Please enter an encryption key consisting of {ENCRYPTION_KEY_EXPECTED_SIZE} printable characters: ", end="")
    encryption_key: str = input()
    if len(encryption_key) != ENCRYPTION_KEY_EXPECTED_SIZE:
        raise Exception("Key must contain exactly 8 characters!")
    return BitVector(textstring = encryption_key)



def clear_files():
    directory = '.'
    keep_pattern = re.compile(r'^plain\d+\.txt$')
    for filename in os.listdir(directory):
        if filename.endswith('.txt') and not keep_pattern.match(filename):
            file_path = os.path.join(directory, filename)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error removing {filename}: {e}")

def avalanche_effect(bv1: BitVector, bv2: BitVector, print_result=False):
    if bv1.length() != bv2.length():
        raise ValueError("BitVectors must have the same length")

    diff = bv1 ^ bv2
    changed_bits = diff.count_bits()
    total_bits = bv1.length()
    percentage = (changed_bits / total_bits) * 100

    if print_result:
        print(f"Avalanche Effect: {changed_bits}/{total_bits} bits changed ({percentage:.2f}%)")
    else:
        return percentage

def run_encryption_decryption():
    PLAIN_TEXT_FILE = "plain.txt"
    CIPHER_TEXT_FILE = "cipher.txt"
    ED_TEXT_FILE = "encrypted_decrypted.txt"

    key = receive_encryption_key()
    DES_algorithm = DES(key=key, use_standard_sboxes=False)

    plain_text_file = BitVector(filename=PLAIN_TEXT_FILE)
    encrypted_bv = DES_algorithm.encrypt(file=plain_text_file)
    with open(CIPHER_TEXT_FILE, 'wb') as f:
        encrypted_bv.write_to_file(f)

    cipher_text_file = BitVector(filename=CIPHER_TEXT_FILE)
    DES_algorithm.switch_mode()
    decrypted_bv = DES_algorithm.encrypt(file=cipher_text_file)
    with open(ED_TEXT_FILE, 'wb') as f:
        decrypted_bv.write_to_file(f)


def run_with_different_sboxes(numof_tests: int = 30):
    print(f"Running {numof_tests} tests with different s-boxes...")
    PLAIN_TEXT_FILE = "plain1.txt"
    key = receive_encryption_key()
    avalanche_percentages = []

    plain_text_file_1 = BitVector(filename=PLAIN_TEXT_FILE)
    DES_algorithm_1 = DES(key=key, use_standard_sboxes=True)
    encrypted_bv_1 = DES_algorithm_1.encrypt(file=plain_text_file_1)
    
    for _ in range(numof_tests):
        plain_text_file_2 = BitVector(filename=PLAIN_TEXT_FILE)
        DES_algorithm_2 = DES(key=key, use_standard_sboxes=False)
        encrypted_bv_2 = DES_algorithm_2.encrypt(file=plain_text_file_2)

        avalanche_percentage = avalanche_effect(bv1=encrypted_bv_1, bv2=encrypted_bv_2)
        avalanche_percentages.append(avalanche_percentage)

    print(f"Average Avalanche effect: {(sum(avalanche_percentages)/len(avalanche_percentages)):.2f}")

def run_with_different_inputs(numof_tests: int = 30):
    print(f"Running {numof_tests} tests with different inputs...")
    PLAIN_TEXT_FILE_1 = "plain1.txt"
    PLAIN_TEXT_FILE_2 = "plain2.txt"

    key = receive_encryption_key()
    avalanche_percentages = []

    for _ in range(numof_tests):
        DES_algorithm_1 = DES(key=key, use_standard_sboxes=False)

        plain_text_file_1 = BitVector(filename=PLAIN_TEXT_FILE_1)
        encrypted_bv_1 = DES_algorithm_1.encrypt(file=plain_text_file_1)

        plain_text_file_2 = BitVector(filename=PLAIN_TEXT_FILE_2)
        encrypted_bv_2 = DES_algorithm_1.encrypt(file=plain_text_file_2)

        avalanche_percentage = avalanche_effect(bv1=encrypted_bv_1, bv2=encrypted_bv_2)
        avalanche_percentages.append(avalanche_percentage)

    print(f"Average Avalanche effect: {(sum(avalanche_percentages)/len(avalanche_percentages)):.2f}")

def main():
    run_with_different_sboxes()
    print()
    run_with_different_inputs()

if __name__ == "__main__":
    clear_files() 
    main()
