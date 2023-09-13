from flask import jsonify
from sqlalchemy import func
from db import db, app
from models import State, Language
from data import get_languages, get_list_of_states
from flask_cors import CORS

def add_to_db():
    states = get_list_of_states()
    for state in states:
        languages = get_languages(state)
        if languages:
            existing_state = State.query.filter_by(name=state).first()
            if not existing_state:
                new_state = State(name=state)
                db.session.add(new_state)
                db.session.commit()
                print(f"Added {state} to database")

            for language in languages:
                existing_language = Language.query.filter_by(name=language).first()
                if not existing_language:
                    new_language = Language(name=language)
                    db.session.add(new_language)
                    existing_state = State.query.filter_by(name=state).first()
                    if existing_state:
                        existing_state.languages.append(new_language)
                else:
                    existing_state = State.query.filter_by(name=state).first()
                    if existing_state:
                        existing_state.languages.append(existing_language)

                db.session.commit()
                print(f"Added {language} to database")
        else:
            print(f"No languages found for {state}")

@app.get("/")
def hello():
    return jsonify({"message": "Hello, world"})

@app.get("/states/<state>/languages")
def get_languages_for_state(state):
    state = State.query.filter(func.lower(State.name) == func.lower(state)).first()
    if not state:
        return jsonify({"message": "State not found"})
    languages = state.languages
    return jsonify({"languages": [language.name for language in languages]})

@app.get("/states/like/<string>")
def get_states_like(string):
    states = State.query.filter(State.name.ilike(f"%{string}%")).all()
    return jsonify({"states": [{"name": state.name, "id": state.id} for state in states]})

if __name__ == '__main__':

#    with app.app_context():
#        db.drop_all()
#        db.create_all()
#        add_to_db()

    CORS(app)
    app.run(debug=True)

