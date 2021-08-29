from yaplee import app

myapp = app()

@myapp.init
def Initial():
    myapp.config(debug=True, port=80)

@myapp.template('main.html', name='home')
def MainPage():
    return {'style': 'style.css'}

myapp.start()