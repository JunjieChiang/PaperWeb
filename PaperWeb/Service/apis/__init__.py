from flask_restplus import Api
from flask import Flask

app = Flask(__name__,
            template_folder=r"C:\Users\14124\Desktop\MyProject\PaperWeb\Service\templates",
            static_folder=r"C:\Users\14124\Desktop\MyProject\PaperWeb\Service\templates\static")


api = Api(
    app,
    version="0.0.1",
    title="papers apis",
    description="论文网站api",
    # authorizations={},       # 通常网站都需要认证
    ui=True,
)

from Service.apis.papers import *