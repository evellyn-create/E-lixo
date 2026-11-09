from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import current_user
from models import Horario
from utils import db

bp_horario = Blueprint("horario", __name__, template_folder='templates')


def somente_admin():
    if not current_user.is_authenticated or not current_user.administrador:
        abort(403)


@bp_horario.route('/get')
def get():
    somente_admin()
    horarios = Horario.query.order_by(Horario.data_hora).all()
    return render_template('horario_get.html', horarios=horarios)


@bp_horario.route('/add', methods=['GET', 'POST'])
def add():
    somente_admin()
    if request.method == 'GET':
        return render_template('horario_add.html')

    data_hora = datetime.strptime(request.form.get('data_hora'), '%Y-%m-%dT%H:%M')
    db.session.add(Horario(data_hora))
    db.session.commit()
    flash('Horário adicionado com sucesso.', 'success')
    return redirect(url_for('horario.get'))


@bp_horario.route('/delete/<int:id>')
def delete(id):
    somente_admin()
    horario = Horario.query.get_or_404(id)
    horario.ativo = False  # desativa em vez de apagar, para não quebrar resíduos já agendados
    db.session.commit()
    flash('Horário desativado com sucesso.', 'success')
    return redirect(url_for('horario.get'))