import os
import sys

# The file passes all the arguments it recieves to the managa.py file.
# ex. "python manage_shortcut.py runserver" runs the server, as the name would suggest
try :
    os.system("python stronka/manage.py " + ' '.join(sys.argv[1::]))
except :
    os.system("py stronka/manage.py " + ' '.join(sys.argv[1::]))
