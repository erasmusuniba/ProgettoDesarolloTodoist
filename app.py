#Importazione moduli necessari
from models import db, login_manager
#Modulo per le migrazioni
from flask_migrate import Migrate
from flask import Flask

"""
Model - View - Controller
- MODEL, memorizza i dati che vengono recuperati in base ai comandi del controller
- VIEW, genera output per l'utente in base alle modifiche nel modello
Il controller agisce sia sul modello che sulla vista ; invia comandi al modello per aggiornarne lo stato e alla vista per modificare le informazioni presentate agli utenti"""

#Flask-Migrate è un'estensione basata su Alembic utilizzata per eseguire migrazioni di database quando si utilizza SQLAlchemy come ORM
#Questa estensione rileva le modifiche apportate ai nostri modelli (nuovi modelli, nuovi campi,...) e genera script con i quali possiamo facilmente effettuare aggiornamenti del database. 
#Comandi principali di Flask-Migrate:
# flask db init: Crea la cartella migrazione con file necessari. Viene eseguito una sola volta, all'inizio.
# flask db migrate: Genera i file di migrazione del database con le modifiche rilevate.
# flask db upgrade: esegue la migrazione del database.
"""
In breve, i passaggi per utilizzare Flask-Migrate sono:

1 : Crea i tuoi modelli iniziali.
2 : Crea il database
3 : eseguire il comando init.
4 : eseguire il comando migrate.
5 : Verificare il codice del file che contiene le istruzioni per la migrazione e verificare che tutto sia corretto.
6 : Eseguire il comando upgrade.
7 : Apporta modifiche ai tuoi modelli.
8 : Torna al PASSO 4.
"""



"""
Il codice per il controller può essere suddiviso in tre sezioni: 
-Inizializzazione
-Routing 
-Esecuzione.
"""


"""
1) Inizializzazione:
    -Creazione di un' istanza dell'app
    -Impostazione delle opzioni di configurazione
    -Collegamento del db all'istanza dell'app
    -Collegamento del login all'istanza dell' app
    -Migrazione del database
"""
#Creazione dell'oggetto app
app = Flask(__name__)

#Assegnazione della chiave privata all'app
# Poiché Flask-login utilizza la sessione per l'autenticazione, è necessario impostare la variabile 
# di configurazione SECRET_KEY.
app.secret_key = 'f9bf78b9a18ce6d46a0cd2b0b86df9da'


#SQLALCHEMY_DATABASE_URI: L'URI del database con cui specificare il database
#  con cui si desidera stabilire una connessione. 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
#SQLALCHEMY_TRACK_MODIFICATIONS: una configurazione per abilitare o disabilitare 
# il rilevamento delle modifiche degli oggetti.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_ECHO'] = True

#Collegamento del db all'app
db.init_app(app) 

#Istruzione per risolvere problema "NoRuntimeApplicationContext"
app.app_context().push()
#Collegamento del login  all'app
login_manager.init_app(app)

#migrazione del database
migrate = Migrate(app,db) 
# per creare/utilizzare il database menzionato nell'URI, eseguire il metodo db.create_all() la prima volta
#db.create_all()


"""
   2)Routing
   Flask ci richiede di definire percorsi URL per la nostra applicazione Web 
   in modo che sappia quali pagine visualizzare/renderizzare 
   quando gli utenti accedono a URL specifici.
"""


"""Ciascun percorso è associato a una funzione del controller(AZIONE DEL CONTROLLER)
Quando ci si immette un URL, l'applicazione tenta di trovare una route corrispondente :
- ESITO POSITIVO chiama l'azione del controller associata a quella route.
- ESITO NEGATIVO , fallisce.
All'interno dell'AZIONE DEL CONTROLLER VENGONO UTILIZZATI: 
- MODELLI per recuperare tutti i dati necessari da un database;
- VISTE per il rendering delle pagine html richieste con i dati ricevuti dai modelli.
  I dati recuperati tramite i modelli vengono generalmente aggiunti a una struttura di dati (come un elenco o un dizionario) 
    e tale struttura è ciò che viene inviato alla vista.
"""
import routes