import subprocess
import webbrowser
import os
import sys
import ctypes
import time
import shutil
import tkinter as tk
import pickle
from tkinter import filedialog

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_as_admin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return

    script = sys.argv[0]
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script, None, 1)

def save_data(data, filename):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)
    else:
        return []

def add_application(wybrane_aplikacje):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select application", filetypes=[("Executable files", "*.exe")])

    if file_path:
        wybrane_aplikacje.append(file_path)
        print("Selected file:", os.path.basename(file_path))
        print("It will be moved to '2. Select previously chosen application'")
        time.sleep(3)

def add_shortcut(wybrane_linki):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select internet shortcut", filetypes=[("Shortcut files", "*.url")])

    if file_path:
        wybrane_linki.append(file_path)
        print("Selected shortcut:", file_path)
        print("It will be moved to '2. Select previously chosen application'")
        time.sleep(3)

def run_application(wybrane_aplikacje, sub_choice):
    if sub_choice.isdigit() and int(sub_choice) in range(1, len(wybrane_aplikacje) + 1):
        aplikacja_indeks = int(sub_choice) - 1
        subprocess.run([wybrane_aplikacje[aplikacja_indeks]])

def open_link(wybrane_linki, sub_choice):
    if sub_choice.isdigit() and int(sub_choice) in range(1, len(wybrane_linki) + 1):
        linki_indeks = int(sub_choice) - 1
        with open(wybrane_linki[linki_indeks], "r") as url_file:
            for line in url_file.readlines():
                if line.startswith("URL="):
                    to_run = line[4:]
                    os.startfile(to_run)
                    break

def main():
    choice = ""
    sub_choice = ""
    wybrane_aplikacje = load_data('aplikacje.pkl')
    wybrane_linki = load_data('linki.pkl')

    while choice != "q":
        clear_console()
        ascii_art = """
          /$$$$$$ /$$$$$$ /$$$$$$        /$$       /$$$$$$ /$$   /$$/$$   /$$ /$$$$$$ /$$   /$$/$$$$$$$$/$$$$$$$ 
         /$$__  $|_  $$_//$$__  $$      | $$      /$$__  $| $$  | $| $$$ | $$/$$__  $| $$  | $| $$_____| $$__  $$
        | $$  \ $$ | $$ | $$  \ $$      | $$     | $$  \ $| $$  | $| $$$$| $| $$  \__| $$  | $| $$     | $$  \ $$
        | $$$$$$$$ | $$ | $$  | $$      | $$     | $$$$$$$| $$  | $| $$ $$ $| $$     | $$$$$$$| $$$$$  | $$$$$$$/
        | $$__  $$ | $$ | $$  | $$      | $$     | $$__  $| $$  | $| $$  $$$| $$     | $$__  $| $$__/  | $$__  $$
        | $$  | $$ | $$ | $$  | $$      | $$     | $$  | $| $$  | $| $$\  $$| $$    $| $$  | $| $$     | $$  \ $$
        | $$  | $$/$$$$$|  $$$$$$/      | $$$$$$$| $$  | $|  $$$$$$| $$ \  $|  $$$$$$| $$  | $| $$$$$$$| $$  | $$
        |__/  |__|______/\______/       |________|__/  |__/\______/|__/  \__/\______/|__/  |__|________|__/  |__/ 
        by klepeczek#1991
        """
        print(ascii_art)
        print("Select an action:")
        print("1. Add applications")
        print("2. Select previously chosen application")
        print("3. Select previously chosen Steam game")
        print("4. Configuration options")
        print("Note: Changes will not be saved without using the 'q' command!")
        choice = input("Select the action number (or 'q' to save): ")

        if choice == "1":
            sub_choice = ""

            while sub_choice != "q":
                clear_console()
                print("1. Add .exe application")
                print("2. Add Steam shortcut or website shortcut.")
                sub_choice = input("Select the launcher number (or 'q' to go back): ")

                if sub_choice == "1":
                    add_application(wybrane_aplikacje)
                elif sub_choice == "2":
                    add_shortcut(wybrane_linki)
                elif sub_choice == "q":
                    break
                else:
                    print("Invalid choice.")
                    time.sleep(1)

        if choice == "2":
            clear_console()
            for i, aplikacja in enumerate(wybrane_aplikacje):
                print(f"{i+1}. {os.path.basename(aplikacja)}")
            sub_choice = input("Select a previously chosen application (or 'q' to exit): ")
            run_application(wybrane_aplikacje, sub_choice)
        if choice == "3":
            clear_console()
            for i, linki in enumerate(wybrane_linki):
                print(f"{i+1}. {os.path.basename(linki)}")
            sub_choice = input("Select a previously chosen link (or 'q' to exit): ")
            open_link(wybrane_linki, sub_choice)
        elif choice == "q":
                break
        time.sleep(1)

        if choice == "4":
            sub_choice = ""
            while sub_choice != "q":
                clear_console()
                print("1. Add script to startup.")
        
                sub_choice = input("Select an option number (or 'q' to go back): ")

                if sub_choice == "1":
                    confirm = input("Are you sure you want this program to run on startup? (1 - Yes, 2 - No): ")
                    if confirm == "1":
                        startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
                        script_path = os.path.abspath(sys.argv[0])
                        shutil.copy(script_path, startup_folder)
                        print("Added to startup.")
                        time.sleep(2)
                elif sub_choice == "q":
                    save_data(wybrane_aplikacje, 'aplikacje.pkl')
                    save_data(wybrane_linki, 'linki.pkl')

if __name__ == "__main__":
    main()
