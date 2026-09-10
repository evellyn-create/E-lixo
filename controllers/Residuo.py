from flask import render_template, request, redirect, flash, url_for
from models import Residuo
from utils import db
from flask import Blueprint

bp_residuo = Blueprint("residuo", __name__, template_folder='templates') 



@bp_residuo.route('/residuo_add', methods=['GET', 'POST'])
def create():
	if request.method=='GET':
		return render_template('residuo_add.html')

	if request.method=='POST':
		tipo_de_residuo = request.form.get('tipo')
		dispositivo = request.form.get('dispositivo')
		descricao = request.form.get('descricao')
		residuo = Residuo(tipo_de_residuo, dispositivo, descricao)
		db.session.add(residuo)
		db.session.commit()


		return redirect(url_for('residuo_get'))

@bp_residuo.route('/delete/<int:id>')
def delete(id):
	residuo = Residuo.query.get_or_404(id)
	db.session.delete(reisduo)
	db.session.commit()
	return redirect(url_for('.get'))
		