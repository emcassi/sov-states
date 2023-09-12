import data
from flask import jsonify
from db import db, app
from models import State
from data import get_list_of_states, get_official_languages


def add_states_to_db():
    states = get_list_of_states()
    
    if len(states) == 0:
        print("No states found")
        return False
    
    for state in states:
        db.session.add(State(name=state))
        db.session.commit()

@app.get("/")
def hello():
    return jsonify({"message": "Hello, world"})


if __name__ == '__main__':


    states = get_list_of_states()
    if len(states) == 0:
        print("No states found")
        exit()
    for state in states:
        print(get_official_languages(state))
        break
        

    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    #     add_states_to_db()

    app.run(debug=True)