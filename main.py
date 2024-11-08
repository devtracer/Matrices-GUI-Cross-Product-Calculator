import customtkinter as ctk
from tkinter import messagebox

# Set the appearance and default color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


# The main app class for Matrix Calculator
class MatrixInputApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Matrices GUI Cross Product Calculator")  # The app's name
        self.geometry("800x500")
        # Default matrix dimensions for a and b (3x3)
        self.rows_a, self.cols_a = 3, 3
        self.rows_b, self.cols_b = 3, 3
        self.setup_dimension_inputs()

        # Buttons for user interactions
        self.generate_button = ctk.CTkButton(self, text="Generate Matrices", command=self.generate_matrices)
        self.generate_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.calculate_button = ctk.CTkButton(self, text="Calculate Cross Product", command=self.calculate_cross_product)
        self.calculate_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.clear_button = ctk.CTkButton(self, text="Clear Matrices", command=self.clear_all)
        self.clear_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.all_widgets = []
        self.matrix_entries_a = []
        self.matrix_entries_b = []
        self.result_entries = []

        # Configuring the grid layout
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_columnconfigure(0, weight=1)

    def setup_dimension_inputs(self):
        # Set up the dimension input fields for matrices A and B
        dim_frame = ctk.CTkFrame(self)
        dim_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.grid_rowconfigure(0, weight=0)

        # Matrix A dimensions
        ctk.CTkLabel(dim_frame, text="Matrix A Rows:").grid(row=0, column=0, padx=5, pady=5)
        self.rows_a_entry = ctk.CTkEntry(dim_frame, width=50)
        self.rows_a_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(dim_frame, text="Matrix A Columns:").grid(row=0, column=2, padx=5, pady=5)
        self.cols_a_entry = ctk.CTkEntry(dim_frame, width=50)
        self.cols_a_entry.grid(row=0, column=3, padx=5, pady=5)

        # Matrix B dimensions
        ctk.CTkLabel(dim_frame, text="Matrix B Rows:").grid(row=1, column=0, padx=5, pady=5)
        self.rows_b_entry = ctk.CTkEntry(dim_frame, width=50)
        self.rows_b_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(dim_frame, text="Matrix B Columns:").grid(row=1, column=2, padx=5, pady=5)
        self.cols_b_entry = ctk.CTkEntry(dim_frame, width=50)
        self.cols_b_entry.grid(row=1, column=3, padx=5, pady=5)

    def generate_matrices(self):
        # Generate matrices based on user input
        self.rows_a = self.get_dimension(self.rows_a_entry, 3)
        self.cols_a = self.get_dimension(self.cols_a_entry, 3)
        self.rows_b = self.get_dimension(self.rows_b_entry, 3)
        self.cols_b = self.get_dimension(self.cols_b_entry, 3)

        # Ensure the number of columns in Matrix A matches the number of rows in Matrix B
        if self.cols_a != self.rows_b:
            messagebox.showerror("Dimension Error", "Matrix A columns must match Matrix B rows for multiplication.")
            return

        # Clear all previous matrix widgets before generating new ones
        self.clear_all_matrix_widgets()

        # Create a new frame to display the matrices
        frame = ctk.CTkFrame(self)
        frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        self.all_widgets.append(frame)

        # Create matrix A with entry widgets
        self.matrix_entries_a = self.create_matrix_entries(self.rows_a, self.cols_a, frame, 0)

        # Label for the multiplication sign (X)
        x_label = ctk.CTkLabel(frame, text="X", font=("Arial", 24))
        x_label.grid(row=self.rows_a // 2, column=self.cols_a + 1, padx=10)
        self.all_widgets.append(x_label)

        # Create matrix B with entry widgets
        self.matrix_entries_b = self.create_matrix_entries(self.rows_b, self.cols_b, frame, self.cols_a + 2)

    def clear_all_matrix_widgets(self):
        # Clear all matrix-related widgets from the screen
        for widget in self.all_widgets:
            widget.destroy()
        self.all_widgets.clear()
        self.matrix_entries_a.clear()
        self.matrix_entries_b.clear()
        self.result_entries.clear()

    def create_matrix_entries(self, rows, cols, parent_frame, start_col):
        # Create entry widgets for matrix cells
        entries = []
        for i in range(rows):
            row_entries = []
            for j in range(cols):
                entry = ctk.CTkEntry(parent_frame, width=50)
                entry.grid(row=i, column=start_col + j, padx=5, pady=5)
                row_entries.append(entry)
                self.all_widgets.append(entry)
            entries.append(row_entries)
        return entries

    def collect_matrices(self):
        # Collect values from matrix entry widgets and return matrices
        matrix_a = self.get_matrix_values(self.matrix_entries_a, self.rows_a, self.cols_a)
        matrix_b = self.get_matrix_values(self.matrix_entries_b, self.rows_b, self.cols_b)
        return matrix_a, matrix_b

    def get_matrix_values(self, entries, rows, cols):
        # Convert the values in matrix entry widgets to a matrix (list of lists)
        matrix = []
        for i in range(rows):
            row = []
            for j in range(cols):
                entry = entries[i][j]
                row.append(self.get_entry_value(entry))
            matrix.append(row)
        return matrix

    def get_entry_value(self, entry):
        # Get the value from an entry widget, or default to 0 if it's invalid
        try:
            return int(entry.get())
        except (ValueError, TypeError):
            return 0

    def get_dimension(self, entry, default):
        # Get matrix dimension value (rows or columns), defaulting to a value if the entry is invalid
        try:
            value = int(entry.get())
            return max(1, value)
        except ValueError:
            return default

    def calculate_cross_product(self):
        # Calculate the cross product of matrices A and B
        try:
            matrix_a, matrix_b = self.collect_matrices()
            if len(matrix_a[0]) != len(matrix_b):
                messagebox.showerror("Dimension Error", "Matrix A columns must match Matrix B rows for multiplication.")
                return

            # for every row of the first matrix and for every column of the second matrix, zip them together.
            # now if we select a and b from this zip, we can go in order to grab items as we should.
            # we then cross a and b together
            # now, different cross products get produced.
            # we'll then sum them and will have that as one of the elements of this result list.
            result = [[sum(a * b for a, b in zip(row_a, col_b)) for col_b in zip(*matrix_b)] for row_a in matrix_a]

            # Clear previous result if any
            if self.result_entries:
                for entry_row in self.result_entries:
                    for entry in entry_row:
                        entry.destroy()
                self.result_entries.clear()

            # Display the "=" label
            equals_label = ctk.CTkLabel(self.all_widgets[0], text="=", font=("Arial", 24))
            equals_label.grid(row=self.rows_a // 2, column=self.cols_a + self.cols_b + 3, padx=10)
            self.all_widgets.append(equals_label)

            # Create result matrix display
            self.result_entries = self.create_result_matrix_entries(result, self.all_widgets[0], self.cols_a + self.cols_b + 4)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def create_result_matrix_entries(self, matrix, parent_frame, start_col):
        # Display the result matrix in entry widgets (read-only)
        entries = []
        for i, row in enumerate(matrix):
            row_entries = []
            for j, value in enumerate(row):
                entry = ctk.CTkEntry(parent_frame, width=50)
                entry.insert(0, str(value))
                entry.configure(state="readonly")
                entry.grid(row=i, column=start_col + j, padx=5, pady=5)
                row_entries.append(entry)
                self.all_widgets.append(entry)
            entries.append(row_entries)
        return entries

    def clear_all(self):
        # Clear all matrices and reset the dimensions
        self.clear_all_matrix_widgets()
        self.rows_a_entry.delete(0, ctk.END)
        self.cols_a_entry.delete(0, ctk.END)
        self.rows_b_entry.delete(0, ctk.END)
        self.cols_b_entry.delete(0, ctk.END)
        self.rows_a, self.cols_a = 3, 3
        self.rows_b, self.cols_b = 3, 3


if __name__ == "__main__":
    app = MatrixInputApp()
    app.mainloop()
