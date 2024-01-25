import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import sv_ttk
import subprocess
import pyperclip
import json
import ctypes

def save_and_launch(*args):
  # Obtenir des données à partir des entrées
  user = user_entry.get()
  password = password_entry.get()
  host = host_entry.get()
  database = database_entry.get()

  # Vérifier que trois champs sont remplis (le mot de passe peut être une chaîne vide)
  if not all([user, host, database]):
    messagebox.showerror("Erreur", "Merci de remplir tous les champs")
    return

    # Enregistrer les données dans un fichier json
  data = {
    "user": user,
    "password": password,
    "host": host,
    "database": database
  }

  with open("config.json", "w") as json_file:
    json.dump(data, json_file)

  # fermer la fenêtre de connexion
  root.destroy()
  # Exécuter le fichier pydo.pyw
  subprocess.run(["python", "pydo.pyw"])

def show_sql_code():
  # Créer une nouvelle fenêtre
  sql_window = tk.Toplevel(root)
  sql_window.title("Code SQL")
  ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('arbitrary string')
  sql_window.iconbitmap('pydo.ico')

  # Créer un widget Texte pour afficher le code SQL
  sql_text = scrolledtext.ScrolledText(sql_window, wrap=tk.WORD, width=40, height=20)
  sql_text.pack(padx=10, pady=10)

  # Code SQL pour créer la base de données requise
  sql_code = """
    CREATE TABLE tache(
    tache_id INT AUTO_INCREMENT,
    tache_libelle VARCHAR(50) ,
    date_creation DATETIME,
    date_fixee DATETIME,
    date_realisation DATETIME,
    PRIMARY KEY(tache_id)
    );

    CREATE TABLE etat(
    etat_id INT AUTO_INCREMENT,
    etat_nom VARCHAR(50) ,
    tache_id INT NOT NULL,
    PRIMARY KEY(etat_id),
    FOREIGN KEY(tache_id) REFERENCES tache(tache_id)
    );
  """

  # Fonction pour enregistrer le code SQL dans le presse-papiers
  def copy_to_clipboard():
    pyperclip.copy(sql_code)

  # Bouton pour copier le code SQL
  copy_button = ttk.Button(sql_window, text="Copier dans le presse-papier", command=copy_to_clipboard)
  copy_button.pack(pady=10)

  sql_text.insert(tk.END, sql_code)

# Fenêtre principale pour la saisie des données
root = tk.Tk()
root.title("Connexion à la base de données")
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('arbitrary string')
root.iconbitmap('pydo.ico')

# Création des entrées
user_label = ttk.Label(root, text="Utilisateur:")
user_label.grid(row=0, column=0, padx=10, pady=5)
user_entry = ttk.Entry(root)
user_entry.insert(0, "root")
user_entry.grid(row=0, column=1, padx=10, pady=5)
user_entry.bind("<Return>", save_and_launch)

password_label = ttk.Label(root, text="Mot de passe:")
password_label.grid(row=1, column=0, padx=10, pady=5)
password_entry = ttk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=5)
password_entry.bind("<Return>", save_and_launch)

host_label = ttk.Label(root, text="Hôte:")
host_label.grid(row=2, column=0, padx=10, pady=5)
host_entry = ttk.Entry(root)
host_entry.insert(0, "localhost")
host_entry.grid(row=2, column=1, padx=10, pady=5)
host_entry.bind("<Return>", save_and_launch)

database_label = ttk.Label(root, text="Base de données:")
database_label.grid(row=3, column=0, padx=10, pady=5)
database_entry = ttk.Entry(root)
database_entry.insert(0, "pydo")
database_entry.grid(row=3, column=1, padx=10, pady=5)
database_entry.bind("<Return>", save_and_launch)


save_button = ttk.Button(root, text="Enregistrer et lancer", command=save_and_launch)
save_button.grid(row=4, column=0, pady=10, padx=20)

# Bouton pour afficher le code SQL
sql_button = ttk.Button(root, text="Afficher le code SQL", command=show_sql_code)
sql_button.grid(row=4, column=1, columnspan=2, pady=10)

sv_ttk.set_theme("light")
root.mainloop()
