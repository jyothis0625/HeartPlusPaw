from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.secret_key = "Secret Key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/pekla_db'
app.config['SQLALCHEMY_TRACK_NOTIFICATION'] = False

db = SQLAlchemy(app)

from app.routes.web_temp import web
# import atexit
# from apscheduler.scheduler import Scheduler
app.register_blueprint(web)

# cron = Scheduler(daemon=True)
# Explicitly kick off the background thread
# cron.start()

# @cron.interval_schedule(hours=1)
# def job_function():
    # Do your work here


# Shutdown your cron thread if the web process is stopped
#  atexit.register(lambda: cron.shutdown(wait=False))

if __name__ == "__main__":
    app.run()
    
    
    
    
# from apscheduler.scheduler import Scheduler
# from flask import Flask

# app = Flask(__name__)

# cron = Scheduler(daemon=True)
# # Explicitly kick off the background thread
# cron.start()

# @cron.interval_schedule(hours=1)
# def job_function():
#     # Do your work here


# # Shutdown your cron thread if the web process is stopped
#   atexit.register(lambda: cron.shutdown(wait=False))

# if __name__ == '__main__':
#     app.run()   