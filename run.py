# run.py
from app import create_app, db
from flask_migrate import Migrate
from app.models import BrokenLink, SpamReport

app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'BrokenLink': BrokenLink, 'SpamReport': SpamReport}

if __name__ == '__main__':
    app.run()
