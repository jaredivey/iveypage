import os, time
from flask import Flask, render_template, json, make_response, g, redirect, url_for

os.environ['TZ'] = 'EST'
time.tzset()

def import_json():
    f =  open("/home/ubuntu/iveypage/resume.json")
    jdat = f.read()
    json_data = json.loads(jdat)
    f.close()
    return json_data

def json2xml(json_obj, line_padding=""):
    rl = list()
    json_obj_type = type(json_obj)

    if json_obj_type is list:
        for sub_elem in json_obj:
            rl.append(json2xml(sub_elem, line_padding))

        return "\n".join(rl)

    if json_obj_type is dict:
        for tag in json_obj:
            sub_obj = json_obj[tag]
            rl.append("%s<%s>" % (line_padding, tag))
            rl.append(json2xml(sub_obj, "\t" + line_padding))
            rl.append("%s</%s>" % (line_padding, tag))
        return "\n".join(rl)

    return "%s%s" % (line_padding, json_obj)

app = Flask(__name__)

@app.before_request
def before_request():
    g.json_data = import_json()

@app.route('/')
def index():
    return render_template('index.html', indextype = "index", json = g.json_data, generated = time.strftime("%a, %d %b %Y %H:%M:%S EST"))

@app.route('/professional')
def professional():
    return render_template('index.html', indextype = "professional", json = g.json_data, generated = time.strftime("%a, %d %b %Y %H:%M:%S EST"))

@app.route('/publications')
def publications():
    return render_template('index.html', indextype = "publications", json = g.json_data, generated = time.strftime("%a, %d %b %Y %H:%M:%S EST"))

@app.route('/personal')
def personal():
    return render_template('index.html', indextype = "personal", json = g.json_data, filenames=[url_for('static',filename='img/sloane.jpg'), url_for('static',filename='img/knowles.jpg')], generated = time.strftime("%a, %d %b %Y %H:%M:%S EST"))

@app.route('/pdf')
def pdf():
    return redirect("https://www.overleaf.com/docs/sqmhhkkxczqt/pdf")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
