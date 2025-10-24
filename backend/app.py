from flask import Flask

app = Flask(__name__)

# Importar y registrar blueprints aquí
# from routes.chat import bp as chat_bp
# app.register_blueprint(chat_bp)

if __name__ == "__main__":
    app.run(debug=True)
