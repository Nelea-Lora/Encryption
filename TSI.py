import tkinter as tk
from tkinter import ttk

def button1_clicked():
    # ��������� �� ������ �������
    notebook.select(tab2)

def button2_clicked():
    # ��������� �� ������ �������
    notebook.select(tab3)

def button3_clicked():
    # ��������� �� ������ �������
    notebook.select(tab1)

# ������� ��������� �������� ����
root = tk.Tk()

root.configure(bg='#F0C4DD')

# ������� �������
notebook = ttk.Notebook(root)
tab1 = tk.Frame(notebook)
tab2 = tk.Frame(notebook)
tab3 = tk.Frame(notebook)
notebook.add(tab1, text='Page 1')
notebook.add(tab2, text='Page 2')
notebook.add(tab3, text='Page 3')

# ���� ������ �� ������ �������
output_label = tk.Label(tab1, text="Output will be displayed here", bg='#C57466', fg='#260D52')
output_label.pack()

# ������� ������
button1 = tk.Button(tab1, text="Go to Page 2", command=button1_clicked, bg='#F06A53', fg='#33221F')
button1.pack()
button2 = tk.Button(tab2, text="Go to Page 3", command=button2_clicked, bg='#F06A53', fg='#33221F')
button2.pack()
button3 = tk.Button(tab3, text="Go to Page 1", command=button3_clicked, bg='#F06A53', fg='#33221F')
button3.pack()

notebook.pack()

# ��������� ������� ���� ��������� �������
root.mainloop()