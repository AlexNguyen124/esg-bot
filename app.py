import os
import ast
import json
from flask import Flask, render_template, request, redirect, url_for
import jiggybase_utils as jbu

app = Flask(__name__)

# Load configuration from JSON file
with open('config.json', 'r') as json_file:
    config_data = json.load(json_file)
app.config.update(config_data)
secret_key = app.config['SECRET_KEY']
upload_folder = app.config['UPLOAD_FOLDER']

# Get company names as list
companies = jbu.collection_doc_names_id()
# Get question list
with open('questions.txt') as file:
    questions = [line.rstrip() for line in file]
# Get template file
with open('template.txt', 'r') as file:
    template = file.read()

@app.route('/')
def index():
    selected_company = ''
    selected_question = ''
    company_name = ''
    prompt = ''
    response = ''
    entered_question = ''
    return render_template('index.html',
                           companies=companies,
                           questions=questions,
                           selected_company=selected_company,
                           selected_question=selected_question,
                           company_name=company_name,
                           prompt=prompt,
                           response=response)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    global companies
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filepath = os.path.join(upload_folder, filename)
            jbu.upload_to_collection(filepath)
            companies.append(os.path.splitext(filename)[0])
    return redirect(url_for('index'))

@app.route('/process', methods=['GET', 'POST'])
def process():
    selected_company = request.form.get('company')
    selected_question = request.form.get('question')
    entered_question = request.form.get('text_input')
    qnumber = int(selected_question[:2])
    company_name = selected_company
    if entered_question == '':
        prompt_response = jbu.submit_prompt(template,company_name,qnumber)
    else:
        prompt_response = jbu.simple_prompt(entered_question,company_name)
    prompt = prompt_response[0]
    response = prompt_response[1]
    return render_template('index.html',
                           companies=companies,
                           questions=questions,
                           selected_company=selected_company,
                           selected_question=selected_question,
                           company_name=company_name,
                           prompt=prompt,
                           response=response)








if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])