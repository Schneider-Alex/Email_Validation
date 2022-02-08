from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import email


@app.route('/')
def homepage():
    return render_template('index.html',all_emails=email.Email.get_all())

@app.route('/saveemail', methods=['POST'])
def addemail():
    if not email.Email.validate_email(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    # ... do other things
    else:
        return redirect('/dashboard')
        data = {
            'email' : request.form['email']
        }
        email.Email.save(data)
    return redirect('/')