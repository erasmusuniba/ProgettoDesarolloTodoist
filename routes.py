#Importazione moduli necessari
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user, login_user, logout_user
from models import db,UserModel, Todo, Category,db, login_manager
from form import TaskForm, RegistrationForm, LoginForm
from werkzeug.urls import url_parse
from datetime import datetime
from models import db 
from flask import Flask, send_from_directory
from app import app

"""
Usiamo decoratori per definire percorsi URL nella nostra istanza dell'applicazione.
I percorsi URL possono includere variabili nelle loro definizioni consentendoci di personalizzare
 le nostre query per ottenere le informazioni esatte richieste.
 Per passare una variabile all'interno di una route si usa : <tipo:nome_variabile>.
 Per chiamare una funzione di route si usa la funzione : url_for('nome_funzione_route')

"""

#PERCORSO DI DEFAULT
@app.route('/')
def index():
  return redirect(url_for('login'))

#PERCORSO DI REGISTRAZIONE
@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Per prima cosa controlliamo se l'utente corrente è già autenticato.
    Per questo utilizziamo l'istanza current_userdi Flask-login .
    Il valore di current_user è l'oggetto restituito da user loader 
    """
    
    if current_user.is_authenticated:
        return redirect(url_for('tasks'))
    #Creazione del modulo register form
    form = RegistrationForm()
     #Successivamente controlliamo se i dati inviati nel modulo sono validi. 
    if form.validate_on_submit():
        #Creo l'oggetto User partendo dai dati memorizzati nell'html con "form.attributo"
        user = UserModel(username=form.username.data.lower(), email=form.email.data.lower())
        #Assegno la password all'utente
        user.set_password(form.password.data)

        #Permette di inserire una riga della tabella
        db.session.add(user)
        #permette di salvare la modifica sul database
        db.session.commit()
        flash('Congratulations, you are now a registered user!')

        #MODEL CORRISPONDE ALLA CLASSE DEL DATABASE
        #E' POSSIBILE OTTENERE TUTTE LE RIGHE CON  model.query.all ()
        

        #Reinderizzare con il link login
        return redirect(url_for('login'))

    #mostrare il template con i dati del form
    return render_template('register.html', title='Register', form=form)


#PERCORSO DI LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    nologin = False

    """
    Per prima cosa controlliamo se l'utente corrente è già autenticato.
    Per questo utilizziamo l'istanza current_userdi Flask-login .
    Il valore di current_user è l'oggetto restituito da user loader 
    """
    if current_user.is_authenticated:
        return redirect(url_for('tasks'))

    #Creazione del modulo login form
    form = LoginForm()
     #Successivamente controlliamo se i dati inviati nel modulo sono validi. 
    if form.validate_on_submit():
        
        # In tal caso, proviamo a recuperare l'utente dall'e-mail con query.filter_by sulla classe userModel
        user = UserModel.query.filter_by(email=form.email.data.lower()).first()
       
        #Controllo che l'oggetto utente non sia nullo e che la password corrisponda
        if user is None or not user.check_password(form.password.data):
            nologin = True
        else:
            # Se c'è un utente con quell'e-mail e la password corrisponde, procediamo all'autenticazione dell'utente chiamando il metodo login_user della classe Flask login.
            login_user(user, remember=form.remember_me.data)
            # Infine controlliamo se riceviamo il parametro next. Ciò accadrà quando l'utente ha tentato di accedere a una pagina protetta ma non è stato autenticato.
            # Per motivi di sicurezza, prenderemo in considerazione questo parametro solo se il percorso è relativo.
            # In questo modo evitiamo di reindirizzare l'utente verso un sito esterno al nostro dominio.
            #  Se il parametro successivo non viene ricevuto o non contiene un percorso relativo, reindirizziamo l'utente alla home page.
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('tasks')
            return redirect(next_page)

    #restituzione del template html
    return render_template('login.html', title='Sign In', form=form, message=nologin)


#PERCORSO DI LOGOUT
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
 
 #PERCORSO DI CREAZIONE DEL TASK
@app.route('/create-task', methods=['GET', 'POST'])
@login_required #new line
def tasks():

    #Acquisizione dell'oggetto user
    user = current_user
    
    #Filtrare tutti i gli oggetti todo dell'utente
    todo= Todo.query.filter_by(author=user) #new line
    print(todo)
    #Acquisizione della data corrente
    date= datetime.now()
    now= date.strftime("%Y-%m-%d")

    #Creazione del form relativo al task 
    form= TaskForm()
    form.category.choices =[(category.id, category.name) for category in Category.query.all()]

    #Gestione del tipo della richiesta
    if request.method == "POST":

        #Gestione del click sul tasto delete del item
        if request.form.get('taskDelete') is not None:
            
            #Filtrare l'item con l'id associato al bottone taskDelete come "value"
            todo_item = Todo.query.filter_by(id=request.form.get('taskDelete')).one()
            
            #Eliminare l'item filtrato
            db.session.delete(todo_item)

            #Applicazione della modifica al database
            db.session.commit()

            #Restituzione del template tasks
            return redirect(url_for('tasks'))

           
        elif request.form.get('taskModify') is not None:
            
            #Filtrare l'item con l'id associato al bottone taskModifycome "value"
            id =request.form.get('taskModify')
            
            #chiamata della route id
            return redirect(url_for('edit', id=id))

           


            #Gestione del click sul bottone aggiungi 
        elif form.validate_on_submit():
                #Ottenere la categoria inserita nel template
                selected= form.category.data


                #ottenere l'oggetto categoria
                category= Category.query.get(selected)

                #Creazione dell'oggetto Todo
                todo_item = Todo(title=form.title.data, date=form.date.data, time= form.time.data, category= category.name, author=user) #new line
                print("ciao" + str(todo_item))
                db.session.add(todo_item)
                db.session.commit()
                flash('Congratulations, you just added a new note')
                return redirect(url_for('tasks'))

    #Rendirizzamento al template task
    return render_template('task.html', title='Create Tasks', form=form, todo=todo, DateNow=now)


#PERCORSO DI MODIFICA DEL TASK 
@app.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required #new line
def edit(id):
    #Acquisizione dell'oggetto user
    user = current_user #new line
     #Filtrare tutti i gli oggetti todo dell'utente
    #Filtrare l'item con l'id associato al bottone taskDelete come "value"
    todo_item = Todo.query.filter_by(id=id).one()
    print(str(todo_item))
  
     #Creazione del form relativo al task 
    form1= TaskForm()
    form1.category.choices =[(category.id, category.name) for category in Category.query.all()]

    #Gestione del tipo della richiesta
    if request.method == "POST":
        print(request.form.get('taskModify'))
        if request.form.get('taskModify') is not None:
                print("ciao")
                #Ottenere la categoria inserita nel template
                selected= form1.category.data


                #ottenere l'oggetto categoria
                category= Category.query.get(selected)

                #Creazione dell'oggetto Todo
                todo_item_new = Todo(title=form1.title.data, date=form1.date.data, time= form1.time.data, category= category.name, user_id=user.id) #new line
                db.session.delete(todo_item)
                db.session.commit()
                print("ciao" + str(todo_item))
                #Aggiornamento del nuovo item

                print("ehi" + str(todo_item_new))
                #Applicare modifica al db 
               
                db.session.add(todo_item_new)
                db.session.commit()
                flash('Congratulations, you just added a new note')
                return redirect(url_for('tasks'))
    #Rendirizzamento al template task
    return render_template('modifica.html', title='Modify Tasks', form=form1, todo=todo_item)

"""Flask memorizza l' ID utente degli utenti che hanno effettuato l'accesso nella sessione
Gestione degli utenti autenticati
"""
#CARICAMENTO DELL'UTENTE
@login_manager.user_loader
def load_user(id):
    return UserModel.query.get(int(id))