# sdc_project

Our software allows a user to create or view SDC files in the form of an Excel spreadsheet. This SDC will have an access control matrix embeded into it to determine role access.

---
## Necessary Files
#### ['ui_module.py']
  > Contains the class **SDCApp** which forms the main GUI that the user will interact with.

  > Contains code that communicates with sdc_module.py, and spreadsheet_viewer.py, which is nessecary to create and view the SDC's.

#### ['sdc_module.py']
  > Contains the functions **create_sdc** and **encrypt_existing_excel** which are what communicate with encryption_module.py to encrypt the data in the excel files.

#### ['spreadsheet_viewer.py']
  > Contains the function **view_sdc** whichis what creates a decrypted excel file for viewing purposes

#### ['encryption_module.py']
  > Contains the functions **encrypt_data** and **decrypt_data** which are needed to encrypt data with AES 128 bit ciphers.

#### ['authentication_module.py']
  > Contains the function **authenticate_user** which is needed to log into the software.

#### ['acm_module.py']
  > Contains the function **generate_acm** which is needed to create the ACM embedded into each SDC.

#### ['users.json']
  > Contains the json file indicating all users, their passwords, and their roles. This file can be modified as needed, but is required for the log in functionality to work.

---
## Necessary Libraries
The libraries used to run this program can be found in requirements.txt. A general list of the modules used to run this program and their documentation can be found below.
* [os](https://docs.python.org/3/library/os.html)
* [json](https://docs.python.org/3/library/json.html)
* [base64](https://docs.python.org/3/library/base64.html)
* [Openpyxl](https://openpyxl.readthedocs.io/en/stable/)
* [PyCryptodome](https://pycryptodome.readthedocs.io/en/latest/)
* [tkinter](https://docs.python.org/3/library/tk.html)

---
## Installation and Running Instructions
1) Attain the files `ui_module.py`, `sdc_module.py`, `spreadsheet_viewer.py`, `encryption_module.py` , `authentication_module.py`, `acm_module.py`, and `users.json` via forking
    **OR** by downloading the specified files to a local repository.
2) Obtain an python IDE (such as [Pycharm](https://www.jetbrains.com/pycharm/download/?section=windows)) or create a [virtual enviroment](https://docs.python.org/3/library/venv.html)
3) Install all the modules to the IDE or virtual environment with `pip install -r requirements.txt`.
4) Make sure all the files are in the virtual envirnoment or IDE before running.
5) Run the program with `python ui_module.py` or if in an IDE the run button. 

---
## Usage Instructions
* Creating an SDC
  > After opening the program, enter the username and password for a dev role from users.json. Upon logging in, select either the `Create New SDC (Blank)` button or the `Import Excel and Encrypt` button.
  > After selecting the `Create New SDC (Blank)` button, simply enter a name to store the SDC under.
  > After selecting the `Import Excel and Encrypt` button, select the excel file you wish to encrypt. Then simply enter a name to store the SDC under.
  
 * Viewing an SDC
  > After opening the program, enter the username and password for a admin, priveleged, user, or guest role from users.json. Upon logging in, select the `Select and View SDC` button.
  > After selecting the `Select and View SDC` button, select the file you wish to view. It must be an SDC file to not return an error. Then simply view the decryted SDC file.
