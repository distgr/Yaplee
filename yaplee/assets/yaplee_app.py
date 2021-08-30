from yaplee import app

# Define yaplee app object here.
myapp = app()

# Config yaplee project initial here.
@myapp.init
def Initial():
    myapp.config(debug=True)

# Define yaplee templates here.

# Start yaplee project (if you want to debug).
myapp.start()