from db import db

class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    languages = db.relationship('Language', secondary='state_language', lazy='subquery', back_populates='states')
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, name) -> None:
        super().__init__()
        self.name = name

    def __str__(self):
        return self.name
    
class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    states = db.relationship('State', secondary='state_language', lazy='subquery', back_populates='languages')
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, name) -> None:
        super().__init__()
        self.name = name

    def __str__(self):
        return self.name
