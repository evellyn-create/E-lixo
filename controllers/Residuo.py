from flask import render_template, request, redirect, flash
from models import Residuo
from utils import db
from flask import Blueprint

bp_residuo = Blueprint("residuo", __name__, template_folder='templates') 

@bp_residuo.route('/recovery')
def recovery():
	residuo = Residuo.query.all()
	return render_template('residuo_recovery.html', residuo = residuo)

@bp_usuarios.route('/create', methods=['GET', 'POST'])
def create():
	if request.method=='GET':
		return render_template('usuario_create.html')

	if request.method=='POST':
		nome = request.form.get('nome')
		email = request.form.get('email')
		senha = request.form.get('senha')
		csenha = request.form.get('csenha')
		usuario = Usuario(nome, email, senha)
		db.session.add(usuario)
		db.session.commit()

		flash("Dados cadastrados com sucesso!")
		return redirect(url_for('.recovery'))
		