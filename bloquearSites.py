import os
import sys
import ctypes
from tkinter import Tk, Entry, messagebox, ttk, Listbox, Button, Toplevel
from tkinter.ttk import Style

def is_admin():
    """Verifica se o programa está rodando como administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Reinicia o programa com privilégios de administrador."""
    script = os.path.abspath(sys.argv[0])
    params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
    sys.exit()

def block_site(site):
    """Bloquear o site no arquivo hosts."""
    if not site:
        messagebox.showerror("Erro", "Por favor, insira um site para bloquear.")
        return

    site = site.replace("http://", "").replace("https://", "").strip("/")
    
    try:
        hosts_path = r"C:\\Windows\\System32\\drivers\\etc\\hosts"
        with open(hosts_path, "r+") as hosts_file:
            lines = hosts_file.readlines()
            entry = f"127.0.0.1 {site}\n"
            hosts_file.seek(0)
            hosts_file.truncate()
            site_blocked = False
            for line in lines:
                if line.strip() == f"#{entry.strip()}":
                    hosts_file.write(entry)  
                    site_blocked = True
                else:
                    hosts_file.write(line)
            if not site_blocked:
                if entry not in lines:
                    hosts_file.write(entry)
                    messagebox.showinfo("Sucesso", f"Site '{site}' foi bloqueado! \nPor favor reinicie seu navegador para que o bloqueio entre em vigor.")
                else:
                    messagebox.showinfo("Informação", f"O site '{site}' já está bloqueado.")
            else:
                messagebox.showinfo("Sucesso", f"Site '{site}' foi bloqueado! \nPor favor reinicie seu navegador para que o bloqueio entre em vigor.")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao bloquear o site:\n{e}")

def unblock_site(site):
    """Desbloquear o site no arquivo hosts."""
    if not site:
        messagebox.showerror("Erro", "Por favor, selecione um site para desbloquear.")
        return

    try:
        hosts_path = r"C:\\Windows\\System32\\drivers\\etc\\hosts"
        with open(hosts_path, "r+") as hosts_file:
            lines = hosts_file.readlines()
            hosts_file.seek(0)
            hosts_file.truncate()
            for line in lines:
                if line.strip() == f"127.0.0.1 {site}":
                    hosts_file.write(f"#{line}")
                else:
                    hosts_file.write(line)
        messagebox.showinfo("Sucesso", f"Site '{site}' foi desbloqueado!")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao desbloquear o site:\n{e}")

def get_blocked_sites():
    """Obtém a lista de sites bloqueados no arquivo hosts."""
    try:
        hosts_path = r"C:\\Windows\\System32\\drivers\\etc\\hosts"
        with open(hosts_path, "r") as hosts_file:
            lines = hosts_file.readlines()
            blocked_sites = [line.split()[1] for line in lines if line.startswith("127.0.0.1")]
        return blocked_sites
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao carregar sites bloqueados:\n{e}")
        return []

def center_window(root, width, height):
    """Centralizar a janela na tela."""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width // 2) - (width // 2)
    y_coordinate = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

def open_blocked_sites_window():
    """Abre uma nova janela para gerenciar sites bloqueados."""
    blocked_sites_window = Toplevel()
    blocked_sites_window.title("Gerenciar Sites Bloqueados")
    width, height = 450, 400
    center_window(blocked_sites_window, width, height)
    blocked_sites_window.resizable(False, False)

    def on_unblock_button_click():
        selected_site = blocked_sites_listbox.get(blocked_sites_listbox.curselection())
        unblock_site(selected_site)
        refresh_blocked_sites()

    def refresh_blocked_sites():
        blocked_sites = get_blocked_sites()
        blocked_sites_listbox.delete(0, "end")
        for site in blocked_sites:
            blocked_sites_listbox.insert("end", site)

    main_frame = ttk.Frame(blocked_sites_window, padding="20")
    main_frame.pack(fill="both", expand=True)

    title_label = ttk.Label(main_frame, text="Sites Bloqueados", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    blocked_sites_listbox = Listbox(main_frame, height=15, width=50)
    blocked_sites_listbox.pack(pady=5)

    unblock_button = Button(main_frame, text="Desbloquear Site", command=on_unblock_button_click)
    unblock_button.pack(pady=10)

    refresh_blocked_sites()

def main():
    if not is_admin():
        run_as_admin()

    def on_block_button_click():
        site = site_entry.get()
        block_site(site)

    root = Tk()
    root.title("Bloqueador de Websites")
    width, height = 450, 400
    center_window(root, width, height)
    root.resizable(False, False)

    style = Style()
    style.theme_use("clam")  
    style.configure("TFrame", background="#2C2F33")  
    style.configure("TLabel", background="#2C2F33", foreground="#FFFFFF", font=("Arial", 11))  
    style.configure("TButton", background="#7289DA", foreground="#FFFFFF", font=("Arial", 10, "bold"), padding=5)  

    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill="both", expand=True)

    title_label = ttk.Label(main_frame, text="Bloqueador de Sites", font=("Arial", 16, "bold"), anchor="center")
    title_label.pack(pady=10)

    site_label = ttk.Label(main_frame, text="Insira o site que deseja bloquear:")
    site_label.pack(pady=5)

    site_entry = ttk.Entry(main_frame, width=50, font=("Arial", 10))
    site_entry.pack(pady=5, ipady=3)

    block_button = ttk.Button(main_frame, text="Bloquear Site", command=on_block_button_click)
    block_button.pack(pady=10)

    view_blocked_button = ttk.Button(main_frame, text="Ver Sites Bloqueados", command=open_blocked_sites_window)
    view_blocked_button.pack(pady=10)

    ttk.Separator(main_frame, orient="horizontal").pack(fill="x", pady=10)

    instructions_frame = ttk.Frame(main_frame)
    instructions_frame.pack(fill="x", pady=5)

    site_label = ttk.Label(instructions_frame, text="Para maior eficácia, experimente colocar a URL limpa.")
    site_label.pack(anchor="w")

    site_label_instruction_1 = ttk.Label(instructions_frame, text="Em vez de: https://www.facebook.com/", anchor="w")
    site_label_instruction_1.pack(anchor="w")

    site_label_instruction_2 = ttk.Label(instructions_frame, text="Coloque: www.facebook.com", anchor="w")
    site_label_instruction_2.pack(anchor="w")

    root.mainloop()



if __name__ == "__main__":
    main()
