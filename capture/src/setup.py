import tkinter as tk


def only_int(input: str):
    return input.isdigit()

def only_filename(input: str):
    return input.isalpha() or input.isnumeric() or input in ["-", "_"]

def only_float(input: str):
    return input.isdigit() or input == "."

def main():
    root = tk.Tk()
    root.title("Monochorder Capture Setup")
    root.geometry("400x300")

    vcmd_int = (root.register(only_int), '%S')
    vcmd_float = (root.register(only_float), '%S')
    vcmd_filename = (root.register(only_filename), '%S')

    def clear():
        for widget in root.winfo_children():
            widget.destroy()

    def render_calibration():
        clear()

        rows_var = tk.StringVar()
        tk.Label(root, text="Rows").grid(row=0, column=0)
        tk.Entry(root, validate="key", validatecommand=vcmd_int, textvariable=rows_var).grid(row=0, column=1, pady=5)

        columns_var = tk.StringVar()
        tk.Label(root, text="Columns").grid(row=1, column=0)
        tk.Entry(root, validate="key", validatecommand=vcmd_int, textvariable=columns_var).grid(row=1, column=1, pady=5)

        square_width_var = tk.StringVar()
        tk.Label(root, text="Square Width").grid(row=2, column=0)
        tk.Entry(root, validate="key", validatecommand=vcmd_float, textvariable=square_width_var).grid(row=2, column=1, pady=5)

        def submit():
            print(int(rows_var.get()))
            print(int(columns_var.get()))
            print(float(square_width_var.get()))
            render_image_creation()

        tk.Button(root, text="Calibrate [C]", command=submit).grid(row=3, column=0, columnspan=2, pady=20)

    def render_image_creation():
        clear()

        name_var = tk.StringVar()
        tk.Label(root, text="Rows").grid(row=0, column=0)
        tk.Entry(root, validate="key", validatecommand=vcmd_filename, textvariable=name_var).grid(row=0, column=1, pady=5)

        def submit():
            print(name_var.get())
            root.quit()

        tk.Button(root, text="Save and Quit [C]", command=submit).grid(row=1, column=0, columnspan=2, pady=20)

    render_calibration()
    root.mainloop()

if __name__ == "__main__":
    main()