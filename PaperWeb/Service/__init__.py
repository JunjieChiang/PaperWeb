from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__,
            template_folder=r"C:\Users\14124\Desktop\MyProject\PaperWeb\Service\templates",
            static_folder=r"C:\Users\14124\Desktop\MyProject\PaperWeb\Service\templates\static")

bootstarp = Bootstrap(app)

from Service.apis import *
from Service.views import *