#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request, redirect, session
import json
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField, FileField
from wtforms.widgets import TextArea, TextInput
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
import random
import time
from database import BOOKS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e70lIUUoXRKlXc5VUBmiJ9Hdi'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static'

@app.route('/', methods=['POST', 'GET'])
def index():
    all_books = BOOKS.get_all()
    cnt = 0
    buffer = [[]]

    for i in all_books:
        cnt += 1;
        buffer[-1].append((i[0], i[1], i[2]))

        if cnt == 3:
            cnt = 0
            buffer.append([])

    return render_template('books.html', BOOKS = buffer)


print(BOOKS.get_all())

class AddBookForm(FlaskForm):
    booktitle = StringField('Название книги:', validators=[DataRequired()], widget=TextInput())
    author = StringField('Автор:', validators=[DataRequired()], widget=TextInput())
    content = TextAreaField('Содержание книги:', validators=[DataRequired()],widget=TextArea())
    image = FileField('Обложка:')
    submit = SubmitField('Отправить')

@app.route('/add_new_book', methods=['POST', 'GET'])
def add_new_book():
    form = AddBookForm()
    if form.validate_on_submit():
        booktitle = form.booktitle.data
        author = form.author.data
        content = form.content.data
        image = request.files['file']

        BOOKS.insert(booktitle, author, content)
        all = BOOKS.get_all()
        if(all):
            image.save('static/images/{}.jpg'.format(all[-1][0]))
        else:
            image.save('static/images/1.jpg')

        return redirect('/')
    return render_template('add_new_book.html', form=form)



@app.route('/book/<id>', methods=['POST', 'GET'])
def readbook(id):
    print(id)
    now_book = BOOKS.get(id)
    if not now_book:
       return redirect('/')
    print(now_book)
    return render_template('readbook.html', id=now_book[0], booktitle=now_book[1], author=now_book[2], text=now_book[3])


@app.route('/delete/<id>', methods=['POST', 'GET'])
def deletebook(id):
    print(id)
    now_book = BOOKS.get(id)
    if not now_book:
       return redirect('/')

    os.remove("static/images/{}.jpg".format(id))
    BOOKS.delete(id)
    return redirect('/')


DEBUG = True
if DEBUG:
    if __name__ == '__main__':
        app.run(port=8080, host='127.0.0.1')