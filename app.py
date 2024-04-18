from flask import *
from text import *
app = Flask(__name__)

@app.route('/')
def hello():
   return render_template('index.html')

@app.route('/generate',methods=['GET',"POST"])
def generate():
    ans=''
    if request.method=="POST":
        txt=request.form.get('txt')
        ans=generate_text(txt, 5, model, max_sequence_len)
    return render_template('index.html',k=ans)

if __name__ == '__main__':
   app.run(debug=True)