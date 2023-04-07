import array
import os
import tkinter as tk
from tkinter import filedialog
import ctypes

aes_lib_path = os.path.abspath('libaes.so')
aes_lib = ctypes.cdll.LoadLibrary(aes_lib_path)

encrypt_func = aes_lib['_Z7EncryptRKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE']
decrypt_func = aes_lib['_Z7DecryptB5cxx11St6vectorIhSaIhEE']

encrypt_func.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_int, ctypes.POINTER(ctypes.c_uint8)]
encrypt_func.restype = None
decrypt_func.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_void_p]
decrypt_func.restype = ctypes.c_void_p

def encrypt_file():
    input_file = filedialog.askopenfilename()
    if not input_file:
        return
    with open(input_file, 'rb') as f:
        input_data = f.read()
    output_file = filedialog.asksaveasfilename()
    if not output_file:
        return
    input_len = len(input_data)
    output_len = (input_len + 15) & ~15
    input_array = (ctypes.c_uint8 * input_len).from_buffer_copy(input_data)
    output_array = (ctypes.c_uint8 * output_len)()
    encrypt_func(input_array, input_len, output_array)
    output_data = bytes(output_array[:input_len])
    with open(output_file, 'wb') as f:
        f.write(output_data)

def decrypt_file():
    input_file = filedialog.askopenfilename()
    if not input_file:
        return
    with open(input_file, 'rb') as f:
        input_data = f.read()
    output_file = filedialog.asksaveasfilename()
    if not output_file:
        return
    output_data = ctypes.create_string_buffer(len(input_data))
    decrypt_func(input_data, b"24680", ctypes.byref(output_data))
    with open(output_file, 'wb') as f:
        f.write(output_data)

root = tk.Tk()
root.title("AES Encryption/Decryption")

input_label = tk.Label(root, text="Choose an option:")
input_label.pack()

encrypt_button = tk.Button(root, text="Encrypt file", command=encrypt_file)
encrypt_button.pack()

decrypt_button = tk.Button(root, text="Decrypt file", command=decrypt_file)
decrypt_button.pack()

root.mainloop()
