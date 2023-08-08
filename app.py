from flask import Flask, render_template, request
import os
import ast
import jiggybase_utils as jbu

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'  # Folder to store uploaded PDFs
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Get company names an id
companies = jbu.collection_doc_names_id()
# Get question list
with open('questions.txt') as file:
    questions = [line.rstrip() for line in file]
# Get template file
with open('template.txt', 'r') as file:
    template = file.read()

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_company = ''
    selected_question = ''
    company_name = ''
    prompt = ''
    response = ''
    entered_question = ''

    if request.method == 'POST':
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
    app.run(debug=True)