from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import random
import os

app = Flask(__name__)
CORS(app)

# DADOS DE ENVIO
EMAIL_REMETENTE = "ferreiramateuss000@gmail.com"
SENHA_APP = "yvsdhnqamzqkhmay"  # Senha de app do Gmail

# FUNÇÃO DE ENVIO DE E-MAIL
def enviar_email(email_destino, senha_gerada):
    corpo_email = f"""\
Assunto: Acesso à Plataforma 🌐

Olá! Obrigado pela sua compra 🛒

Aqui estão seus dados de acesso:

📧 E-mail: {email_destino}
🔐 Senha: {senha_gerada}
🌍 Plataforma: https://seudominio.com

Aproveite!
"""

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_REMETENTE, SENHA_APP)
            smtp.sendmail(EMAIL_REMETENTE, email_destino, corpo_email.encode("utf-8"))
        return True
    except Exception as erro:
        print("Erro ao enviar e-mail:", erro)
        return False

@app.route("/")
def home():
    return "🟢 API da Kiwify está rodando com sucesso!"

# ENDPOINT PARA WEBHOOK
@app.route("/webhook_kiwify", methods=["POST"])
def webhook_kiwify():
    dados = request.get_json()
    print("Recebido:", dados)

    try:
        status = dados["status"]
        email_cliente = dados["customer"]["email"]
    except Exception as e:
        return jsonify({"erro": "Dados inválidos no webhook"}), 400

    if status == "approved" and email_cliente:
        senha = str(random.randint(10000, 99999))
        sucesso = enviar_email(email_cliente, senha)
        if sucesso:
            return jsonify({"mensagem": "E-mail enviado com sucesso"}), 200
        else:
            return jsonify({"erro": "Falha ao enviar e-mail"}), 500
    else:
        return jsonify({"erro": "Status diferente de aprovado ou e-mail ausente"}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
