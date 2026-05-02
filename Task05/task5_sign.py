import os
import argparse
import hashlib
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m", "--message", type=str, default="give my friend 2 bitcoins for a pizza"
    )
    args = parser.parse_args()

    message_str = args.message
    message = message_str.encode("utf-8")

    key_path = "../keys_and_certs/server.key"
    output_dir = "output"

    print(f"Message: '{message.decode()}'")

    try:
        with open(key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(), password=None, backend=default_backend()
            )
    except FileNotFoundError:
        print(f"Error no file {key_path}")
        return

    # extract param for RSA
    private_numbers = private_key.private_numbers()
    d = private_numbers.d
    n = private_numbers.public_numbers.n
    key_size_bytes = (n.bit_length() + 7) // 8

    # hash message
    digest = hashlib.sha256(message).digest()
    hash_int = int.from_bytes(digest, byteorder="big")

    print("Demo of 5 itereations to see the difference of Textbook RSA vs RSA-PSS\n")

    for i in range(1, 6):
        print(f"--- Iteration {i} ---")

        textbook_sig_int = pow(hash_int, d, n)
        textbook_sig_bytes = textbook_sig_int.to_bytes(key_size_bytes, byteorder="big")

        pss_sig_bytes = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )

        print(f"Textbook RSA : {textbook_sig_bytes[:16].hex()}...")
        print(f"RSA-PSS      : {pss_sig_bytes[:16].hex()}...")
        print()

        if i == 5:
            print(f"{'='*40}")
            print("Saving 5th iteration results")

            textbook_path = os.path.join(output_dir, "signature_textbook.bin")
            pss_path = os.path.join(output_dir, "signature_pss.bin")

            with open(textbook_path, "wb") as f:
                f.write(textbook_sig_bytes)

            with open(pss_path, "wb") as f:
                f.write(pss_sig_bytes)

            print(f"Signature downloaded into '{output_dir}':")
            print(f"1. {textbook_path}")
            print(f"2. {pss_path}")
            print(f"{'='*40}")


if __name__ == "__main__":
    main()
