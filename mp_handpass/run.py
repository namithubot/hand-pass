window = tk.Tk()
button = tk.Button(window, text='Record', width=25, command=lambda: start())
button.pack()
window.mainloop()