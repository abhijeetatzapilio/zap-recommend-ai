#configuration details

import os
from flask import Flask
from configobj import ConfigObj
from flask_pymongo import PyMongo

config=ConfigObj(os.getcwd()+"/config/config.ini")
mongodb=config["mongodb"]

app=Flask(__name__,template_folder=f"{os.getcwd()}/templates")
app.config['JSON_SORT_KEYS'] = False
app.config["MONGO_URI"]=f"mongodb://{mongodb['HOST']}:{mongodb['PORT']}/{mongodb['DB']}"

mongo=PyMongo(app)