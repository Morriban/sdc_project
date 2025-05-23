import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from authentication_module import authenticate_user
from sdc_module import create_sdc, encrypt_existing_excel
from spreadsheet_viewer import view_sdc
import os


# This class is responsible for creating the main GUI, and interacting with the other modules
class SDCApp:
    # Creates the initial geometry of the GUI
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Data Container (SDC) System")
        self.root.geometry("400x250")

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self.build_login_screen()

    # Creates the login button, and the entry boxes for the username and password
    def build_login_screen(self):
        tk.Label(self.root, text="Username").pack(pady=5)
        tk.Entry(self.root, textvariable=self.username_var).pack()

        tk.Label(self.root, text="Password").pack(pady=5)
        tk.Entry(self.root, textvariable=self.password_var, show="*").pack()

        tk.Button(self.root, text="Login", command=self.handle_login).pack(pady=20)

    # This method will retrieve the inputted username and password, and call the authentication module to check it.
    # If the module returns the role, then the login was successful and the role menu will be created/called
    # If nothing is returned, then it will show an error message
    def handle_login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "Username and password required.")
            return

        role = authenticate_user(username, password)
        if role:
            messagebox.showinfo("Login Successful", f"Welcome {username}! Role: {role}")
            self.root.withdraw()
            self.launch_role_menu(role)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

    # This method  will create the new menu when a user logs in.
    # If they are a developer, then it will create two new buttons.
    # One button will create a new blank SDC, while the other encrypts an existing Excel file.
    # If they are a normal user, then it will create one button. This button decrypts an SDC.
    def launch_role_menu(self, role):
        menu = tk.Toplevel()
        menu.title(f"Role Menu - {role}")
        menu.geometry("400x250")

        if role == "developer":
            tk.Label(menu, text="You are a Developer").pack(pady=10)
            tk.Button(menu, text="Create New SDC (Blank)", command=create_sdc_gui).pack(pady=5)
            tk.Button(menu, text="Import Excel and Encrypt", command=import_and_encrypt_excel_gui).pack(pady=5)
        else:
            tk.Label(menu, text=f"Logged in as {role}").pack(pady=10)
            tk.Button(menu, text="Select and View SDC", command=lambda: browse_and_view_sdc(role)).pack(pady=10)

        tk.Button(menu, text="Exit", command=self.root.destroy).pack(pady=20)


# This function will ask the user for a name to create the SDC under, and then attempt to call create_sdc
# If it's successful, a success message will be returned and the SDC can be found in files under the given name.
# If it's unsuccessful, an error message will be returned.
def create_sdc_gui():
    sdc_name = simpledialog.askstring("SDC Name", "Enter a name for this new SDC:")
    if sdc_name:
        try:
            create_sdc(sdc_name)
            messagebox.showinfo("Success", f"Blank SDC '{sdc_name}' created successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create SDC: {e}")


# This function will have the user select an Excel file to encrypt.
# It will then ask the user for a name to create the SDC under, and then attempt to call encrypt_existing_excel
# If it's successful, a success message will be returned and the SDC can be found in files under the given name.
# If it's unsuccessful in finding the file, a Cancelled error message will be returned.
# If it's unsuccessful in encrypting the file then an error message will be returned.
def import_and_encrypt_excel_gui():
    file_path = filedialog.askopenfilename(
        title="Select Excel File to Encrypt",
        filetypes=[("Excel files", "*.xlsx")],
        initialdir="."
    )
    if file_path:
        try:
            sdc_name = simpledialog.askstring("SDC Name", "Enter a name for this SDC:")
            if sdc_name:
                encrypt_existing_excel(file_path, sdc_name)
                messagebox.showinfo("Success", f"Excel file encrypted into SDC '{sdc_name}' successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {e}")
    else:
        messagebox.showinfo("Cancelled", "No file selected.")


# This function will have the user select an Excel file (preferably an SDC file)
# It will then attempt to decrypt the file.
# If it's successful, a success message will be returned and the decrypted SDC file can be found in files.
# If the file can't be found then a cancelled error will be returned.
# If it fails to decrypt the file then an error will be returned.
def browse_and_view_sdc(role):
    file_path = filedialog.askopenfilename(
        title="Select an SDC Excel File",
        filetypes=[("Excel files", "*.xlsx")],
        initialdir="data/sdcs"
    )
    print(file_path)
    if file_path:
        try:
            sdc_dir = os.path.dirname(file_path)
            sdc_name = os.path.basename(sdc_dir)
            view_sdc(role, file_path)
            messagebox.showinfo("Success", f"Decrypted view for '{role}' saved in '{sdc_name}' folder.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to view SDC: {str(e)}")
    else:
        messagebox.showinfo("Cancelled", "No file selected.")


# The main function to run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = SDCApp(root)
    root.mainloop()
