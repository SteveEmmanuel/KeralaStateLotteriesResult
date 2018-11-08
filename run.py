from app import app, db, bcrypt, login_manager
import flask
from flask import render_template, request, url_for, redirect
from app import Lottery, User
from sqlalchemy import or_
from datetime import datetime
import flask_admin
from flask_admin.contrib.sqla import ModelView
from Forms import LotteryForm, LoginForm
from flask_login import login_user, logout_user, current_user

'''import logging
logging.basicConfig(
    filename="/home/steveisredatw/tasks.log",
    level=logging.DEBUG
)
logging.info("At the starting line")'''

class LotteryModelView(ModelView):
    form_base_class = LotteryForm

    def render(self, template, **kwargs):
        """
        using extra js in render method allow use
        url_for that itself requires an app context
        """
        self.extra_js = [url_for("static", filename="js/flask-admin.js")]
        self.extra_css = [url_for("static", filename="css/flask-admin.css")]

        return super(LotteryModelView, self).render(template, **kwargs)


    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = flask_admin.Admin(app, name='Admin')
admin.add_view(LotteryModelView(Lottery, db.session, name='Lotteries'))

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/result/<lottery_id>')
def result(lottery_id):
    query = db.session.query(Lottery).filter(Lottery.id.__eq__(lottery_id))
    if query.count() == 0:
        return render_template('404.html')
    return render_template('result_view.html', lottery=query.first())

@app.route('/page', methods = ['GET', 'POST'])
def paginate():
    search_value = request.form['search[value]']

    query = db.session.query(Lottery)
    total_count = query.count()

    if 'date' in request.form:
        if request.form['date'].__len__() != 0:
            date = datetime.strptime(request.form['date'], '%d/%m/%Y')
            query = query.filter(Lottery.date == date.date())

    if search_value.__len__() != 0:
        query = query.filter(or_(Lottery.name.contains(search_value),
                                Lottery.series.contains(search_value)))
    filtered_count = query.count()

    if request.form['order[0][column]'] == '0':
        order_column = Lottery.date
    if request.form['order[0][column]'] == '1':
        order_column = Lottery.name
    if request.form['order[0][column]'] == '2':
        order_column = Lottery.series

    if request.form['order[0][dir]'] == 'asc':
        order_column = order_column.asc()
    else:
        order_column = order_column.desc()

    query = query.order_by(order_column)

    length = int(request.form['length'])
    start = int(request.form['start'])
    query = query.paginate(page=(start/length)+1, per_page=length, error_out=False, max_per_page=None)
    #print request.form
    result_dict = []
    for q in query.items:
        result_dict.append([q.date.strftime('%a, %d/%m/%Y'), q.name, q.series, q.id])
    data = {'draw': int(request.form['draw']),
            'recordsTotal': total_count,
            'recordsFiltered': filtered_count,
            'data': result_dict}

    return flask.jsonify(data)

@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return db.session.query(User).filter(User.id.__eq__(user_id)).first()

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.user_id.__eq__(form.user_id.data))
        if user.count() == 1:
            user = user.first()
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("admin.index"))
    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def processing_error(error):
    return render_template('500.html', error=error), 500

if __name__ == '__main__':
    port = 8080
    app.run(host='0.0.0.0', port=port)
