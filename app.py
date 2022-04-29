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
PASSWORDS = [config.get("Server", "admin_password")]

app = Flask(
    __name__
)  # CREATE THE FLASK APP VARIABLE =- =- =- =- =- =- =- =- =- =- =- =- =- =-


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
    with open(ACCESSLOG, "a") as f:
        f.write(
            f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} | {request.method}: {request.remote_addr} - Index\n"
        )
    return render_template("index.html")


@app.route("/about")
def about():
    with open(ACCESSLOG, "a") as f:
        f.write(
            f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} | {request.method}: {request.remote_addr} - About\n"
        )
    return render_template("about.html")


@app.route("/people")
def cast():
    with open(ACCESSLOG, "a") as f:
        f.write(
            f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} | {request.method}: {request.remote_addr} - People\n"
        )
    people = []
    for _, _, files in os.walk("people"):

        for file in sort_files(files):
            with open("people/" + file, "r") as f:
                people.append(json.load(f))

    return render_template("people.html", people=people)


@app.route("/person/<name>")
def person(name):
    with open(ACCESSLOG, "a") as f:
        f.write(
            f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} | {request.method}: {request.remote_addr} - Person/{name}\n"
        )
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
    with open(ACCESSLOG, "a") as f:
        f.write(
            f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} | {request.method}: {request.remote_addr} - Bts\n"
        )
    return render_template("bts.html")


@app.route("/contact")
def contact():
    with open(ACCESSLOG, "a") as f:
        f.write(
            f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} | {request.method}: {request.remote_addr} - Contact\n"
        )
    return render_template("contact.html")


@app.route("/submit", methods=["GET", "POST"])
def submit_user():
    with open(ACCESSLOG, "a") as f:
        f.write(
            f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} | {request.method}: {request.remote_addr} - Submit\n"
        )

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


@app.route("/email", methods=["GET", "POST"])
def send_email():
    if request.method == "POST":
        data = json.loads(json.dumps(request.form))
        ip_address = request.remote_addr
        return "Error: not finished :( sorry"


@app.route("/getinvolved", methods=["GET", "POST"])
def get_involved():
    with open(ACCESSLOG, "a") as f:
        f.write(
            f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} | {request.method}: {request.remote_addr} - Getinvolved\n"
        )

    if request.method == "GET":
        return render_template("getinvolved.html")

    if request.method == "POST":
        data = request.form

        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        # Authentication
        s.login("sabercodeboy@gmail.com", "saber-films")

        message = data

        # sending the mail
        s.sendmail("sabercodeboy@gmail.com", "sabercodeboy@gmail.com", message)

        # terminating the session
        s.quit()


@app.route("/sponsors")
def sponsors():
    with open(ACCESSLOG, "a") as f:
        f.write(
            f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} | {request.method}: {request.remote_addr} - Sponsors\n"
        )

    sponsors = []
    for _, _, files in os.walk("sponsors"):

        for file in sort_files(files):
            with open("sponsors/" + file, "r") as f:
                sponsors.append(json.load(f))

    return render_template("sponsors.html", sponsors=sponsors)


@app.route("/picture/<name>")
def get_picture(name):
    with open(ACCESSLOG, "a") as f:
        f.write(
            f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} | {request.method}: {request.remote_addr} - Picture/{name}\n"
        )
    return send_file(f"/root/saberfilmsapp/static/images/{name}",
                     attachment_filename="img.jpg")


@app.route("/downloads/<name>")
def downloads(name):
    with open(ACCESSLOG, "a") as f:
        f.write(
            f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} | {request.method}: {request.remote_addr} - Downloads/{name}\n"
        )
    if "pdf" in name:
        return send_file(f"/root/saberfilmsapp/downloads/{name}")
    elif "jpg" in name:
        return send_file(f"/root/saberfilmsapp/downloads/{name}",
                         attachment_filename="TLA_Image.jpg")
    return send_file(f"/root/saberfilmsapp/downloads/{name}",
                     as_attachment=True)


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "GET":
        return password_prompt("Enter password for Admin page")


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
