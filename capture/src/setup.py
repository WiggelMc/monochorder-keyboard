import tkinter as tk


def only_int(input: str):
    return input.isdigit()

def only_float(input: str):
    return input.isdigit() or input == "."

def main():
    root = tk.Tk()
    root.title("Monochorder Capture Setup")

    vcmd_int = (root.register(only_int), '%S')
    vcmd_float = (root.register(only_float), '%S')

    rows_var = tk.StringVar()
    columns_var = tk.StringVar()
    square_width_var = tk.StringVar()

    tk.Label(root, text="Rows").grid(row=0, column=0)
    rows_input = tk.Entry(root, validate="key", validatecommand=vcmd_int, textvariable=rows_var)
    rows_input.grid(row=0, column=1)

    tk.Label(root, text="Columns").grid(row=1, column=0)
    columns_input = tk.Entry(root, validate="key", validatecommand=vcmd_int, textvariable=columns_var)
    columns_input.grid(row=1, column=1)

    tk.Label(root, text="Square Width").grid(row=2, column=0)
    square_width_input = tk.Entry(root, validate="key", validatecommand=vcmd_float, textvariable=square_width_var)
    square_width_input.grid(row=2, column=1)

    def submit():
        print(int(rows_var.get()))
        print(int(columns_var.get()))
        print(float(square_width_var.get()))

    calibrate_button = tk.Button(text="Calibrate [C]", command=submit)
    calibrate_button.grid(row=4, column=0, columnspan=2)
    root.mainloop()

if __name__ == "__main__":
    main()