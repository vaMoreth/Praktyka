import re
from docx import Document
from flask import Flask, send_file, request, render_template
import os
from datetime import datetime

app = Flask(__name__)

months = {
    1: "січня", 2: "лютого", 3: "березня", 4: "квітня",
    5: "травня", 6: "червня", 7: "липня", 8: "серпня",
    9: "вересня", 10: "жовтня", 11: "листопада", 12: "грудня"
}

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    doc_number = request.form['doc_number']
    issue_date = request.form['issue_date']
    course = request.form['course']
    name = request.form['name']
    days = request.form['days']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    template_path = 'static/InputFiles/file2.docx'
    document = Document(template_path)

    process_elements(document, doc_number, issue_date, course, name, days, start_date, end_date)

    output_path = os.path.join('uploads', f'Довідка_{name}_{doc_number}.docx')
    document.save(output_path)

    return send_file(output_path, as_attachment=True)


def process_elements(document, doc_number, issue_date, course, name, days, start_date, end_date):

    for paragraph in document.paragraphs:
        replace_placeholders(paragraph, doc_number, issue_date, course, name, days, start_date, end_date)


def replace_placeholders(paragraph, doc_number, issue_date, course, name, days, start_date, end_date):
    text = paragraph.text

    date_obj = datetime.strptime(issue_date, "%Y-%m-%d")
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

    formatted_date = f'від «{date_obj.day}» {months[date_obj.month]} {date_obj.year} року'
    formatted_start_date = f'з «{start_date_obj.day}» {months[start_date_obj.month]} {start_date_obj.year} року'
    formatted_end_date = f'по «{end_date_obj.day}» {months[end_date_obj.month]} {end_date_obj.year} року'

    text = re.sub(r'\{\{doc_number\}\}', doc_number, text)
    text = re.sub(r'\{\{issue_date\}\}', formatted_date, text)
    text = re.sub(r'\{\{course\}\}', course, text)
    text = re.sub(r'\{\{name\}\}', name, text)
    text = re.sub(r'\{\{days\}\}', str(days), text)
    text = re.sub(r'\{\{start_date\}\}', formatted_start_date, text)
    text = re.sub(r'\{\{end_date\}\}', formatted_end_date, text)
    paragraph.text = text


if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)








