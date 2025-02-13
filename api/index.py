from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from waitress import serve


app = Flask(__name__)
CORS(app)

# Arbre de décision sous forme de dictionnaire
decision_tree = {
    "Le patient est-il un enfant ?": {
        "oui": "L'enfant a-t-il déjà eu une maladie cardiaque, des palpitations ?"
,       "non": "L'adulte a-t-il perdu brièvement connaissance ?"
},     
    "Le patient a-t-il déjà eu une maladie cardiaque, des palpitations ?": {  
        "oui": "Nous allons faire le bilan cardiaque du patient d'ici 15 minutes. Très urgent"
,       "non": "A-t-il fait son malaise au repos ?"
},    
    "A-t-il fait son malaise au repos ?": {
        "oui": "Nous allons faire passer un examen clinique au patient d'ici une trentaine de minutes. Urgent"
,       "non": "Nous allons faire le bilan cardiaque du patient d'ici 15 minutes. Très urgent"
},  
    "Le patient a-t-il perdu brièvement connaissance ?": {
        "oui": "A-t-il perdu connaissance pendant plus de 5 minutes ?"
,       "non": "Le patient a fait une lipothymie. Il pourra être pris en charge d'ici 15 minutes. Très urgent"
},  
    "A-t-il perdu connaissance pendant plus de 5 minutes ?": {
        "oui": "Le patient est dans le coma. Il doit être pris en charge immédiatement. Réanimation"              
,       "non": "Le patient a fait une syncope. Il pourra être pris ne charge dans les 15 minutes qui suivent. Très urgent"
},         
}

@app.route("/")
def index():
    return send_file("templates/index.html")

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.json
    question = data.get("question")
    answer = data.get("answer")

    next_step = decision_tree.get(question, {}).get(answer, "Je n'ai pas compris.")
    
    return jsonify({"next_question": next_step})

def run():
    serve(app, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    run()