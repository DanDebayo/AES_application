import tkinter as tk
import ctypes

aes_lib = ctypes.cdll.LoadLibrary('aes.dll')


aes_lib.aes_encrypt.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
aes_lib.aes_encrypt.restype = ctypes.c_char_p
aes_lib.aes_decrypt.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
aes_lib.aes_decrypt.restype = ctypes.c_char_p


def encrypt():
    input_data = input_text.get("1.0", "end-1c").encode()
    output_data = aes_lib.aes_encrypt(input_data, b"24680")
    output_text.delete("1.0", "end")
    output_text.insert("1.0", output_data.decode())

def decrypt():
    input_data = input_text.get("1.0", "end-1c").encode()
    output_data = aes_lib.aes_decrypt(input_data, b"24680")
    output_text.delete("1.0", "end")
    output_text.insert("1.0", output_data.decode())


root = tk.Tk()
root.title("AES Encryption/Decryption")

input_label = tk.Label(root, text="Input:")
input_label.pack()

input_text = tk.Text(root, height=5)
input_text.pack()

encrypt_button = tk.Button(root, text="Encrypt", command=encrypt)
encrypt_button.pack()

decrypt_button = tk.Button(root, text="Decrypt", command=decrypt)
decrypt_button.pack()

output_label = tk.Label(root, text="Output:")
output_label.pack()

output_text = tk.Text(root, height=5)
output_text.pack()

root.mainloop()
