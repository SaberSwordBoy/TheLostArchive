import configparser
import json
import os
import smtplib
from datetime import datetime
from ipaddress import ip_address

from flask import Flask, redirect, render_template, request, send_file

config = configparser.ConfigParser()
config.read("/root/saberfilmsapp/config/config.ini")

HOST = config.get("Server", "ip")
PORT = config.get("Server", "port")
ACCESSLOG = config.get("Server", "logfile")
PASSWORDS = config.get("Server", "admin_password").split(",")

app = Flask(__name__)


def get_importance(file: str) -> int:
    with open("people/" + file, "r") as f:
        print(f"{file} - {json.loads(f.read())['importance']}")
        return json.loads(f.read())["importance"]


def sort_files(files):
    return files  # need to implement sorting here
    # return sorted(files, reverse=True)


def password_prompt(message):
    return f"""
                <form action="/admin" method='post'>
                  <label for="password">{message}:</label><br>
                  <input type="password" id="password" name="password" value=""><br>
                  <input type="submit" value="Submit">
                </form>"""


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/people")
def cast():
    people = []
    for _, _, files in os.walk("people"):

        for file in sort_files(files):
            with open("people/" + file, "r") as f:
                people.append(json.load(f))

    return render_template("people.html", people=people)


@app.route("/person/<name>")
def person(name):
    picture = False
    data = {"Name": "ERROR"}
    try:
        with open(f"people/{name}.json", "r") as f:
            data = json.load(f)
            if data.get("Picture") != "":
                picture = True
    except FileNotFoundError:
        data = {
            "Name": "ERROR",
            "About": "This Person does not exist.",
            "Roles": ["Error"],
        }
    return render_template("person.html", person=data, picture=picture)


@app.route("/bts")
def behind_the_scenes():
    images = []
    for _, _, files in os.walk("bts"):

        for file in sort_files(files):
            images.append(
                {"filename": file, "url": f"https://thelostarchive.cf/bts/{file}"}
            )

    return render_template("bts.html", images=images)


@app.route("/bts/<name>")
def btsdownloads(name):
    return send_file(f"/root/saberfilmsapp/bts/{name}")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/submit", methods=["GET", "POST"])
def submit_user():
    if request.method == "POST":
        data = request.form

        if data["password"] not in PASSWORDS:
            return "You do not have permission to do that!"

        str_json = json.dumps(data)
        data = json.loads(str_json)

        data["link"] = "".join(data["Name"].split(" ")).lower()
        data["socials"] = data["socials"].split(",")
        data["Roles"] = data["Roles"].split(",")
        data["password"] = ""

        if os.path.exists(f"people/{data['link']}.json"):
            return "That user already exists."

        with open(f"people/{data['link']}.json", "w+") as file:
            json.dump(data, file)

        return redirect("/people")

    if request.method == "GET":
        return render_template("add_user.html")


@app.route("/update", methods=["GET", "POST"])
@app.route("/update/<name>", methods=["GET", "POST"])
def update_user(name=None):
    if request.method == "POST":
        data = request.form

        if data["password"] not in PASSWORDS:
            return "You do not have permission to do that!"

        str_json = json.dumps(data)
        data = json.loads(str_json)

        data["link"] = "".join(data["Name"].split(" ")).lower()
        if data.get("socials") is not None:
            data["socials"] = data["socials"].split(",")
        data["Roles"] = data["Roles"].split(",")
        data["password"] = ""

        with open(f"people/{data['link']}.json", "w") as file:
            json.dump(data, file)

        return redirect("/people")

    if request.method == "GET":

        try:
            with open(f"people/{name}.json", "r") as f:
                data = json.load(f)
                if data.get("Picture") != "":
                    picture = True
        except FileNotFoundError:
            data = {
                "Name": "ERROR",
                "About": "This Person does not exist.",
                "Roles": ["Error"],
            }

        return render_template("edituser.html", person=data)


@app.route("/email", methods=["GET", "POST"])
def send_email():
    if request.method == "POST":
        data = json.loads(json.dumps(request.form))
        ip_address = request.remote_addr
        return "Error: not finished :( sorry"


@app.route("/getinvolved", methods=["GET", "POST"])
def get_involved():

    if request.method == "GET":
        return render_template("getinvolved.html")

    if request.method == "POST":
        pass


@app.route("/sponsors")
def sponsors():

    sponsors = []
    for _, _, files in os.walk("sponsors"):

        for file in sort_files(files):
            with open("sponsors/" + file, "r") as f:
                sponsors.append(json.load(f))

    return render_template("sponsors.html", sponsors=sponsors)


@app.route("/picture/<name>")
def get_picture(name):
    return send_file(
        f"/root/saberfilmsapp/static/images/{name}", attachment_filename="img.jpg"
    )


@app.route("/downloads/<name>")
def downloads(name):
    if "pdf" in name:
        return send_file(f"/root/saberfilmsapp/downloads/{name}")
    if "jpg" in name:
        return send_file(
            f"/root/saberfilmsapp/downloads/{name}", attachment_filename="TLA_Image.jpg"
        )
    if "ttf" in name:
        return send_file(f"/root/saberfilmsapp/downloads/{name}", as_attachment=False)

    return send_file(f"/root/saberfilmsapp/downloads/{name}", as_attachment=True)


@app.route("/plot")
def plot():
    return render_template("plot.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "GET":
        return password_prompt("Enter password for Admin page")
    if request.method == "POST":
        data = json.load(json.dumps(request.form))
        return data


@app.route("/urmom")
def urmom():
    return render_template(
        "person.html",
        data={
            "Name": "Your Mother",
            "About": "Its ur mom dont ask me",
            "Roles": ["Bitch", "Whore"],
            "Socials": [],
        },
    )


@app.route("/logs")
def logs():
    data = []

    lineNum = 0
    with open("/root/saberfilmsapp/logs/gunicorn.access.log", "r") as f:
        for line in f.readlines():
            lineNum += 1
            if not "uptimerobot" in line.lower():
                if lineNum > len(f.readlines()) / 2:
                    data.append(line)

    return "<br>".join(data)


@app.errorhandler(404)
def page_not_found_404(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error_500(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(
        host=HOST,
        port=PORT,
        ssl_context=(
            "/root/saberfilmsapp/certs/cert.pem",
            "/root/saberfilmsapp/certs/key.pem",
        ),
        debug=True,
    )
