from PIL import Image
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
import os


ITERATIONS = 390000


# -------------------------------
# KEY GENERATION
# -------------------------------

def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS
    )

    return base64.urlsafe_b64encode(
        kdf.derive(password.encode())
    )


# -------------------------------
# ENCRYPT MESSAGE
# -------------------------------

def encrypt_message(message, password):

    salt = os.urandom(16)

    key = derive_key(password, salt)

    cipher = Fernet(key)

    encrypted = cipher.encrypt(
        message.encode("utf-8")
    )

    # Store salt + encrypted data
    payload = salt + encrypted

    return base64.b64encode(payload).decode("ascii")


# -------------------------------
# DECRYPT MESSAGE
# -------------------------------

def decrypt_message(payload, password):

    raw = base64.b64decode(payload)

    salt = raw[:16]

    encrypted = raw[16:]

    key = derive_key(password, salt)

    cipher = Fernet(key)

    decrypted = cipher.decrypt(encrypted)

    return decrypted.decode("utf-8")


# -------------------------------
# HIDE DATA USING LSB
# -------------------------------

def hide_payload(image_path, payload, output_path):

    image = Image.open(image_path).convert("RGB")

    pixels = image.load()

    data = payload.encode("utf-8")

    # Store payload length in first 32 bits
    bits = []

    length_bits = format(len(data), "032b")

    for bit in length_bits:
        bits.append(int(bit))

    # Convert payload to binary
    for byte in data:

        byte_bits = format(byte, "08b")

        for bit in byte_bits:
            bits.append(int(bit))

    # Check image capacity
    capacity = image.width * image.height * 3

    if len(bits) > capacity:

        raise ValueError(
            "Message is too large for this image."
        )

    index = 0

    # Traverse pixels
    for y in range(image.height):

        for x in range(image.width):

            channels = list(pixels[x, y])

            # R, G, B
            for c in range(3):

                if index < len(bits):

                    # Replace LSB
                    channels[c] = (
                        channels[c] & 254
                    ) | bits[index]

                    index += 1

            pixels[x, y] = tuple(channels)

            # Finished
            if index >= len(bits):

                image.save(
                    output_path,
                    "PNG"
                )

                return

    raise RuntimeError("Embedding failed.")


# -------------------------------
# EXTRACT DATA
# -------------------------------

def extract_payload(image_path):

    image = Image.open(image_path).convert("RGB")

    pixels = image.load()

    def get_bits():

        for y in range(image.height):

            for x in range(image.width):

                r, g, b = pixels[x, y]

                yield r & 1
                yield g & 1
                yield b & 1

    stream = get_bits()

    # First 32 bits = payload length
    length_bits = []

    for _ in range(32):

        length_bits.append(
            next(stream)
        )

    length = int(
        "".join(map(str, length_bits)),
        2
    )

    max_bytes = (image.width * image.height * 3 - 32) // 8
    if length > max_bytes:
        raise ValueError("Invalid payload: no hidden message found or length exceeds capacity.")

    data = bytearray()

    # Extract bytes
    for _ in range(length):

        byte_bits = []

        for _ in range(8):
            try:
                byte_bits.append(
                    next(stream)
                )
            except StopIteration:
                raise ValueError("Unexpected end of image data.")

        value = int(
            "".join(map(str, byte_bits)),
            2
        )

        data.append(value)

    return data.decode("utf-8")


# -------------------------------
# MAIN PROGRAM
# -------------------------------

def main():

    print("\n======================================")
    print(" STEGANOGRAPHY + CRYPTOGRAPHY TOOL")
    print("======================================")

    print("\n1. Hide encrypted message")
    print("2. Extract and decrypt message")

    choice = input("\nEnter choice: ")

    # -------------------------------
    # HIDE
    # -------------------------------

    if choice == "1":

        message = input(
            "\nEnter secret message: "
        )

        password = input(
            "Enter password: "
        )

        print("\nEncrypting message...")

        payload = encrypt_message(
            message,
            password
        )

        print("Encryption successful.")

        cover_image = input("Enter cover image path [original.png]: ").strip() or "original.png"
        output_image = input("Enter output image path [stego.png]: ").strip() or "stego.png"

        print("Hiding encrypted data...")

        try:
            hide_payload(
                cover_image,
                payload,
                output_image
            )
            print("Message hidden successfully.")
            print(f"\nOutput image: {output_image}")
        except FileNotFoundError:
            print(f"\nError: Could not find the cover image '{cover_image}'.")


    # -------------------------------
    # EXTRACT
    # -------------------------------

    elif choice == "2":

        password = input(
            "\nEnter password: "
        )

        stego_image = input("Enter stego image path [stego.png]: ").strip() or "stego.png"
        
        try:

            print("\nExtracting hidden data...")

            payload = extract_payload(
                stego_image
            )

            print("Encrypted data extracted.")

            message = decrypt_message(
                payload,
                password
            )

            print("\nDecryption successful.")

            print(
                "Recovered message:",
                message
            )

        except InvalidToken:

            print(
                "\nDecryption failed!"
            )

            print(
                "Incorrect password or corrupted data."
            )

        except Exception as e:

            print(
                "\nError:",
                e
            )


    else:

        print("Invalid choice.")


# -------------------------------
# START PROGRAM
# -------------------------------

if __name__ == "__main__":

    main()
