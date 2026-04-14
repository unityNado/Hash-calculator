import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib
import os


def calculate_hash():
    algo = algo_var.get()
    mode = mode_var.get()
    data = b''

    try:
        if mode == 1:  # Текст
            text = text_input.get("1.0", tk.END).strip()
            if not text:
                messagebox.showwarning("Ошибка", "Введите текст!")
                return
            data = text.encode('utf-8')

        elif mode == 2:  # Файл
            path = file_path.get()
            if not path or not os.path.exists(path):
                messagebox.showwarning("Ошибка", "Файл не выбран или не найден!")
                return
            with open(path, 'rb') as f:
                data = f.read()

        if algo == "MD5":
            result = hashlib.md5(data).hexdigest()
        elif algo == "SHA-1":
            result = hashlib.sha1(data).hexdigest()
        elif algo == "SHA-256":
            result = hashlib.sha256(data).hexdigest()

        result_entry.config(state='normal')
        result_entry.delete(0, tk.END)
        result_entry.insert(0, result)
        result_entry.config(state='readonly')

    except Exception as e:
        messagebox.showerror("Ошибка", f"Что-то пошло не так:\n{e}")


def select_file():
    path = filedialog.askopenfilename()
    if path:
        file_path.set(path)
        lbl_filename.config(text=os.path.basename(path))


def copy_to_clipboard():
    # Получаем текст из поля результата
    result_text = result_entry.get()

    if result_text:
        # Очищаем буфер обмена и кладем туда текст
        root.clipboard_clear()
        root.clipboard_append(result_text)

        # Меняем текст кнопки на время
        original_text = copy_btn.cget("text")
        copy_btn.config(text="Скопировано!", bg="#666666")
        # Вернем текст кнопки обратно через 1.5 секунды
        root.after(1500, lambda: copy_btn.config(text=original_text, bg="#333333"))


# --- Создание окна ---
root = tk.Tk()
root.title("Хэш-Калькулятор")
root.geometry("500x650")
root.configure(bg="#000000")

# Переменные
mode_var = tk.IntVar(value=1)
algo_var = tk.StringVar(value="MD5")
file_path = tk.StringVar()

# Заголовок
header = tk.Label(root, text="КАЛЬКУЛЯТОР ХЭШ-СУММ", font=("Arial", 16, "bold"), bg="#000000", fg="#FFFFFF")
header.pack(pady=20)

# --- Выбор режима ---
mode_frame = tk.Frame(root, bg="#000000")
mode_frame.pack(pady=5)

tk.Label(mode_frame, text="Что хэшируем?", bg="#000000", fg="#FFFFFF", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
rb_style = {"bg": "#000000", "fg": "#FFFFFF", "selectcolor": "#333333", "activebackground": "#000000",
            "font": ("Arial", 10)}
tk.Radiobutton(mode_frame, text="Текст", variable=mode_var, value=1, **rb_style).pack(side=tk.LEFT, padx=5)
tk.Radiobutton(mode_frame, text="Файл", variable=mode_var, value=2, **rb_style).pack(side=tk.LEFT, padx=5)

# --- Поле для ввода текста ---
tk.Label(root, text="Введите текст:", bg="#000000", fg="#FFFFFF", font=("Arial", 10)).pack(pady=(10, 0))
text_input = tk.Text(root, height=5, width=45, bg="#202020", fg="#FFFFFF", insertbackground="#FFFFFF",
                     font=("Arial", 10), relief=tk.FLAT)
text_input.pack(pady=5, padx=10)

# --- выбор файла ---
tk.Label(root, text="Или выберите файл:", bg="#000000", fg="#FFFFFF", font=("Arial", 10)).pack(pady=(10, 0))

file_frame = tk.Frame(root, bg="#000000")
file_frame.pack(pady=5)

btn_select = tk.Button(file_frame, text="Обзор...", command=select_file, bg="#333333", fg="#FFFFFF", font=("Arial", 10))
btn_select.pack(side=tk.LEFT, padx=5)

lbl_filename = tk.Label(file_frame, text="Файл не выбран", bg="#202020", fg="#888888", font=("Arial", 10), padx=10)
lbl_filename.pack(side=tk.LEFT, fill=tk.X)

# --- Выбор алгоритма ---
tk.Label(root, text="Выберите алгоритм:", bg="#000000", fg="#FFFFFF", font=("Arial", 10)).pack(pady=(15, 5))

algo_frame = tk.Frame(root, bg="#000000")
algo_frame.pack(pady=5)

tk.Radiobutton(algo_frame, text="MD5", variable=algo_var, value="MD5", **rb_style).pack(side=tk.LEFT, padx=10)
tk.Radiobutton(algo_frame, text="SHA-1", variable=algo_var, value="SHA-1", **rb_style).pack(side=tk.LEFT, padx=10)
tk.Radiobutton(algo_frame, text="SHA-256", variable=algo_var, value="SHA-256", **rb_style).pack(side=tk.LEFT, padx=10)

# --- Кнопка расчета ---
calc_btn = tk.Button(root, text="РАССЧИТАТЬ", command=calculate_hash,
                     bg="#FFFFFF", fg="#000000", font=("Arial", 12, "bold"), bd=0, padx=20, pady=10)
calc_btn.pack(pady=20)

# --- Поле результата ---
tk.Label(root, text="Результат:", bg="#000000", fg="#FFFFFF", font=("Arial", 10)).pack()

result_entry = tk.Entry(root, width=50, font=("Courier New", 12), justify='center',
                        bg="#202020", fg="#FFFFFF", readonlybackground="#202020",
                        relief=tk.FLAT, state="readonly")
result_entry.pack(pady=5, ipady=5)

# --- Кнопка копирования ---
copy_btn = tk.Button(root, text="КОПИРОВАТЬ", command=copy_to_clipboard,
                     bg="#333333", fg="#FFFFFF", font=("Arial", 10), bd=0, padx=15, pady=5)
copy_btn.pack(pady=5)

# --- Запуск главного цикла ---
root.mainloop()