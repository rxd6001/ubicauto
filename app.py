#-*- coding:utf-8 -*-
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

@app.route('/home')
def home():
    return render_template('/webtest/index1.html')


if __name__ == '__main__': 
    app.run(host="192.168.0.24", port=5001, debug=True)
