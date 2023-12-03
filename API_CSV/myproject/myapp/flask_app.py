from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/receber_previsoes', methods=['POST'])
def receber_previsoes():
    try:
        dados = request.get_json()
        previsoes = dados['previsoes']

        # Faça o que for necessário com as previsões (por exemplo, atualize o banco de dados)
        print("Previsões recebidas:", previsoes)

        return jsonify({'status': 'success', 'message': 'Previsões recebidas com sucesso.'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
