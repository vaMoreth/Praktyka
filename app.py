from flask import Flask, request, send_file, render_template
import os
from docx import Document
from datetime import datetime

app = Flask(__name__)

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
    
    template_path = 'static/InputFiles/file.docx'
    document = Document(template_path)
    
    for paragraph in document.paragraphs:
        if '№ _____' in paragraph.text:
            paragraph.text = paragraph.text.replace('№ _____', f'№ {doc_number}')
        if 'від «____» ______________ 20___ року' in paragraph.text:
            formatted_issue_date = datetime.strptime(issue_date, '%Y-%m-%d').strftime('%d.%m.%Y')
            paragraph.text = paragraph.text.replace('від «____» ______________ 20___ року', f'від «{formatted_issue_date}» року')
        if '______ курсу' in paragraph.text:
            paragraph.text = paragraph.text.replace('______ курсу', f'{course} курсу')
        if '______________ (прізвище власне ім’я по батькові за наявності))' in paragraph.text:
            paragraph.text = paragraph.text.replace('______________ (прізвище власне ім’я по батькові за наявності))', f'{name}')
        if 'строком на ______ днів' in paragraph.text:
            paragraph.text = paragraph.text.replace('строком на ______ днів', f'строком на {days} днів')
        if 'з «____» _________________ 20___ року по «____» _________________ 20___ року' in paragraph.text:
            formatted_start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%d.%m.%Y')
            formatted_end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%d.%m.%Y')
            paragraph.text = paragraph.text.replace('з «____» _________________ 20___ року по «____» _________________ 20___ року', f'з «{formatted_start_date}» року по «{formatted_end_date}» року')
    
    output_path = os.path.join('uploads', f'call_{doc_number}.docx')
    document.save(output_path)
    
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
