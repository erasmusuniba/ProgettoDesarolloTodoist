from flask_sqlalchemy import SQLAlchemy

#Modulo per generare hash della password
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import MetaData

"""
Flask login offre:
- Memorizza l'ID utente nella sessione e i meccanismi per il login e il logout .
- Limita l'accesso a determinate viste solo agli utenti autenticati.
- Gestisci la funzionalità Ricordami  per mantenere la sessione anche dopo che l'utente ha chiuso il browser.
- Proteggi l'accesso ai cookie di sessione di terze parti."""
from flask_login import UserMixin, LoginManager

#Problema importazione dell'app dal file app risolto con 
from flask import current_app
#Flask werkzeug ha funzioni integrate per affrontare questo problema.#Problema : non possiamo salvare le password degli utenti
"""
Flask-login utilizza l'autenticazione basata su cookie.
uando il cliente effettua il login tramite le sue credenziali, 
Flask crea una sessione contenente l' ID utente e quindi invia l' ID sessione all'utente tramite un cookie,
 utilizzando il quale può effettuare il login e il logout come e quando richiesto.
"""
#Creazione di un oggetto della classe LoginManager che chiameremo login_manager e collegarlo all'app
login_manager = LoginManager() #creare e inizializzare l'estensione Flask_login.
login_manager.login_view = 'login'

#Creazione dell'oggetto db e collegamento all' pp
db = SQLAlchemy()

#new line

#CLASSE UTENTE
#L'unico requisito dichiarato da Flask-login è che la classe utente deve implementare le seguenti proprietà e metodi:
# - is_authenticated: una proprietà che indica Truese l'utente è stato autenticato e Falsealtro
# - is_active: una proprietà che indica se l'account dell'utente è attivo ( True) o meno ( False). È tua decisione definire cosa significa che un account utente è attivo. Ad esempio, l'e-mail è stata verificata o non è stata eliminata da un amministratore. Per impostazione predefinita, gli utenti con account inattivi non possono eseguire l'autenticazione.
# - is_anonymous: una proprietà valida False per utenti reali e True per utenti anonimi.
# - get_id(): un metodo che restituisce a string( unicodenel caso di Python 2) con l' IDunivoca dell'utente. Se IDl'utente era into qualsiasi altro tipo, è tua responsabilità convertirlo in string.
#Flask-login ci rende disponibile la classe UserMixincon un'implementazione predefinita per tutte queste proprietà e metodi. 
# Dobbiamo solo ereditare da esso nella nostra stessa classe User.
class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'
 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String())
    todo = db.relationship('Todo', backref='author', lazy='dynamic')

 
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
     
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)



#CLASSE CATEGORY
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __repr__(self):
        return '<Category {}>'.format(self.name)


#CLASSE TODO
class Todo(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    date = db.Column(db.Date())
    time = db.Column(db.Time())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category= db.Column(db.String, db.ForeignKey('category.id'))

    def __str__ (self):
        return 'Titolo =' + self.title + 'data =' + str(self.date) + 'time =' + str(self.time) + 'user =' +  str(self.user_id) + 'categoria =' + self.category
    def __repr__(self):
        return '<ToDo {}>'.format(self.title)
