from flask import Blueprint, request, jsonify
# from backend.services.texto import generar_respuesta

bp = Blueprint('chat', __name__)

@bp.route("/chat", methods=["POST"])
def chat():
    prompt = request.json.get("prompt")
    # response = generar_respuesta(prompt)
    # return jsonify({"respuesta": response})
    return jsonify({"respuesta": "Funcionalidad pendiente de integrar"})
