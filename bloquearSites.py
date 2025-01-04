import os
import sys
import ctypes
from tkinter import Tk, Entry, messagebox, ttk
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

    # Formatar o site
    site = site.replace("http://", "").replace("https://", "").strip("/")
    
    try:
        hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        with open(hosts_path, "r+") as hosts_file:
            lines = hosts_file.readlines()
            entry = f"127.0.0.1 {site}\n"
            if entry not in lines:
                hosts_file.write(entry)
                messagebox.showinfo("Sucesso", f"Site '{site}' foi bloqueado! \nPor favor reinicie seu navegador para que o bloqueio entre em vigor.")
            else:
                messagebox.showinfo("Informação", f"O site '{site}' já está bloqueado.")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao bloquear o site:\n{e}")

def center_window(root, width, height):
    """Centralizar a janela na tela."""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width // 2) - (width // 2)
    y_coordinate = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

def main():
    if not is_admin():
        run_as_admin()

    def on_block_button_click():
        site = site_entry.get()
        block_site(site)

    root = Tk()
    root.title("Bloqueador de Websites")
    width, height = 450, 350
    center_window(root, width, height)
    root.resizable(False, False)

    # Estilo do programa
    style = Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#f0f0f0")
    style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
    style.configure("TButton", background="#0078d7", foreground="white", font=("Arial", 10, "bold"), padding=5)

    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill="both", expand=True)

    title_label = ttk.Label(main_frame, text="Bloqueador de Sites", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    site_label = ttk.Label(main_frame, text="Insira o site que deseja bloquear:")
    site_label.pack(pady=5)

    site_entry = ttk.Entry(main_frame, width=50)
    site_entry.pack(pady=5)

    block_button = ttk.Button(main_frame, text="Bloquear Site", command=on_block_button_click)
    block_button.pack(pady=20)
    
    ttk.Separator(main_frame, orient="horizontal").pack(fill="x", pady=10)

    site_label = ttk.Label(main_frame, text="Para maior eficácia, experimente colocar a URL limpa.")
    site_label.pack(pady=5)
    
    site_label_instruction_1 = ttk.Label(main_frame, text="Em vez de: https://www.facebook.com/", anchor="w")
    site_label_instruction_1.pack(fill="x", pady=2)

    site_label_instruction_2 = ttk.Label(main_frame, text="Coloque: www.facebook.com", anchor="w")
    site_label_instruction_2.pack(fill="x", pady=2)

    root.mainloop()

if __name__ == "__main__":
    main()
