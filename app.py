from flask import Flask, render_template, redirect, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

Responses = []


@app.route('/')
def show_survey():
    return render_template("survey_start.html", survey=survey)


@app.route('/start')
def start_survey():
    return redirect('questions/0')


@app.route('/questions/<id>')
def show_question(id):
    if (Responses is None):
        return redirect('/')
    if (len(Responses) != id):
        flash(f"Question out of order: {id}")
        return redirect(f'/questions/{len(Responses)}')
    if (len(Responses) == len(survey.questions)):
        return redirect('/finished')
    question = survey.questions[id]
    return render_template('questions.html', question_num=id, question=question)


@app.route('/answer', methods=['POST'])
def handle_question():
    choice = request.form['answer']
    Responses.append(choice)
    if (len(Responses) == len(survey.questions)):
        return redirect('/finished')


@app.route('/finished')
def finished():
    return render_template("finished.html")
