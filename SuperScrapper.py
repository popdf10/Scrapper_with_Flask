from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_file

app = Flask("SuperScrapper")

db = {}


@app.route('/')
def home():
    return render_template("potato.html")


@app.route('/report')
def report():
    word = request.args.get("word")
    if word:
        word = word.lower()
        existingDb = db.get(word)
        if existingDb:
            jobs = existingDb
        else:
            jobs = get_jobs(word)
            db[word] = jobs
    else:
        return redirect('/')
    return render_template("report.html", SearchingBy=word, resultsNumber=len(jobs), jobs=jobs)


@app.route('/export')
def export():
    try:
        word = request.args.get("word")
        print(word)
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        print(jobs)
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        return send_file("jobs.csv",
                         mimetype='text/csv',
                         attachment_filename=f"{word}.csv",
                         as_attachment=True)
    except:
        return redirect('/')


app.run(host="127.0.0.1")
