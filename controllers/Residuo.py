from flask import render_template, request, redirect, flash, url_for
from flask_login import current_user
from models import Residuo
from utils import db
from flask import Blueprint

bp_residuo = Blueprint("residuo", __name__, template_folder='templates') 



@bp_residuo.route('/add', methods=['GET', 'POST'])
def add():
	if request.method=='GET':
		return render_template('residuo_add.html')

	if request.method=='POST':
		tipo_de_residuo = request.form.get('tipo')
		dispositivo = request.form.get('dispositivo')
		descricao = request.form.get('descricao')
		id_user = current_user.id_user
		print(tipo_de_residuo, dispositivo, descricao, id_user)
		residuo = Residuo(tipo_de_residuo, dispositivo, descricao, id_user)
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