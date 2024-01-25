import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from tkcalendar import DateEntry
import sv_ttk
import ctypes
from PIL import Image, ImageTk
import html
from app import add_todo, get_all_tasks, delete_todo, update_status_todo, edit_todo

# Rendre les boutons actifs ou inactifs en fonction de l'état de la tâche. Utiliser l'événement click sur une tâche
def on_treeview_select(event):
  selected_item = tree.selection()
  if selected_item:
    values = tree.item(selected_item, 'values')
    column_value = values[len(values) - 2] if values else None

    start_button.config(state=tk.NORMAL if column_value == "À faire" or column_value == "Terminée" else tk.DISABLED)
    pause_button.config(state=tk.NORMAL if column_value == "En cours" else tk.DISABLED)
    stop_button.config(state=tk.NORMAL if column_value == "En cours" else tk.DISABLED)
  else:
    start_button.config(state=tk.DISABLED)
    pause_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.DISABLED)

# Ajouter une nouvelle tâche. Si l'entree est vide, on demande au moins un caractère.
# 'Date fixée' par défaut est fixée une semaine à l'avance. Cela peut être modifié
def on_submit_click(*args):
  user_input = entry.get()
  end_date = date_entry.get()
  error = False

  try:
    if len(user_input) < 1 or user_input == "Saisir une tâche":
      error = True
      message = "La tâche doit contenir au moins un caractère"
    else:
      add_todo(user_input, end_date)
      date_entry.set_date(datetime.now() + timedelta(days=7))
      message = "Informations enregistrées"

  except Exception as err:
    message = "Une erreur s'est produite"
    error = True
  
  finally:
    entry.delete(0, tk.END)
    info_label.config(text=message, fg="green" if not error else "red")
    fenetre.after(2000, clear_info_label)
    update_listbox()

# Supprimer une tâche en appuyant sur un bouton ou une touche
# *args permet de traiter l'événement keypress
def on_delete_click(*args):
  selected_item = tree.selection()
  if selected_item:
    values = tree.item(selected_item)['values']
    tache_id = values[len(values) - 1]
    error = False
  try:
    delete_todo(tache_id)
    message = "La tâche a été supprimée avec succès"

  # Si la tâche n'est pas sélectionnée, on demande de le faire.
  except Exception as err:
    message = "Vous devez sélectionner une tâche pour la supprimer"
    error = True
  
  finally:
    info_label.config(text=message, fg="green" if not error else "red")
    fenetre.after(2000, clear_info_label)
    update_listbox()

def on_edit_button_click(*args):
  selected_item = tree.selection()
  if not selected_item:
    message = "Vous devez sélectionner une tâche à modifier"
    info_label.config(text=message, fg="red")
    fenetre.after(2000, clear_info_label)
    update_listbox()
    return
  
  values = tree.item(selected_item)['values']
  tache_id = values[len(values) - 1]

  # éditer la tâche dans une nouvelle fenêtre
  edit_window = tk.Toplevel(fenetre)
  edit_window.title("Modifier une tâche")

  task_data = tree.item(selected_item, "values")

  label_label = tk.Label(edit_window, text="Description de la tâche:")
  label_label.grid(row=0, column=0, padx=10, pady=5)

  label_entry = ttk.Entry(edit_window, width=30)
  label_entry.insert(0, task_data[1])
  label_entry.grid(row=0, column=1, padx=10, pady=5)

  def save_changes(*args):
    new_label = label_entry.get()

    if len(new_label) < 1:
      edit_window.destroy()
      info_label.config(text="La tâche doit contenir au moins un caractère", fg="red")
      fenetre.after(2000, clear_info_label)
      update_listbox()
      return

    edit_todo(tache_id, new_label)

    update_listbox()
    edit_window.destroy()

  save_button = ttk.Button(edit_window, text="Sauvegarder", command=save_changes)
  save_button.grid(row=2, column=0, columnspan=2, pady=10)
  label_entry.bind("<Return>", save_changes)

# Modification de l'état de la tâche en fonction du bouton enfoncé
def on_update_status_click(button_name):
  selected_item = tree.selection()
  if selected_item:
    values = tree.item(selected_item)['values']
    tache_id = values[len(values) - 1]
    error = False
    new_status = ""
    if button_name == "start":
      new_status = "En cours"
    elif button_name == "stop":
      new_status = "Terminée"
    elif button_name == "pause":
      new_status = "À faire"

  try:
    update_status_todo(tache_id, new_status)
    message = "L'état de la tâche a été mis à jour"

  except Exception as err:
    message = "Vous devez sélectionner une tâche pour corriger l'état"
    error = True
  
  finally:
    info_label.config(text=message, fg="green" if not error else "red")
    fenetre.after(2000, clear_info_label)
    update_listbox()

# Effacer le champ d'information
def clear_info_label():
  info_label.config(text="", fg="black")

# Mettre à jour la liste des tâches après chaque changement
# Ne pas afficher le vrai tache_id de la base de données, car cela n'a aucune signification pour l'utilisateur
def update_listbox():
  tasks = get_all_tasks()
  tree.delete(*tree.get_children())

  for index, task in enumerate(reversed(tasks)):
      if option_var.get() == "Actives" and task['etat_nom'] == "Terminée":
        continue
      tree.insert("", tk.END, values=(index + 1, task['tache_libelle'], task['date_creation'], task['date_fixee'], task['date_realisation'], task['etat_nom'], task['tache_id']))
  
  tree.column("#0", width=0, stretch=tk.NO)
  tree.column("ID", width=40, anchor=tk.W)
  tree.column("Libellé", width=220, anchor=tk.CENTER)
  tree.column("Date de création", width=160, anchor=tk.CENTER)
  tree.column("Date fixée", width=160, anchor=tk.CENTER)
  tree.column("Date de réalisation", width=160, anchor=tk.CENTER)
  tree.column("État", width=80, anchor=tk.CENTER)

# Implémentation d'un placeholder
def on_entry_click(event):
  if entry.get() == 'Saisir une tâche':
    entry.delete(0, "end")
    entry.insert(0, '')

def on_entry_leave(event):
  if entry.get() == '':
    entry.insert(0, 'Saisir une tâche')

# Avant de fermer le programme principal, réinitialiser les données dans le fichier config.json
def on_closing():
  with open("config.json", "w") as file:
      file.write("")
  fenetre.destroy()

# Creation de la fenetre
fenetre = tk.Tk()
fenetre.geometry("900x700")
fenetre.title('PyDo. V:1.0')

# Ajout d'une icône
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('arbitrary string')
fenetre.iconbitmap('pydo.ico')

container_frame = tk.Frame(fenetre)
container_frame.pack(side="top", padx=10)

# Input pour la nouvelle tache
entry = ttk.Entry(container_frame, width=30)
entry.pack(side="left", padx=10, pady=10)
entry.insert(0, 'Saisir une tâche')

entry.bind("<Return>", on_submit_click)
entry.bind('<FocusIn>', on_entry_click) 
entry.bind('<FocusOut>', on_entry_leave)

label_between_entries = tk.Label(container_frame, text="faire avant le", font=("", 11))
label_between_entries.pack(side="left", padx=5, pady=10)

date_entry = DateEntry(
  container_frame, 
  width=12, 
  date_pattern="yyyy-mm-dd", 
  mindate=datetime.now() + timedelta(days=1), 
  locale="fr_FR", 
  state="readonly"
)
date_entry.set_date(datetime.now() + timedelta(days=7))
date_entry.pack(side="left", padx=10)

# Bouton pour envoyer la tache 
button_send = ttk.Button(container_frame, text="Créer une tâche", command=on_submit_click)
button_send.pack(side="left")

# Label pour info message
info_label = tk.Label(fenetre, text="", fg="black")
info_label.pack()

container_frame_update = tk.Frame(fenetre)
container_frame_update.pack(side="top", padx=10)

option_var = tk.StringVar(value="Actives")

actives_button = ttk.Radiobutton(container_frame_update, text="Actives", variable=option_var, value="Actives", command=update_listbox)
actives_button.pack(side=tk.LEFT, padx=5)

toutes_button = ttk.Radiobutton(container_frame_update, text="Toutes", variable=option_var, value="Toutes", command=update_listbox)
toutes_button.pack(side=tk.LEFT, padx=5)

image = Image.open("pydo-img.png")
photo = ImageTk.PhotoImage(image)
label_image = tk.Label(fenetre, image=photo)
label_image.pack(padx=10, pady=10)

# Boutons de contrôle de l'état des tâches
container_frame_buttons= tk.Frame(fenetre)
container_frame_buttons.pack(side="top", padx=10, pady=10)

text_play = '&#9658;'
start_button = ttk.Button(container_frame_buttons, text=html.unescape(text_play), command=lambda: on_update_status_click("start"), state=tk.DISABLED)
start_button.pack(side=tk.LEFT, pady=10)

text_pause = '&#9208;&#65039;'
pause_button = ttk.Button(container_frame_buttons, text=html.unescape(text_pause), command=lambda: on_update_status_click("pause"), state=tk.DISABLED)
pause_button.pack(side=tk.LEFT, pady=10)

text_stop = '&#9209;'
stop_button = ttk.Button(container_frame_buttons, text=html.unescape(text_stop), command=lambda: on_update_status_click("stop"), state=tk.DISABLED)
stop_button.pack(side=tk.LEFT, pady=10)

container_frame_modifications= tk.Frame(fenetre)
container_frame_modifications.pack(side="top", padx=10, pady=10)

# Bouton pour supprimer une tache 
delete_button = ttk.Button(container_frame_modifications, text="Supprimer", command=on_delete_click)
delete_button.pack(side=tk.LEFT, pady=2)

fenetre.bind("<Delete>", on_delete_click)

# Création d'un bouton de modification
edit_button = ttk.Button(container_frame_modifications, text="Modifier", command=on_edit_button_click)
edit_button.pack(side=tk.LEFT, pady=2)

# Treeview pour toutes nos taches
tree = ttk.Treeview(fenetre, columns=("ID", "Libellé", "Date de création", "Date fixée", "Date de réalisation", "État"))
tree.heading("ID", text="ID")
tree.heading("Libellé", text="Libellé")
tree.heading("Date de création", text="Date de création")
tree.heading("Date fixée", text="Date fixée")
tree.heading("Date de réalisation", text="Date de réalisation")
tree.heading("État", text="État")

tree.bind("<Double-1>", on_edit_button_click)
tree.bind("<<TreeviewSelect>>", on_treeview_select)

tree.pack(pady=10)

update_listbox()

# Bouton pour fermer la fenetre 
bouton = ttk.Button(fenetre, text="Fermer", command=on_closing)
bouton.pack()

# Le thème peut être défini sur 'dark'
sv_ttk.set_theme("light")

fenetre.protocol("WM_DELETE_WINDOW", on_closing)
fenetre.mainloop()