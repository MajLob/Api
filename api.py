from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Customer {self.id} - {self.name} {self.last_name}>'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        last_name = request.form['last_name']
        new_customer = Customer(name=name, last_name=last_name)

        try:
            db.session.add(new_customer)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding the new customer."

    else:
        customers = Customer.query.order_by(Customer.date_created).all()
        return render_template('index.html', customers=customers)


@app.route('/delete/<int:id>')
def delete(id):
    customer_to_delete = Customer.query.get_or_404(id)
    try:
        db.session.delete(customer_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting this customer'
    

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    customer = Customer.query.get_or_404(id)
    if request.method == 'POST':
        customer.name = request.form['name']
        customer.last_name = request.form['last_name']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating this customer'
        
    else:
        return render_template('update.html', customer=customer)

if __name__ == '__main__':
    app.run(debug=True)
