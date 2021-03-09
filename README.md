# Task for job application at Gideon Brothers

To start the app:
1. Clone/download repository
2. cd /path/to/repository
3. python3 -m venv venv
4. source venv/bin/activate
5. pip install -r requirements
6. Set up environment variables:
    
    export FLASK_APP=run.py
    
    export FLASK_ENV=development
    
    export DATABASE_URL=postrgres://<username>:<password>@localhost:5432/robot_management
    
    export SECRET_KEY=<some_secret_key>
    
7. Run create_db:
    chmod a+x ./create_db.sh
    ./create_db.sh
8. flask run
9. Open localhost:5000 in browser

To create admin user:
flask add-user <email> --admin

