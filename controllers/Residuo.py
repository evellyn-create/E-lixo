from datetime import datetime
from flask import render_template, request, redirect, flash, url_for
from flask_login import current_user
from models import Residuo, Horario
from utils import db
from flask import Blueprint

bp_residuo = Blueprint("residuo", __name__, template_folder='templates')


def horarios_disponiveis():
    return (Horario.query
            .filter(Horario.ativo == True, Horario.data_hora > datetime.now())
            .order_by(Horario.data_hora)
            .all())


@bp_residuo.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('residuo_add.html', horarios=horarios_disponiveis())

    tipo_de_residuo = request.form.get('tipo')
    dispositivo = request.form.get('dispositivo')
    descricao = request.form.get('descricao')
    id_horario = request.form.get('horario', type=int)
    id_user = current_user.id_user

    horario = Horario.query.get(id_horario) if id_horario else None
    if not horario or not horario.ativo or horario.data_hora <= datetime.now():
        flash('Horário inválido ou indisponível. Escolha outro.', 'error')
        return render_template('residuo_add.html', horarios=horarios_disponiveis())

    residuo = Residuo(tipo_de_residuo, dispositivo, descricao, id_user, id_horario)
    db.session.add(residuo)
    db.session.commit()

    flash("Resíduo adicionado com sucesso.", 'success')
    return redirect(url_for('residuo.get'))


@bp_residuo.route('/delete/<int:id>')
def delete(id):
    residuo = Residuo.query.get_or_404(id)
    db.session.delete(residuo)
    db.session.commit()
    flash('Resíduo deletado com sucesso', 'success')
    return redirect(url_for('.get'))


@bp_residuo.route('/get')
def get():
    if current_user.administrador:
        residuos = Residuo.query.all()
    else:
        residuos = Residuo.query.filter_by(id_user=current_user.id_user).all()
    return render_template('residuo_get.html', residuos=residuos)