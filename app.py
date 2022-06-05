from http.client import responses
from flask import Flask, render_template, redirect, flash, request, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

Responses = 'responses'


@app.route('/')
def show_survey():

    return render_template("survey_start.html", survey=survey)


@app.route('/start', methods=['POST'])
def start_survey():

    session[Responses] = []

    return redirect('/questions/0')


@app.route('/answer', methods=['POST'])
def handle_question():
    choice = request.form['answer']

    responses = session[Responses]
    responses.append(choice)
    session[Responses] = responses
    if (len(responses) == len(survey.questions)):
        return redirect('/finished')

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route('/questions/<int:id>')
def show_question(id):

    responses = session.get(Responses)

    if (responses is None):
        return redirect('/')

    if (len(responses) == len(survey.questions)):
        return redirect('/finished')

    if (len(responses) != id):
        flash(f"Question out of order: {id}")
        return redirect(f'/questions/{len(Responses)}')

    question = survey.questions[id]
    return render_template('questions.html', question_num=id, question=question)


@app.route('/finished')
def finished():
    return render_template("finished.html")
