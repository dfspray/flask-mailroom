import os
import base64
from passlib.hash import pbkdf2_sha256

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donor, Donation 

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY').encode()

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/create', methods=['GET', 'POST'])
def create():

    if request.method == "POST":
        if request.form['name'] not in [donor.name for donor in Donor.select()]:
            return render_template('create.jinja2')
        try:
            donor_obj = Donor.get(Donor.name==(request.form['name']))
            donation = int(request.form['amount'])
            print(type(donor_obj))
            print(type(donation))
            new_Donation = Donation(donor=donor_obj, value=donation)
            new_Donation.save()
        except ValueError as val:
            print(val)
            return render_template('create.jinja2')
        return redirect(url_for('all'))
    else:
        return render_template('create.jinja2')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
