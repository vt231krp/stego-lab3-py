import os
import re


# --- Utility Functions ---


def text_to_bits(text):
    return "".join(format(ord(c), "08b") for c in text)


def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i : i + 8]
        if len(byte) < 8:
            break
        chars.append(chr(int(byte, 2)))
    return "".join(chars)


# --- Steganography Methods ---


# 1. Zero-Width Characters (ZWC)
def encode_zwc(carrier, secret):
    bits = text_to_bits(secret)
    encoded_bits = "".join(["\u200b" if b == "1" else "\u200c" for b in bits])
    return encoded_bits + carrier


def decode_zwc(stego):
    bits = []
    for char in stego:
        if char == "\u200b":
            bits.append("1")
        elif char == "\u200c":
            bits.append("0")
    return bits_to_text("".join(bits))


# 2. Case Modification
def encode_case(carrier, secret):
    bits = text_to_bits(secret)
    result = []
    bit_idx = 0
    for char in carrier:
        if char.isalpha() and bit_idx < len(bits):
            result.append(char.upper() if bits[bit_idx] == "1" else char.lower())
            bit_idx += 1
        else:
            result.append(char)
    if bit_idx < len(bits):
        print("Warning: Carrier text too short for this secret!")
    return "".join(result)


def decode_case(stego):
    bits = []
    for char in stego:
        if char.isalpha():
            bits.append("1" if char.isupper() else "0")
    return bits_to_text("".join(bits))


# 3. Whitespace Manipulation
def encode_whitespace(carrier, secret):
    bits = text_to_bits(secret)
    words = carrier.split(" ")
    result = []
    for i, word in enumerate(words):
        result.append(word)
        if i < len(bits):
            result.append("  " if bits[i] == "1" else " ")
        elif i < len(words) - 1:
            result.append(" ")
    return "".join(result)


def decode_whitespace(stego):
    bits = []
    spaces = re.findall(r"(\s+)", stego)
    for s in spaces:
        bits.append("1" if len(s) > 1 else "0")
    return bits_to_text("".join(bits))


# 4. Font Color Modification
def encode_color_html(carrier, secret):
    bits = text_to_bits(secret)
    html = "<html><body>"
    bit_idx = 0
    for char in carrier:
        if char != " " and bit_idx < len(bits):
            color = "#0A0A0A" if bits[bit_idx] == "1" else "#000000"
            html += f'<span style="color:{color}">{char}</span>'
            bit_idx += 1
        else:
            html += char
    html += "</body></html>"
    return html


def decode_color_html(stego):
    colors = re.findall(r"color:(#\w+)", stego)
    bits = "".join(["1" if c == "#0A0A0A" else "0" for c in colors])
    return bits_to_text(bits)


# --- Main Application Logic ---


def save_to_file(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved to {filename}")


def read_from_file(filename):
    if not os.path.exists(filename):
        return None
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def main_menu():
    while True:
        print("\n--- TEXT STEGANOGRAPHY TOOL ---")
        print("1. Hide Message (Encode)")
        print("2. Extract Message (Decode)")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == "3":
            break

        print("\nMethods: 1. ZWC | 2. Case | 3. Whitespace | 4. Color (HTML)")
        method = input("Select method: ")

        if choice == "1":  # ENCODE
            carrier = input("Enter carrier text: ")
            secret = input("Enter secret message: ")

            binary = text_to_bits(secret)
            print(f"Secret in Binary: {binary}")

            stego = ""
            ext = ".txt"
            if method == "1":
                stego = encode_zwc(carrier, secret)
            elif method == "2":
                stego = encode_case(carrier, secret)
            elif method == "3":
                stego = encode_whitespace(carrier, secret)
            elif method == "4":
                stego = encode_color_html(carrier, secret)
                ext = ".html"

            print(f"Stego-text generated.")
            save_to_file("stego_output" + ext, stego)

        elif choice == "2":  # DECODE
            filename = input("Enter filename to decode from: ")
            stego_data = read_from_file(filename)

            if stego_data:
                extracted = ""
                if method == "1":
                    extracted = decode_zwc(stego_data)
                elif method == "2":
                    extracted = decode_case(stego_data)
                elif method == "3":
                    extracted = decode_whitespace(stego_data)
                elif method == "4":
                    extracted = decode_color_html(stego_data)

                print(f"Extracted Message: {extracted}")
            else:
                print("File not found.")


if __name__ == "__main__":
    main_menu()
