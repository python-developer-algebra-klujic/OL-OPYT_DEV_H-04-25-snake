import tkinter as tk

STEP = 150

root = tk.Tk()
root.title('Tkinter canvas demo')

lbl_title = tk.Label(root, text='Canvas demo', font=('Verdana', 18))
lbl_title.pack(pady=25)

canvas = tk.Canvas(root, width=800, height=600, bg='black')
canvas.pack()

canvas.create_text(10, 10, anchor='nw', fill='white', text='Tekst unutar Canvas widget-a')
canvas.create_oval(25, 25, 75, 75, fill='red', outline='')
canvas.create_rectangle(25 + STEP, 25 + STEP, 75 + STEP, 75 + STEP, fill='red', outline='')


root.mainloop()
