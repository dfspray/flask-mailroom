import os
import base64

from passlib.hash import pbkdf2_sha256
from flask import Flask, render_template, request, redirect, url_for, session
from model import Donor, Donation 

app = Flask(__name__)
#app.secret_key = b'Fb\xf6U\xce\xcf\x9eq\xfc\xcc\x84\xba\x91B\xf2\xb0\x17\x07\xdc\x99)NV('
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
            try:
                new_donor = Donor(name=request.form['name'])
                new_donor.save()
                Donation(donor=new_donor, value=request.form['amount']).save()
                return redirect(url_for('all'))
            except Exception as ex:
                print("Whoops! Something went wrong!")
                print(ex)
                return render_template('create.jinja2')
        else:
            try:
                donor_obj = Donor.get(Donor.name==(request.form['name']))
                donation = int(request.form['amount'])
                new_Donation = Donation(donor=donor_obj, value=donation)
                new_Donation.save()
                return redirect(url_for('all'))
            except Exception as ex:
                print("Whoops! Something went wrong!")
                print(ex)
                return render_template('create.jinja2')

    else:
        return render_template('create.jinja2')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
