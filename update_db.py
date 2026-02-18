import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Création de la table Taches selon le cahier des charges
# Champs requis : Titre, Description, Date d'échéance, État (Terminée ou non)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS taches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titre TEXT NOT NULL,
        description TEXT,
        date_echeance TEXT,
        complete BOOLEAN DEFAULT 0
    )
''')

print("Table 'taches' ajoutée avec succès à database.db !")

conn.commit()
conn.close()
