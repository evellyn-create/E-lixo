from flask import render_template, request, redirect, flash
from models import Ponto_de_coleta
from utils import db
from flask import Blueprint

bp_pontos = Blueprint("pontos", __name__, template_folder='templates') 

@bp_pontos.route('/recovery')
def recovery():
	pontos = Ponto_de_coleta.query.all()
	return render_template('pontos_recovery.html', pontos = pontos)

#@bp_usuarios.route('/create', methods=['GET', 'POST'])
#def create():
	# if request.method=='GET':
	# 	return render_template('usuario_create.html')

	# if request.method=='POST':
	# 	nome = request.form.get('nome')
	# 	email = request.form.get('email')
	# 	senha = request.form.get('senha')
	# 	csenha = request.form.get('csenha')
	# 	usuario = Usuario(nome, email, senha)
	# 	db.session.add(ponto)
	# 	db.session.commit()

	
	return redirect(url_for('.recovery'))
		