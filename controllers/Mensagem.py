from flask import Blueprint, render_template, request, redirect, flash, url_for, abort
from flask_login import login_required, current_user
from models import Mensagem, MensagemLida
from utils import db

bp_mensagem = Blueprint("mensagem", __name__, template_folder='templates')


@bp_mensagem.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if not current_user.administrador:
        abort(403)

    if request.method == 'GET':
        return render_template('mensagem_add.html')

    titulo = request.form.get('titulo', '').strip()
    texto = request.form.get('texto', '').strip()
    if not titulo or not texto:
        flash('Preencha o título e a mensagem.', 'warning')
        return redirect(url_for('.add'))

    db.session.add(Mensagem(titulo, texto, current_user.id_user))
    db.session.commit()
    flash('Mensagem enviada com sucesso', 'success')
    return redirect(url_for('.get'))


@bp_mensagem.route('/get')
@login_required
def get():
    lista = Mensagem.query.order_by(Mensagem.data_envio.desc()).all()
    novas = set()

    if not current_user.administrador:
        lidas = {l.id_mensagem for l in
                MensagemLida.query.filter_by(id_user=current_user.id_user)}
        novas = {m.id_mensagem for m in lista if m.id_mensagem not in lidas}
        for id_mensagem in novas:
            db.session.add(MensagemLida(current_user.id_user, id_mensagem))
        db.session.commit()

    return render_template('mensagem_get.html', lista=lista, novas=novas)


@bp_mensagem.route('/delete/<int:id_mensagem>', methods=['POST'])
@login_required
def delete(id_mensagem):
    if not current_user.administrador:
        abort(403)
    MensagemLida.query.filter_by(id_mensagem=id_mensagem).delete()
    m = Mensagem.query.get_or_404(id_mensagem)
    db.session.delete(m)
    db.session.commit()
    flash('Mensagem excluída com sucesso', 'success')
    return redirect(url_for('.get'))