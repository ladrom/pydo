import mysql.connector
from datetime import datetime
from mysql.connector import errorcode
import json

# Connexion à la base de données en utilisant les données du fichier json
def database_connection():
  try:
    with open('config.json', 'r') as file:
      data = json.load(file)
      data_user = data["user"]
      data_password = data["password"]
      data_host = data["host"]
      data_database = data["database"]

    return mysql.connector.connect(
    user=data_user, 
    password=data_password,
    host=data_host,
    database=data_database
  )

  except FileNotFoundError:
    pass

def get_all_tasks():
  connection = database_connection()
  cursor = connection.cursor(dictionary=True)

  try:
    # Obtenir toutes les données de deux tables en utilisant la jointure interne
    cursor.execute("SELECT * FROM tache INNER JOIN etat ON etat.tache_id = tache.tache_id ORDER BY tache.tache_id DESC")
    tasks = cursor.fetchall()
    return tasks

  except mysql.connector.Error as err:
    print(f"Erreur MySQL: {err}")

  finally:
    cursor.close()
    connection.close()

def add_todo(new_todo, end_date):
  connection = database_connection()
  cursor = connection.cursor()
  try:
    tache_libelle = new_todo
    date_creation = datetime.now()
    date_fixee = end_date
    date_realisation = None

    # Enregistrer une nouvelle tâche dans la base de données
    insert_query = "INSERT INTO tache (tache_libelle, date_creation, date_fixee, date_realisation) VALUES (%s, %s, %s, %s)"
    values = (tache_libelle, date_creation, date_fixee, date_realisation)
    cursor.execute(insert_query, values)

    tache_id = cursor.lastrowid
    etat_query = "INSERT INTO etat (etat_nom, tache_id) VALUES (%s, %s)"
    etat_values = ("À faire", tache_id)
    cursor.execute(etat_query, etat_values)

    connection.commit()

  except errorcode:
      print(f"Erreur MySQL: {errorcode}")

  finally:
      cursor.close()
      connection.close()

def delete_todo(tache_id):
  connection = database_connection()
  cursor = connection.cursor()

  # Supprimer une tâche de deux tables en utilisant l'ID reçu
  try:
    delete_etat_query = "DELETE FROM etat WHERE tache_id = %s"
    cursor.execute(delete_etat_query, (tache_id,))

    delete_tache_query = "DELETE FROM tache WHERE tache_id = %s"
    cursor.execute(delete_tache_query, (tache_id,))

    connection.commit()

  except errorcode:
    print(f"Erreur MySQL: {errorcode}")

  finally:
    cursor.close()
    connection.close()

def update_status_todo(tache_id, new_status):
  connection = database_connection()
  cursor = connection.cursor()
  # Mettre à jour le statut de la tâche. si la tâche est terminée, ajoutez l'heure d'achèvement actuelle.
  try: 
    update_etat_query = "UPDATE etat SET etat_nom = %s WHERE tache_id = %s"
    cursor.execute(update_etat_query, (new_status, tache_id))

    if new_status == 'Terminée':
      date_realisation_query = "UPDATE tache SET date_realisation = %s WHERE tache_id = %s"
      cursor.execute(date_realisation_query, (datetime.now(), tache_id))
    else:
      date_realisation_query = "UPDATE tache SET date_realisation = %s WHERE tache_id = %s"
      cursor.execute(date_realisation_query, (None, tache_id))

    connection.commit()

  except errorcode:
    print(f"Erreur MySQL: {errorcode}")
  
  finally:
    cursor.close()
    connection.close()

def edit_todo(tache_id, new_label):
  connection = database_connection()
  cursor = connection.cursor()
  # Correction du libellé de la tâche
  try:
    update_libelle_query = "UPDATE tache SET tache_libelle = %s WHERE tache_id = %s"
    cursor.execute(update_libelle_query, (new_label, tache_id))

    connection.commit()

  except errorcode:
    print(f"Erreur MySQL: {errorcode}")
  
  finally:
    cursor.close()
    connection.close()
