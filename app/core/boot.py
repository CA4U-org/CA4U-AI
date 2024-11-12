from core.config import env
import core.ctx
from db.db import DB
from datetime import datetime

def boot():  
    print("Application initiation start")
    environment = env()

    db = DB (
        host = environment["DB_HOST"],    
        username = environment["DB_USERNAME"],
        password = environment["DB_PASSWORD"],
        database = environment["DB_DATABASE"]
    )

    core.ctx.CTX = core.ctx.Container(env, db)
  

    
    print("Application initiation finished.")


boot()        