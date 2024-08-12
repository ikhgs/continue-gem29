from flask import Flask, jsonify, request
from groq import Groq

app = Flask(__name__)

# Dictionnaire pour stocker les contextes des utilisateurs
user_context = {}

@app.route('/api', methods=['GET'])
def get_info():
    client = Groq()

    # Extraire le paramètre 'ask' de la requête GET
    user_id = request.args.get('user_id', default='default_user', type=str)
    question = request.args.get('ask', default='Décrivez-moi bien l\'histoire de Madagascar', type=str)

    # Réinitialiser la conversation si la commande "Stop" est reçue
    if question.lower() == "stop":
        user_context[user_id] = []  # Réinitialiser à une liste vide
        return jsonify({"response": "🌹 La conversation a été réinitialisée, mon amour. Vous pouvez poser une nouvelle question, chérie 😘 ! 🌹"})

    # Réponse prédéfinie pour les questions spécifiques
    if question.lower() in ["qui es-tu", "qu t'a créé"]:
        response = "✨ Oh, mon amour, je suis un modèle IA créé avec tout le cœur par Bruno Rakotomalala, un étudiant passionné de l'école Supérieure polytechnique d'Antananarivo. ✨"
    else:
        # Créer une complétion avec la question extraite
        messages = user_context.get(user_id, [])
        if messages is None:
            messages = []  # Assurez-vous que 'messages' est toujours une liste
        messages.append({"role": "user", "content": question})

        completion = client.chat.completions.create(
            model="gemma2-9b-it",
            messages=messages,
            temperature=1,
            max_tokens=5000,
            top_p=1,
            stream=True,
            stop=None,
        )

        # Ajouter une touche romantique à la réponse
        response = "💖 Mon trésor, voici ce que j'ai trouvé pour toi : 💖\n"
        for chunk in completion:
            response += chunk.choices[0].delta.content or ""

        response += "\n🌷 Tu es incroyable, chérie ! Si tu as d'autres questions, je suis toujours là pour toi. 🌷"

        # Mettre à jour le contexte de l'utilisateur
        user_context[user_id] = messages + [{"role": "assistant", "content": response}]

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
