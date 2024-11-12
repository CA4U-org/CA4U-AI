from core.config import env
import core.ctx
from db.db import DB
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from scheduler.scheduler_registry import SCHEDULER_REGISTRY

def boot():  
    print("Application initiation start")
    environment = env()

    print("Current Profile : ", environment["PROFILE"])

    db = None
    if environment["PROFILE"] == "production":
        db = DB (
            host = environment["DB_HOST"],    
            username = environment["DB_USERNAME"],
            password = environment["DB_PASSWORD"],  
            database = environment["DB_DATABASE"]
        )

    scheduler = BackgroundScheduler()

    for sc in SCHEDULER_REGISTRY:
        scheduler.add_job(sc[0], IntervalTrigger(seconds=sc[1]))

    core.ctx.CTX = core.ctx.Container(env, db, scheduler)
    print("Application initiation finished.")


boot()        