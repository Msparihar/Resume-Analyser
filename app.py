from flask import Flask, redirect,url_for, request, render_template, jsonify
import os
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired

from PyPDF2 import PdfReader

import spacy

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app=Flask(__name__)

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

required_skills = [
    "Java",
    "C++",
    "Python",
    "C#",
    "PHP",
    "JavaScript",
    "HTML",
    "CSS",
    "SQL",
    "Agile",
    "Scrum",
    "Git",
    "Linux",
    "Docker",
    "Kubernetes",
    "CI/CD",
]

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods = ['GET', 'POST'])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        scores = score()
        return render_template("home.html", form=form, scores = scores)
    return render_template("home.html", form=form)

def score():
    reader = PdfReader("static\\files\\resume.pdf")
    number_of_pages = len(reader.pages)
    number_of_pages

    with open('static\\files\\resume.txt', 'w',encoding='utf-8') as text_file:
        for page in range(number_of_pages):
            text = reader.pages[page].extract_text()
            text_file.write(text)
            
    # load the English NLP model
    nlp = spacy.load("en_core_web_sm")

    # read the resume text from a file
    with open("static\\files\\resume.txt", "r",encoding="utf-8") as f:
        resume_text = f.read()

    # use the NER model to extract skills from the resume text
    doc = nlp(resume_text)
    skills = []
    for ent in doc.ents:
        skills.append(ent.text)


    skills = [skill for skill in skills if skill in required_skills]


    # Create a CountVectorizer object
    vectorizer = CountVectorizer()

    # Fit the vectorizer on the two sets of skills
    vectorizer.fit_transform(skills + required_skills)

    # Convert each set of skills to a vector of word counts
    technical_skills_vector = vectorizer.transform([', '.join(skills)])
    skills_vector = vectorizer.transform([', '.join(required_skills)])

    # Calculate the cosine similarity between the two vectors
    cosine_sim = cosine_similarity(technical_skills_vector, skills_vector)[0][0]

    # Convert the cosine similarity to a percentage
    similarity_percent = cosine_sim * 100

    print("The resume is {:.2f}% match for the Job".format(similarity_percent))
    
    os.remove("static\\files\\resume.pdf")
    os.remove("static\\files\\resume.txt")
            
    return "The resume is {:.2f}% match for the Job".format(similarity_percent)
    

@app.route("/hello", methods = ['GET', 'POST'])
def hello():
    return "Hello There!"

if __name__=="__main__":
    app.run(debug=True)
    
    