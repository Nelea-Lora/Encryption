import tkinter as tk
import random
from tkinter import ttk
from tkinter import simpledialog
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def center_window(window):
    # Определяем размеры окна
    window_width = window.winfo_reqwidth()
    window_height = window.winfo_reqheight()

    # Определяем размеры экрана
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Вычисляем координаты для центрирования окна
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Устанавливаем положение окна
    window.geometry('+{}+{}'.format(x, y))
 
def generate_key():
    return get_random_bytes(24)


def encrypt_text(key, plaintext):
    cipher = DES3.new(key, DES3.MODE_CBC)
    padded_plaintext = pad(plaintext.encode(), DES3.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    return ciphertext, cipher.iv

# Дешифрование текста с использованием 3DES
def decrypt_text(key, iv, ciphertext):
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(ciphertext)
    plaintext = unpad(decrypted_data, DES3.block_size)
    return plaintext.decode()

# Функция для проверки простоты числа - Асимметричный алгоритм
def is_prime(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    for _ in range(k):
        a = random.randint(2, n - 1)
        if pow(a, n - 1, n) != 1:
            return False
    return True

# Функция для генерации простого числа длины bit_length бит
def generate_prime(bit_length):
    while True:
        p = random.getrandbits(bit_length)
        if is_prime(p):
            return p

# Функция для нахождения примитивного элемента по модулю p
def find_primitive_root(p):
    for g in range(2, p):
        if pow(g, (p - 1) // 2, p) != 1 and pow(g, p - 1, p) == 1:
            return g
    return None

# Функция для генерации ключей
def generate_keys(bit_length):
    p = generate_prime(bit_length)
    g = find_primitive_root(p)
    x = random.randint(2, p - 1)
    h = pow(g, x, p)
    public_key = (p, g, h)
    private_key = x
    return public_key, private_key

# Функция для шифрования
def encrypt(public_key, plaintext):
    p, g, h = public_key
    y = random.randint(2, p - 1)
    c1 = pow(g, y, p)
    s = pow(h, y, p)
    c2 = plaintext * s % p
    return c1, c2

# Функция для расшифрования
def decrypt(public_key, private_key, ciphertext):
    p, _, _ = public_key
    c1, c2 = ciphertext
    s = pow(c1, private_key, p)
    plaintext = c2 * pow(s, -1, p) % p
    return plaintext

def button1_clicked():
    # Симметричный алгоритм
    input_window = tk.Toplevel(root)
    input_window.title("Enter Text")
    entry_label = tk.Label(input_window, text="Enter text:")
    entry_label.pack()
    text_entry = tk.Entry(input_window)
    text_entry.pack()

    # Функция, вызываемая при нажатии кнопки "Зашифровать"
    def encrypt_button_clicked():
        plaintext = text_entry.get()  # Получаем текст из поля ввода
        key = generate_key()
        ciphertext, iv = encrypt_text(key, plaintext)

        # Отображаем результаты шифрования в новом окне
        result_window = tk.Toplevel(root)
        result_window.title("Encrypted Text")

        encrypted_label = tk.Label(result_window, text="Encrypted text: " + ciphertext.hex())
        encrypted_label.pack()

        iv_label = tk.Label(result_window, text="Initialization vector: " + iv.hex())
        iv_label.pack()

        # Функция, вызываемая при нажатии кнопки "Расшифровать"
        def decrypt_button_clicked():
            decrypted_text = decrypt(key, iv, ciphertext)
            decrypted_label = tk.Label(result_window, text="Decrypted text: " + decrypted_text)
            decrypted_label.pack()

            print("Decrypted text:", decrypted_text)

        # Создаем кнопку "Расшифровать" и связываем с ней функцию decrypt_button_clicked
        decrypt_button = tk.Button(result_window, text="Decrypt", command=decrypt_button_clicked)
        decrypt_button.pack()

        print("Encrypted text:", ciphertext.hex())
        print("Initialization vector:", iv.hex())

    # Создаем кнопку "Зашифровать" и связываем с ней функцию encrypt_button_clicked
    encrypt_button = tk.Button(input_window, text="Encrypt", command=encrypt_button_clicked)
    encrypt_button.pack()

def button2_clicked():
    # Асимметричный алгоритм
    def encrypt_button_clicked():
        plaintext_str = text_entry.get()  # Получаем текст из поля ввода
        plaintext_bytes = plaintext_str.encode()
        plaintext_int = int.from_bytes(plaintext_bytes, byteorder='big')
        ciphertext = encrypt(public_key, plaintext_int)

        # Функция для обработки нажатия кнопки "Decrypt"
        def decrypt_button_clicked():
            decrypted_text = decrypt(public_key, private_key, ciphertext)
            print("Decrypted text:", decrypted_text)

        # Создаем новое окно для отображения зашифрованного текста
        result_window = tk.Toplevel(root)
        result_window.title("Encrypted Text")

        # Выводим зашифрованный текст на новом окне
        encrypted_label = tk.Label(result_window, text="Encrypted text: " + str(ciphertext))
        encrypted_label.pack()

        # Создаем кнопку "Decrypt" и связываем с ней функцию decrypt_button_clicked
        decrypt_button = tk.Button(result_window, text="Decrypt", command=decrypt_button_clicked)
        decrypt_button.pack()

        # Выводим информацию о ключах и зашифрованном тексте в консоль
        print("Public key:", public_key)
        print("Private key:", private_key)
        print("Encrypted Text:", ciphertext)

    # Генерируем ключи
    public_key, private_key = generate_keys(128)

    # Создаем окно для ввода текста
    input_window = tk.Toplevel(root)
    input_window.title("Enter Text")
    entry_label = tk.Label(input_window, text="Enter text:")
    entry_label.pack()
    text_entry = tk.Entry(input_window)
    text_entry.pack()

    # Создаем кнопку "Encrypt" и связываем с ней функцию encrypt_button_clicked
    encrypt_button = tk.Button(input_window, text="Encrypt", command=encrypt_button_clicked)
    encrypt_button.pack()

def button3_clicked():
    # Открываем окно ввода текста
    result = simpledialog.askstring("Input", "Please enter text:")
    

def button4_clicked():
    # Открываем окно ввода текста
    result = simpledialog.askstring("Input", "Please enter text:")
    
       
root = tk.Tk()

root.configure(bg='#F0C4DD')

# Поле вывода
output_label = tk.Label(root, text="What would you like to do?", bg='#F0C4DD', fg='#260D52', font=('Arial',40))

# Создаем кнопки
button1 = tk.Button(root, text="Symmetric encryption algorithm", command=button1_clicked, bg='#F06A53', fg='#33221F', font=('Arial', 25))
button2 = tk.Button(root, text="Asymmetric encryption algorithm", command=button2_clicked, bg='#F06A53', fg='#33221F', font=('Arial', 25))
button3 = tk.Button(root, text="Digital signature", command=button3_clicked, bg='#F06A53', fg='#33221F', font=('Arial', 26))
button4 = tk.Button(root, text="Decrypter", command=button4_clicked, bg='#F06A53', fg='#33221F', font=('Arial', 26))

# Размещаем кнопки и поле вывода на главном окне
output_label.pack()
button1.pack()
button2.pack()
button3.pack()
button4.pack()

# Запускаем главный цикл обработки событий
root.mainloop()