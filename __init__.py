from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/lecture')
def lecture():
    # Sécurité : Si pas admin, on vire
    if session.get('user_type') != 'admin':
        return redirect(url_for('authentification'))
    
    # SUCCÈS : On affiche le beau menu
    return render_template('admin_dashboard.html')

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        # Vérification Admin
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            session['user_type'] = 'admin'
            return redirect(url_for('lecture'))
        # Vérification User simple
        elif request.form['username'] == 'user' and request.form['password'] == '12345':
            session['user_type'] = 'user'
            return redirect(url_for('search_nom'))
        else:
            return render_template('formulaire_authentification.html', error=True)
    return render_template('formulaire_authentification.html', error=False)

# --- Routes Clients ---
@app.route('/enregistrer_client', methods=['GET', 'POST'])
def enregistrer_client():
    if request.method == 'GET':
        return render_template('formulaire.html')
    
    nom = request.form['nom']
    prenom = request.form['prenom']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)', (1002938, nom, prenom, "ICI"))
    conn.commit()
    conn.close()
    return redirect('/consultation/')

@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/fiche_nom/', methods=['GET', 'POST'])
def search_nom():
    if not session.get('user_type'):
        return redirect(url_for('authentification'))
    
    if request.method == 'POST':
        nom_recherche = request.form['nom']
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clients WHERE UPPER(nom) = UPPER(?)', (nom_recherche,))
        data = cursor.fetchall()
        conn.close()
        return render_template('read_data.html', data=data)

    return render_template('formulaire_recherche.html')

# --- Routes Livres (Admin) ---
@app.route('/admin_livres', methods=['GET', 'POST'])
def admin_livres():
    if session.get('user_type') != 'admin':
        return redirect(url_for('authentification'))
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        cursor.execute('INSERT INTO livres (titre, auteur, statut) VALUES (?, ?, 0)', (titre, auteur))
        conn.commit()
    cursor.execute('SELECT * FROM livres')
    livres = cursor.fetchall()
    conn.close()
    return render_template('admin_livres.html', livres=livres)

@app.route('/supprimer_livre/<int:id>')
def supprimer_livre(id):
    if session.get('user_type') != 'admin':
        return redirect(url_for('authentification'))
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM livres WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_livres'))

@app.route('/catalogue')
def catalogue():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres')
    livres = cursor.fetchall()
    conn.close()
    return render_template('catalogue.html', livres=livres)

@app.route('/emprunter/<int:id>')
def emprunter(id):
    if not session.get('user_type'):
        return redirect(url_for('authentification'))
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE livres SET statut = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('catalogue'))

@app.route('/rendre/<int:id>')
def rendre(id):
    if not session.get('user_type'):
        return redirect(url_for('authentification'))
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE livres SET statut = 0 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('catalogue'))

@app.route("/bonus/")
def bonus():
    return render_template("bonus.html")

if __name__ == "__main__":
    app.run(debug=True)
