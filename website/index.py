from flask import Flask, render_template

from time import sleep
from random import uniform
from enum import Enum
import datetime
app=Flask(__name__) 


@app.route('/')
def home(): 
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    templateData = {
        'time' : date,
    }
    return render_template('home.html', **templateData)



@app.route('/about/')
def about():
    templateData = 0
    return render_template('about.html')
    
if __name__ =='__main__': 
    app.run(debug=True, host='0.0.0.0') 

