#!/bin/env python3

from flask import Flask, send_from_directory, redirect, request, url_for, render_template
from config import output, serial_port
from badge import readBadge
from classes import SQLiteOutput
from datetime import datetime
import sqlite3


app = Flask(__name__)
app.url_map.strict_slashes = False

sql = SQLiteOutput(output,"badge")

@app.route("/sqlite-viewer/<path:filename>")
def serve_sqlite_viewer(filename):
    return send_from_directory("sqlite-viewer", filename)

@app.route("/output/<path:filename>")
def serve_db(filename):
    return send_from_directory("output", filename)

@app.route("/badge")
def serve_badgeur():
    return render_template("badge.html", id_badge = readBadge(serial_port)) 

@app.route("/override")
def override():
    prenom = request.args.get("prenom")
    nom = request.args.get("nom")
    id_badge = request.args.get("id_badge")
    try:
        sql.update({"Id":id_badge},{"Prenom":prenom,"Nom":nom,"Date":datetime.now().isoformat()})
        return render_template("success.html",prenom = prenom,nom = nom,id_badge = id_badge)
    except sqlite3.IntegrityError as e:
        return render_template("fail.html",message = str(e))


@app.route("/add")
def update_table():
    prenom = request.args.get("prenom")
    nom = request.args.get("nom")
    id_badge = request.args.get("id_badge")
    try:
        max_uniqueid = sql.select_max_unique_id()[0]
        if max_uniqueid == None:
            max_uniqueid = 1
        print(max_uniqueid)
        sql.insert({"uniqueid":(max_uniqueid+1),"Prenom":prenom,"Nom":nom,"Id":id_badge,"Date":datetime.now().isoformat()})
        return render_template("success.html",prenom = prenom,nom = nom,id_badge = id_badge)
    except sqlite3.IntegrityError :
        old = sql.select({"Id":id_badge},{"Prenom","Nom"})
        return render_template("fail.html",
                                message = "Le badge n° " + id_badge + " est déjà dans la BDD, vérifier la BDD",
                                numero = id_badge,
                                ancien_nom = old["Nom"],
                                ancien_prenom = old["Prenom"],
                                nom = nom,
                                prenom = prenom)

@app.route("/")
def main():
    db_url = request.args.get("url")
    if not db_url:
        return redirect("/?url=" + request.url_root + output)
    return render_template("index.html")
   
if __name__ == "__main__":
    app.run(host="127.0.0.1") 
