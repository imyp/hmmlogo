from flask import Flask, session, redirect, url_for, request, render_template
from hmmlogo import hmmlogo, get_fig

app = Flask("pfam")
app.config['SECRET_KEY'] = 'dev'

@app.route('/')
def index():
    return redirect(url_for('submit'))

@app.route('/submit', methods=('GET','POST'))
def submit():
    if request.method == 'POST':
        session['accession'] = request.form['accession']
        session['start'] = request.form['start']
        session['end'] = request.form['end']
        return redirect(url_for('result'))
    return render_template('submit.html')

@app.route('/result')
def result():
    pfam_ac = session['accession']
    start = session['start']
    end = session['end']
    if start=='':
        start = None
    else:
        start = int(start)
    if end=='':
        end = None
    else:
        end = int(end)
    fig = hmmlogo(pfam_ac, start=start, end=end)
    hmm = get_fig(fig, format='png')
    
    return render_template('result.html', hmm=hmm)
if __name__ == '__main__':
    app.run(debug=True)
