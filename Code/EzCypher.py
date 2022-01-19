import tkinter as tk
import os
from tkinter import filedialog
from tkinter import messagebox
from cryptography.fernet import Fernet

# ~~~~~~
# VARS
# ~~~~~~
window = tk.Tk()
window.geometry('350x300')
window.title('EzCypher')
window.resizable(width=False, height=False)

selected = tk.IntVar()
folder_path = ''
app_name = os.path.basename(__file__)
encoding = '.b64'
key = Fernet('YiB7ph9p8_TzDo24f5U3F__xnL4fvPt3xu_jVBR64rM=')

# ~~~~~~~~~~~~
# FUNCTIONS
# ~~~~~~~~~~~~
# Run over every element in the directory and execute operation
def iterateOverDirectory(encryptFiles, path):
    for dirPath, dirName, files in os.walk(path, topdown=False):
        for file_name in files:
            if (file_name != app_name):  # avoid encypting the program itself
                if (encryptFiles and encoding not in file_name):
                    encryptFile(os.path.join(dirPath, file_name))
                else:
                    decryptFile(os.path.join(dirPath, file_name))

# READ ORIGINAL FILE
def readFile(file_name):
    with open(file_name, 'rb') as file:
        return file.read()


# ENCRYPT FILE
def encryptFile(file_name):
    # encrypting the file
    encrypted = key.encrypt(readFile(file_name))

    # opening the file in write mode and writing the encrypted data
    with open(file_name, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

    # renaming the file
    os.rename(file_name, file_name + encoding)


# DECRYPT FILE
def decryptFile(file_name):
    # decrypting the file
    decrypted = key.decrypt(readFile(file_name))

    # opening the file in write mode and writing the decrypted data
    with open(file_name, 'wb') as dec_file:
        dec_file.write(decrypted)

    # renaming the file
    os.rename(file_name, file_name[:-4])


# ALLOW USER TO SELECT A DIRECTORY AND STORE IT
def browse_button():
    global folder_path
    filename = filedialog.askdirectory()
    folder_path = filename
    label4.config(text=folder_path)

# RUN PROGRAM WITH SELECTED RADIO OPTION
def run():
    if (selected.get() == 1 and folder_path):
        iterateOverDirectory(True, folder_path)
        messagebox.showinfo('Done', 'All contents were cyphered')
    elif (selected.get() == 2 and folder_path):
        iterateOverDirectory(False, folder_path)
        messagebox.showinfo('Done', 'All contents were decyphered')
    else:
        print(selected, ' ', folder_path)
        messagebox.showinfo('Error', 'Please fill all the options')


# ~~~
# GUI
# ~~~
# VIEW DECLARATIONS
rad1 = tk.Radiobutton(window, text='Encrypt', value=1, variable=selected)
rad2 = tk.Radiobutton(window, text='Decrypt', value=2, variable=selected)
label1 = tk.Label(window, text='This app will encrypt all files contained in the\n specyfied  directory, USE WITH CAUTION.')
label2 = tk.Label(window, text='Select action to perform:')
label3 = tk.Label(window, text='Select location:')
button1 = tk.Button(text='Browse', command=browse_button)
button2 = tk.Button(window, text='Run', command=run)
label4 = tk.Label(window, text='')

# POSITIONING
label1.grid(columnspan=2, row=0, ipadx=10, ipady=8, padx=10, pady=8)
label2.grid(columnspan=2, row=1)

rad2.grid(column=1, row=2, ipadx=0, ipady=8, padx=0, pady=8)
rad1.grid(column=0, row=2, ipadx=0, ipady=8, padx=0, pady=8)

label3.grid(column=0, row=3, pady=5)
button1.grid(column=1, row=3, pady=5)

label4.grid(columnspan=2, row=4, pady=8)

button2.grid(columnspan=2, row=5, pady=10)

# start gui
window.mainloop()