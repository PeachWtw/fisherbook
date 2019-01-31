from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user


from app.model.base import  db
from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from app.model.user import User
from app.web import web

__author__ = 'tovi'


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            # user = User(form.nickname.data,form.email.data,form.password.data)
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
            # db.session.commit()
            return  redirect(url_for('web.login'))

    return render_template('auth/register.html',form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('帐号不存在或者密码错误')
    return render_template('auth/login.html',form={'data':[]})


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method== 'POST' and form.validate():
        account_email = form.email.data
        user = User.query.filter_by(email=account_email).first_or_404()
        from app.libs.email import send_mail
        send_mail(form.email.data,'重置你的密码','email/reset_password.html',
                  user=user.nickname,token=user.generate_token())
        flash('一封邮件已发送到邮箱'+ account_email + '请注意查收！')
    return render_template('auth/forget_password_request.html',form=form)



@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        success = User.reset_password(form.password1.data,token)
        if success:
            flash('你的密码已更新，请使用新密码登录')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败')
    return render_template('auth/forget_password.html')


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
