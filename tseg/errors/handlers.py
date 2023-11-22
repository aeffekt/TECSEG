from flask import Blueprint, render_template, current_app, url_for, request, redirect
from tseg.users.utils import role_required, buscarLista
from tseg.models import ErrorLog

errors = Blueprint('errors', __name__) # 'name', __name variable__


@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500


@role_required("Admin")
@errors.route("/errors_log")
def errors_log():
    select_item = request.args.get('selectItem')
    if select_item:		
        return redirect(url_for('errors.error_log', error_log_id=select_item))
    registros = buscarLista(ErrorLog)
    orderBy = current_app.config['ORDER_HISTORIAS']	
    item_type="Error"
    return render_template('errors/all_errors.html', 
                           title="Log de errores", 
                           orderBy=orderBy,
                           item_type=item_type,
                           lista=registros)


@role_required("Admin")
@errors.route("/error_log-<int:error_log_id>")
def error_log(error_log_id):    
    error_log = ErrorLog.query.get_or_404(error_log_id)    
    return render_template('errors/error_log.html', 
                           title="Consulta Error", 
                           error = error_log)