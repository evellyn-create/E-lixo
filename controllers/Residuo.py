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
		return render_template('residuo_registro.html')

	if request.method=='POST':
		tipo_de_residuo = request.form.get('tipo_de_residuo')
		dispositivo = request.form.get('dispositivo')
		descricao = request.form.get('descricao')
		residuo = Residuo(tipo_de_residuo, dispositivo, descricao)
		db.session.add(residuo)
		db.session.commit()


		return redirect(url_for('.recovery'))
		