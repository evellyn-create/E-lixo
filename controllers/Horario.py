from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import current_user
from models import Horario
from utils import db

bp_horario = Blueprint("horario", __name__, template_folder='templates')

FUSO_BR = ZoneInfo("America/Sao_Paulo")

def agora_br():
    return datetime.now(FUSO_BR)

@bp_horario.app_template_filter('br')
def formato_br(dt):
    if dt is None:
        return ''
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(FUSO_BR).strftime('%d/%m/%Y %H:%M')

def _para_br(dt):
    if dt.tzinfo is None:  # veio do banco sem fuso, assume UTC
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(FUSO_BR)

@bp_horario.app_template_filter('data_br')
def data_br(dt):
    return '' if dt is None else _para_br(dt).strftime('%d/%m/%Y')

@bp_horario.app_template_filter('hora_br')
def hora_br(dt):
    return '' if dt is None else _para_br(dt).strftime('%H:%M')

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

    data_hora = datetime.strptime(
        request.form.get('data_hora'), '%Y-%m-%dT%H:%M'
    ).replace(tzinfo=FUSO_BR).astimezone(timezone.utc)

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