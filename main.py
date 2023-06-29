from dotenv import load_dotenv, find_dotenv  # Module pour charger les variables d'environnement depuis un fichier .env
import os  # Module pour interagir avec le système d'exploitation
import pprint  # Module pour afficher joliment les données
from pymongo import MongoClient  # Module pour se connecter à MongoDB
from urllib.parse import quote_plus  # Module pour encoder les caractères spéciaux dans l'URL
from tkinter import ttk  # Module pour les widgets Tkinter améliorés
from tkinter import *  # Module principal Tkinter
from tkinter import scrolledtext  # Module pour créer un widget ScrolledText

load_dotenv(find_dotenv())  # Chargement des variables d'environnement à partir du fichier .env

password = os.environ.get("MONGODB_PWD")  # Récupération du mot de passe MongoDB depuis les variables d'environnement
escaped_password = quote_plus(password)  # Encodage du mot de passe pour l'inclure dans l'URL de connexion

# Chaîne de connexion à MongoDB avec le nom d'utilisateur 'anselme' et le mot de passe encodé
connection_string = f"mongodb+srv://anselme:{escaped_password}@expressjs.exlqbgg.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(connection_string)  # Création d'une instance de client MongoDB

dbs = client.list_database_names()  # Récupération de la liste des noms de bases de données

book_db = client.Book  # Sélection de la base de données 'Book'
collection = book_db.Book  # Sélection de la collection 'Book' dans la base de données 'Book'

def add():
    # Récupération des valeurs du formulaire
    titre = entrlivre.get()
    auteur = entrautor.get()
    commentaire = entrcomment.get()

    # Création d'un document représentant un livre
    livre = {
        'titre': titre,
        'auteur': auteur,
        'commentaire': commentaire
    }

    # Insertion du document dans la collection
    collection.insert_one(livre)

    # Effacement des champs de saisie
    entrlivre.delete(0, END)
    entrautor.delete(0, END)
    entrcomment.delete(0, END)

    update_table()  # Mise à jour du tableau

def delete():
    selected_item = table.selection()  # Récupération de l'élément sélectionné dans le tableau
    if selected_item:
        item_values = table.item(selected_item)['values']
        titre = item_values[0]
        auteur = item_values[1]
        commentaire = item_values[2]
        livre = {
            'titre': titre,
            'auteur': auteur,
            'commentaire': commentaire
        }
        collection.delete_one(livre)  # Suppression du document correspondant à l'élément sélectionné dans la collection
        table.delete(selected_item)  # Suppression de l'élément sélectionné dans le tableau

def modify():
    selected_item = table.selection()  # Récupération de l'élément sélectionné dans le tableau
    if selected_item:
        item_values = table.item(selected_item)['values']
        titre = item_values[0]
        auteur = item_values[1]
        commentaire = item_values[2]
        livre = {
            'titre': titre,
            'auteur': auteur,
            'commentaire': commentaire
        }
        new_titre = entrlivre.get()
        new_auteur = entrautor.get()
        new_commentaire = entrcomment.get()
        new_livre = {
            'titre': new_titre,
            'auteur': new_auteur,
            'commentaire': new_commentaire
        }
        collection.update_one(livre, {'$set': new_livre})  # Mise à jour du document correspondant à l'élément sélectionné dans la collection
        entrlivre.delete(0, END)
        entrautor.delete(0, END)
        entrcomment.delete(0, END)
        table.item(selected_item, text='', values=(new_titre, new_auteur, new_commentaire))  # Mise à jour de l'élément sélectionné dans le tableau

def update_table():
    records = collection.find()  # Récupération de tous les documents dans la collection
    table.delete(*table.get_children())  # Effacement de tous les éléments actuels du tableau
    for record in records:
        titre = record['titre']
        auteur = record['auteur']
        commentaire = record['commentaire']
        table.insert('', 'end', values=(titre, auteur, commentaire))  # Insertion d'un nouvel élément dans le tableau

fenetre = Tk()
fenetre.title("GESTION DES LIVRES")
fenetre.geometry("1350x700+0+0")
fenetre.configure(background="#dfe2a8")

# Titre
lbtitre = Label(fenetre, bd=20, relief=RIDGE, text="GESTION DE LIVRES", font=("Arial", 30), bg="darkblue", fg="white")
lbtitre.pack(fill=X)

# Tableau
frame_table = Frame(fenetre, bg="#dfe2a8")
frame_table.pack(pady=20)

table = ttk.Treeview(frame_table, columns=(1, 2, 3), height=5, show="headings")
table.pack(side=LEFT, padx=20)

table.heading(1, text="Titre du livre")
table.heading(2, text="Nom de l'auteur")
table.heading(3, text="Commentaire")
table.column(1, width=200)
table.column(2, width=200)
table.column(3, width=600)

scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=table.yview)
scrollbar.pack(side=RIGHT, fill=Y)
table.configure(yscrollcommand=scrollbar.set)

# Création de la colonne de commentaire avec ScrolledText
table.column(3, width=600, stretch=YES)
table.column("#0", width=0)  # Masquer la première colonne

def view_comment():
    selected_item = table.focus()
    if selected_item:
        comment = table.item(selected_item)['values'][2]
        comment_window = Toplevel(fenetre)
        comment_window.title("Commentaire")
        comment_window.geometry("400x300")

        comment_text = scrolledtext.ScrolledText(comment_window, wrap=WORD, width=40, height=10, font=("Arial", 12))
        comment_text.insert(END, comment)
        comment_text.pack(expand=True, fill=BOTH)

# Formulaire
frame_form = Frame(fenetre, bg="#dfe2a8")
frame_form.pack(pady=20)

lblmatricule = Label(frame_form, text="Titre du livre", font=("Arial", 16), bg="#dfe2a8")
lblmatricule.grid(row=0, column=0, padx=10, pady=10)
entrlivre = Entry(frame_form, font=("Arial", 14))
entrlivre.grid(row=0, column=1, padx=10, pady=10)

lblautor = Label(frame_form, text="Nom de l'auteur", font=("Arial", 16), bg="#dfe2a8")
lblautor.grid(row=1, column=0, padx=10, pady=10)
entrautor = Entry(frame_form, font=("Arial", 14))
entrautor.grid(row=1, column=1, padx=10, pady=10)

lblcomment = Label(frame_form, text="Commentaire", font=("Arial", 16), bg="#dfe2a8")
lblcomment.grid(row=2, column=0, padx=10, pady=10)
entrcomment = Entry(frame_form, font=("Arial", 14))
entrcomment.grid(row=2, column=1, padx=10, pady=10)

# Boutons
frame_buttons = Frame(fenetre, bg="#dfe2a8")
frame_buttons.pack(pady=20)

btnadd = Button(frame_buttons, text="AJOUTER", font=("Arial", 16), bg="darkblue", fg="yellow", command=add)
btnadd.pack(side=LEFT, padx=10)

btndelete = Button(frame_buttons, text="SUPPRIMER", font=("Arial", 16), bg="darkblue", fg="yellow", command=delete)
btndelete.pack(side=LEFT, padx=10)

btnsave = Button(frame_buttons, text="MODIFIER", font=("Arial", 16), bg="darkblue", fg="yellow", command=modify)
btnsave.pack(side=LEFT, padx=10)

update_table()  # Initialisation du tableau

fenetre.mainloop()  # Boucle principale de l'interface graphique
