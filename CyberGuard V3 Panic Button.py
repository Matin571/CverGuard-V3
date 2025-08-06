import tkinter as tk
from tkinter import messagebox, font
import subprocess
import ctypes

# Functions to perform actions
def kill_user_processes():
    tasks = subprocess.check_output('tasklist', shell=True).decode()
    for line in tasks.splitlines()[3:]:
        parts = line.split()
        if len(parts) >= 2:
            process_name = parts[0]
            pid = parts[1]
            system_processes = ['System', 'svchost.exe', 'winlogon.exe', 'csrss.exe', 'explorer.exe']
            if process_name.lower() not in [sp.lower() for sp in system_processes]:
                try:
                    subprocess.run(f'taskkill /PID {pid} /F', shell=True)
                except:
                    pass

def disable_internet():
    try:
        interfaces = subprocess.check_output('netsh interface show interface', shell=True).decode()
        for line in interfaces.splitlines():
            if 'Enabled' in line and ('Connected' in line or 'Disconnected' in line):
                parts = line.split()
                interface_name = ' '.join(parts[3:])
                subprocess.run(f'netsh interface set interface "{interface_name}" admin=disable', shell=True)
    except:
        pass

def panic_button_action():
    if ctypes.windll.shell32.IsUserAnAdmin():
        kill_user_processes()
        disable_internet()
        messagebox.showinfo("Operation Completed", "All applications have been closed and internet connection disabled.")
    else:
        messagebox.showwarning("Permission Error", "Please run the program as administrator!")

# Panic button confirmation window
def open_panic_window():
    panic_win = tk.Toplevel(root)
    panic_win.title("Panic Button Confirmation")
    panic_win.geometry("420x220")
    panic_win.resizable(False, False)
    panic_win.configure(bg="#2c3e50")

    label = tk.Label(panic_win, 
                     text="You are about to activate the Panic Button.\n\n"
                          "This will forcibly close all applications and disable the internet connection.\n"
                          "Are you sure you want to proceed?",
                     bg="#2c3e50", fg="white", font=("Segoe UI", 12), justify="center")
    label.pack(pady=25, padx=20)

    btn_frame = tk.Frame(panic_win, bg="#2c3e50")
    btn_frame.pack(pady=10)

    def confirm_panic():
        panic_button_action()
        panic_win.destroy()

    btn_yes = tk.Button(btn_frame, text="Yes, Proceed", bg="#e74c3c", fg="white", font=("Segoe UI", 11, "bold"),
                        activebackground="#c0392b", activeforeground="white", width=15, command=confirm_panic)
    btn_yes.grid(row=0, column=0, padx=10)

    btn_no = tk.Button(btn_frame, text="Cancel", bg="#95a5a6", fg="white", font=("Segoe UI", 11),
                       activebackground="#7f8c8d", activeforeground="white", width=15, command=panic_win.destroy)
    btn_no.grid(row=0, column=1, padx=10)

# Initial agreement popup
def show_agreement_and_start():
    agreement_text = (
        "You must accept the terms of use for CyberGuard V3 Panic Button.\n\n"
        "This program will forcibly close all your open applications and disable your internet connection.\n"
        "This action is irreversible and may cause data loss.\n"
        "You are fully responsible for any hardware malfunctions or other technical issues.\n\n"
        "This software is not malicious, but you must acknowledge all risks.\n\n"
        "The program will not start without user consent.\n\n"
        "Do you accept?"
    )
    if messagebox.askyesno("Terms of Use and Disclaimer", agreement_text):
        start_main_window()
    else:
        messagebox.showinfo("Consent Required", "Program will close.")
        root.destroy()

# Start main window
def start_main_window():
    root.deiconify()  # Show hidden window
    root.title("CyberGuard V3 Panic Button")
    root.geometry("450x250")
    root.configure(bg="#34495e")
    root.resizable(False, False)

    title_font = ("Segoe UI", 20, "bold")
    btn_font = ("Segoe UI", 14, "bold")

    label = tk.Label(root, text="CyberGuard V3 Main Panel", bg="#34495e", fg="white", font=title_font)
    label.pack(pady=30)

    panic_button = tk.Button(root, text="OPEN PANIC BUTTON", bg="#e74c3c", fg="white", font=btn_font,
                             activebackground="#c0392b", activeforeground="white", width=20,
                             command=open_panic_window)
    panic_button.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide window at start
    show_agreement_and_start()
    root.mainloop()
