from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 's3creT'  # chave secreta para sessões

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        limite_inferior = int(request.form['lower_limit'])
        limite_superior = int(request.form['upper_limit'])
        session['numero_secreto'] = random.randint(limite_inferior, limite_superior)
        session['tentativas'] = 0
        session['limite_inferior'] = limite_inferior
        session['limite_superior'] = limite_superior
        return redirect(url_for('jogar'))

    return render_template('index.html')

@app.route('/jogar', methods=['GET', 'POST'])
def jogar():
    if request.method == 'POST':
        palpite = int(request.form['guess'])
        session['tentativas'] += 1
        numero_secreto = session['numero_secreto']

        if palpite < numero_secreto:
            resultado = "Muito baixo! Tente novamente."
        elif palpite > numero_secreto:
            resultado = "Muito alto! Tente novamente."
        else:
            resultado = f"Parabéns! Você adivinhou o número {numero_secreto} em {session['tentativas']} tentativas."
            return redirect(url_for('index'))  # Reinicia o jogo

        return render_template('play.html', result=resultado)

    return render_template('play.html', result="")

if __name__ == '__main__':
    app.run(debug=True)
