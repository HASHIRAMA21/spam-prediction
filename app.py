from flask import Flask , request,render_template
import pickle
from flask_cors import CORS
import os
filename1 = "spamModel.sav"
filename2="countVect.sav"
loadedCV=pickle.load( open(filename2, 'rb'))
loadMod=pickle.load(open(filename1, 'rb'))

app = Flask(__name__)
CORS(app)
def read_from_pickle(path):
    with open(path, 'rb') as fichier:
        return pickle.load(fichier)

@app.route('/api/spamdetector', methods=["GET", "POST"])
def mail_detector():
    mail = request.args.get('mail')
    mail_convert = loadedCV.transform([mail])
    p = loadMod.predict_proba(mail_convert.toarray().reshape(1, -1))[0]
    print("Le mail est un spam a", p[1], "%")
    print("Le mail est un ham a", p[0], "%")
  
    return "C'est un spam a "+str(p[1])+" %"


@app.route("/", methods=['GET', 'POST'])
def main_page():
    opts = {}
    if request.method == 'GET':
        return render_template('index.html', opts=opts)

if __name__ == '__main__':
    #app.run(port=5000, debug=True, host="127.0.0.1")
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port, debug=False, host="0.0.0.0")
   