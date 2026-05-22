from datetime import date
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Grado, Gestion, Materia, Profesor, Curso, Alumno, Inscrito, Asignado, Nota, Pago, Costo
from app.decorators import permission_required

# ── GRADO ─────────────────────────────────────────────────
grado_bp = Blueprint('grado', __name__, url_prefix='/grado')

@grado_bp.route('/')
@login_required
@permission_required('grado_ver')
def index():
    lista = Grado.query.join(Gestion).order_by(Gestion.gestion.desc(), Grado.nivel, Grado.grado).all()
    return render_template('grado/index.html', grados=lista)

@grado_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@permission_required('grado_crear')
def nuevo():
    gestiones = Gestion.query.order_by(Gestion.gestion.desc()).all()
    if request.method == 'POST':
        g = Grado(
            grado=request.form['grado'], nivel=request.form['nivel'],
            ges_id=int(request.form['ges_id']),
            creado=date.today(), act=date.today(), usu_id=current_user.id
        )
        db.session.add(g); db.session.commit()
        flash('Grado creado.', 'success')
        return redirect(url_for('grado.index'))
    return render_template('grado/form.html', grado=None, gestiones=gestiones)

@grado_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@permission_required('grado_editar')
def editar(id):
    g = Grado.query.get_or_404(id)
    gestiones = Gestion.query.order_by(Gestion.gestion.desc()).all()
    if request.method == 'POST':
        g.grado = request.form['grado']; g.nivel = request.form['nivel']
        g.ges_id = int(request.form['ges_id']); g.act = date.today()
        db.session.commit(); flash('Grado actualizado.', 'success')
        return redirect(url_for('grado.index'))
    return render_template('grado/form.html', grado=g, gestiones=gestiones)

@grado_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@permission_required('grado_borrar')
def eliminar(id):
    g = Grado.query.get_or_404(id)
    try:
        db.session.delete(g); db.session.commit()
        flash('Grado eliminado.', 'success')
    except Exception:
        db.session.rollback(); flash('No se puede eliminar: tiene registros relacionados.', 'danger')
    return redirect(url_for('grado.index'))


# ── MATERIA ───────────────────────────────────────────────
materia_bp = Blueprint('materia', __name__, url_prefix='/materia')

@materia_bp.route('/')
@login_required
@permission_required('materia_ver')
def index():
    lista = Materia.query.join(Grado).order_by(Grado.grado, Materia.materia).all()
    return render_template('materia/index.html', materias=lista)

@materia_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
@permission_required('materia_crear')
def nueva():
    grados = Grado.query.order_by(Grado.grado).all()
    if request.method == 'POST':
        m = Materia(
            materia=request.form['materia'], gra_id=int(request.form['gra_id']),
            creado=date.today(), act=date.today(), usu_id=current_user.id
        )
        db.session.add(m); db.session.commit()
        flash('Materia creada.', 'success')
        return redirect(url_for('materia.index'))
    return render_template('materia/form.html', materia=None, grados=grados)

@materia_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@permission_required('materia_editar')
def editar(id):
    m = Materia.query.get_or_404(id)
    grados = Grado.query.order_by(Grado.grado).all()
    if request.method == 'POST':
        m.materia = request.form['materia']; m.gra_id = int(request.form['gra_id'])
        m.act = date.today(); db.session.commit()
        flash('Materia actualizada.', 'success')
        return redirect(url_for('materia.index'))
    return render_template('materia/form.html', materia=m, grados=grados)

@materia_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@permission_required('materia_borrar')
def eliminar(id):
    m = Materia.query.get_or_404(id)
    try:
        db.session.delete(m); db.session.commit(); flash('Materia eliminada.', 'success')
    except Exception:
        db.session.rollback(); flash('No se puede eliminar: tiene registros relacionados.', 'danger')
    return redirect(url_for('materia.index'))


# ── PROFESOR ──────────────────────────────────────────────
profesor_bp = Blueprint('profesor', __name__, url_prefix='/profesor')

@profesor_bp.route('/')
@login_required
@permission_required('profesor_ver')
def index():
    lista = Profesor.query.order_by(Profesor.paterno, Profesor.nombre).all()
    return render_template('profesor/index.html', profesores=lista)

@profesor_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@permission_required('profesor_crear')
def nuevo():
    if request.method == 'POST':
        p = Profesor(
            nombre=request.form['nombre'], paterno=request.form.get('paterno'),
            materno=request.form.get('materno'),
            masculino=request.form.get('genero') == 'M',
            ci=request.form.get('ci') or None,
            formacion=request.form.get('formacion'),
            email=request.form.get('email'),
            activo='activo' in request.form,
            creado=date.today(), act=date.today(), usu_id=current_user.id
        )
        db.session.add(p); db.session.commit()
        flash('Profesor registrado.', 'success')
        return redirect(url_for('profesor.index'))
    return render_template('profesor/form.html', profesor=None)

@profesor_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@permission_required('profesor_editar')
def editar(id):
    p = Profesor.query.get_or_404(id)
    if request.method == 'POST':
        p.nombre = request.form['nombre']; p.paterno = request.form.get('paterno')
        p.materno = request.form.get('materno')
        p.masculino = request.form.get('genero') == 'M'
        p.ci = request.form.get('ci') or None
        p.formacion = request.form.get('formacion'); p.email = request.form.get('email')
        p.activo = 'activo' in request.form; p.act = date.today()
        db.session.commit(); flash('Profesor actualizado.', 'success')
        return redirect(url_for('profesor.index'))
    return render_template('profesor/form.html', profesor=p)

@profesor_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@permission_required('profesor_borrar')
def eliminar(id):
    p = Profesor.query.get_or_404(id)
    try:
        db.session.delete(p); db.session.commit(); flash('Profesor eliminado.', 'success')
    except Exception:
        db.session.rollback(); flash('No se puede eliminar: tiene asignaciones.', 'danger')
    return redirect(url_for('profesor.index'))


# ── CURSO ─────────────────────────────────────────────────
curso_bp = Blueprint('curso', __name__, url_prefix='/curso')

@curso_bp.route('/')
@login_required
@permission_required('curso_ver')
def index():
    lista = Curso.query.join(Grado).order_by(Curso.gestion.desc(), Grado.grado, Curso.paralelo).all()
    return render_template('curso/index.html', cursos=lista)

@curso_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@permission_required('curso_crear')
def nuevo():
    grados = Grado.query.order_by(Grado.grado).all()
    if request.method == 'POST':
        c = Curso(
            curso=request.form.get('curso'), paralelo=request.form['paralelo'],
            gra_id=int(request.form['gra_id']), aula=request.form.get('aula'),
            capacidad=request.form.get('capacidad') or None,
            gestion=int(request.form['gestion']),
            creado=date.today(), act=date.today(), usu_id=current_user.id
        )
        db.session.add(c); db.session.commit()
        flash('Curso creado.', 'success')
        return redirect(url_for('curso.index'))
    return render_template('curso/form.html', curso=None, grados=grados)

@curso_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@permission_required('curso_editar')
def editar(id):
    c = Curso.query.get_or_404(id)
    grados = Grado.query.order_by(Grado.grado).all()
    if request.method == 'POST':
        c.curso = request.form.get('curso'); c.paralelo = request.form['paralelo']
        c.gra_id = int(request.form['gra_id']); c.aula = request.form.get('aula')
        c.capacidad = request.form.get('capacidad') or None
        c.gestion = int(request.form['gestion']); c.act = date.today()
        db.session.commit(); flash('Curso actualizado.', 'success')
        return redirect(url_for('curso.index'))
    return render_template('curso/form.html', curso=c, grados=grados)

@curso_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@permission_required('curso_borrar')
def eliminar(id):
    c = Curso.query.get_or_404(id)
    try:
        db.session.delete(c); db.session.commit(); flash('Curso eliminado.', 'success')
    except Exception:
        db.session.rollback(); flash('No se puede eliminar: tiene registros relacionados.', 'danger')
    return redirect(url_for('curso.index'))


# ── ALUMNO ────────────────────────────────────────────────
alumno_bp = Blueprint('alumno', __name__, url_prefix='/alumno')

@alumno_bp.route('/')
@login_required
@permission_required('alumno_ver')
def index():
    q = request.args.get('q', '')
    query = Alumno.query
    if q:
        query = query.filter(
            db.or_(Alumno.nombre.ilike(f'%{q}%'),
                   Alumno.paterno.ilike(f'%{q}%'),
                   Alumno.materno.ilike(f'%{q}%'))
        )
    lista = query.order_by(Alumno.paterno, Alumno.nombre).all()
    return render_template('alumno/index.html', alumnos=lista, q=q)

@alumno_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@permission_required('alumno_crear')
def nuevo():
    if request.method == 'POST':
        a = Alumno(
            nombre=request.form['nombre'], paterno=request.form.get('paterno'),
            materno=request.form.get('materno'),
            nacimiento=date.fromisoformat(request.form['nacimiento']) if request.form.get('nacimiento') else None,
            masculino=request.form.get('genero') == 'M',
            ci=request.form.get('ci') or None,
            direccion=request.form.get('direccion'), email=request.form.get('email'),
            activo='activo' in request.form, obs=request.form.get('obs'),
            creado=date.today(), act=date.today(), usu_id=current_user.id
        )
        db.session.add(a); db.session.commit()
        flash('Alumno registrado.', 'success')
        return redirect(url_for('alumno.index'))
    return render_template('alumno/form.html', alumno=None)

@alumno_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@permission_required('alumno_editar')
def editar(id):
    a = Alumno.query.get_or_404(id)
    if request.method == 'POST':
        a.nombre = request.form['nombre']; a.paterno = request.form.get('paterno')
        a.materno = request.form.get('materno')
        a.nacimiento = date.fromisoformat(request.form['nacimiento']) if request.form.get('nacimiento') else None
        a.masculino = request.form.get('genero') == 'M'
        a.ci = request.form.get('ci') or None
        a.direccion = request.form.get('direccion'); a.email = request.form.get('email')
        a.activo = 'activo' in request.form; a.obs = request.form.get('obs')
        a.act = date.today(); db.session.commit()
        flash('Alumno actualizado.', 'success')
        return redirect(url_for('alumno.index'))
    return render_template('alumno/form.html', alumno=a)

@alumno_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@permission_required('alumno_borrar')
def eliminar(id):
    a = Alumno.query.get_or_404(id)
    try:
        db.session.delete(a); db.session.commit(); flash('Alumno eliminado.', 'success')
    except Exception:
        db.session.rollback(); flash('No se puede eliminar: tiene registros relacionados.', 'danger')
    return redirect(url_for('alumno.index'))


# ── INSCRITO ──────────────────────────────────────────────
inscrito_bp = Blueprint('inscrito', __name__, url_prefix='/inscrito')

@inscrito_bp.route('/')
@login_required
@permission_required('inscrito_ver')
def index():
    lista = Inscrito.query.join(Alumno).join(Curso).order_by(Alumno.paterno, Alumno.nombre).all()
    return render_template('inscrito/index.html', inscritos=lista)

@inscrito_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@permission_required('inscrito_crear')
def nuevo():
    alumnos = Alumno.query.filter_by(activo=True).order_by(Alumno.paterno).all()
    cursos  = Curso.query.order_by(Curso.gestion.desc(), Curso.paralelo).all()
    if request.method == 'POST':
        ins = Inscrito(
            alu_id=int(request.form['alu_id']), cur_id=int(request.form['cur_id']),
            reserva='reserva' in request.form, inscrito='inscrito' in request.form,
            descuento=int(request.form.get('descuento', 0)),
            motivo_descuento=request.form.get('motivo_descuento'),
            obs=request.form.get('obs'),
            creado=date.today(), act=date.today(), usu_id=current_user.id
        )
        db.session.add(ins); db.session.flush()
        # Generar plan de pagos automáticamente
        costo = Costo.query.filter_by(cur_id=ins.cur_id).first()
        if costo:
            for i in range(1, costo.nro_cuota + 1):
                monto = float(costo.cuota) * (1 - ins.descuento / 100)
                p = Pago(ins_id=ins.id, nro_cuota=i, cuota=round(monto, 2),
                         pagado=False, creado=date.today(), act=date.today(), usu_id=current_user.id)
                db.session.add(p)
        db.session.commit()
        flash('Inscripción realizada. Plan de pagos generado.', 'success')
        return redirect(url_for('inscrito.index'))
    return render_template('inscrito/form.html', inscrito=None, alumnos=alumnos, cursos=cursos)

@inscrito_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@permission_required('inscrito_editar')
def editar(id):
    ins = Inscrito.query.get_or_404(id)
    alumnos = Alumno.query.filter_by(activo=True).order_by(Alumno.paterno).all()
    cursos  = Curso.query.order_by(Curso.gestion.desc(), Curso.paralelo).all()
    if request.method == 'POST':
        ins.cur_id = int(request.form['cur_id'])
        ins.reserva = 'reserva' in request.form
        ins.inscrito = 'inscrito' in request.form
        ins.descuento = int(request.form.get('descuento', 0))
        ins.motivo_descuento = request.form.get('motivo_descuento')
        ins.abandono = 'abandono' in request.form
        ins.obs = request.form.get('obs'); ins.act = date.today()
        db.session.commit(); flash('Inscripción actualizada.', 'success')
        return redirect(url_for('inscrito.index'))
    return render_template('inscrito/form.html', inscrito=ins, alumnos=alumnos, cursos=cursos)


# ── NOTA ──────────────────────────────────────────────────
nota_bp = Blueprint('nota', __name__, url_prefix='/nota')

@nota_bp.route('/')
@login_required
@permission_required('nota_ver')
def index():
    cur_id = request.args.get('cur_id', type=int)
    cursos = Curso.query.order_by(Curso.gestion.desc(), Curso.paralelo).all()
    notas  = []
    if cur_id:
        notas = (Nota.query
                 .join(Inscrito).filter(Inscrito.cur_id == cur_id)
                 .join(Materia).join(Alumno, Inscrito.alu_id == Alumno.id)
                 .order_by(Alumno.paterno, Materia.materia).all())
    return render_template('nota/index.html', notas=notas, cursos=cursos, cur_id=cur_id)

@nota_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
@permission_required('nota_crear')
def nueva():
    inscritos = Inscrito.query.filter_by(inscrito=True).all()
    materias  = Materia.query.all()
    if request.method == 'POST':
        n1 = int(request.form.get('nota1', 0))
        n2 = int(request.form.get('nota2', 0))
        n3 = int(request.form.get('nota3', 0))
        nota_final = round((n1 + n2 + n3) / 3, 1)
        aprob = int(request.form.get('nota_aprob', 51))
        n = Nota(
            ins_id=int(request.form['ins_id']), mat_id=int(request.form['mat_id']),
            nota1=n1, nota2=n2, nota3=n3,
            nota_final=nota_final, nota_aprob=aprob,
            aprobado=nota_final >= aprob,
            obs=request.form.get('obs'),
            creado=date.today(), act=date.today(), usu_id=current_user.id
        )
        db.session.add(n); db.session.commit()
        flash('Nota registrada.', 'success')
        return redirect(url_for('nota.index'))
    return render_template('nota/form.html', nota=None, inscritos=inscritos, materias=materias)

@nota_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@permission_required('nota_editar')
def editar(id):
    n = Nota.query.get_or_404(id)
    inscritos = Inscrito.query.filter_by(inscrito=True).all()
    materias  = Materia.query.all()
    if request.method == 'POST':
        n.nota1 = int(request.form.get('nota1', 0))
        n.nota2 = int(request.form.get('nota2', 0))
        n.nota3 = int(request.form.get('nota3', 0))
        n.nota_final = round((n.nota1 + n.nota2 + n.nota3) / 3, 1)
        n.nota_aprob = int(request.form.get('nota_aprob', 51))
        n.aprobado = n.nota_final >= n.nota_aprob
        n.obs = request.form.get('obs'); n.act = date.today()
        db.session.commit(); flash('Nota actualizada.', 'success')
        return redirect(url_for('nota.index'))
    return render_template('nota/form.html', nota=n, inscritos=inscritos, materias=materias)


# ── PAGO ──────────────────────────────────────────────────
pago_bp = Blueprint('pago', __name__, url_prefix='/pago')

@pago_bp.route('/')
@login_required
@permission_required('pago_ver')
def index():
    alu_id = request.args.get('alu_id', type=int)
    alumnos = Alumno.query.filter_by(activo=True).order_by(Alumno.paterno).all()
    pagos = []
    alumno_sel = None
    if alu_id:
        alumno_sel = Alumno.query.get(alu_id)
        ins = Inscrito.query.filter_by(alu_id=alu_id).first()
        if ins:
            pagos = Pago.query.filter_by(ins_id=ins.id).order_by(Pago.nro_cuota).all()
    return render_template('pago/index.html', pagos=pagos, alumnos=alumnos,
                           alu_id=alu_id, alumno_sel=alumno_sel)

@pago_bp.route('/<int:id>/registrar', methods=['GET', 'POST'])
@login_required
@permission_required('pago_crear')
def registrar(id):
    pago = Pago.query.get_or_404(id)
    if request.method == 'POST':
        pago.pagado = True
        pago.metodo_pago = request.form.get('metodo_pago')
        pago.fecha_pago = date.fromisoformat(request.form['fecha_pago'])
        pago.referencia_pago = request.form.get('referencia_pago')
        pago.obs = request.form.get('obs')
        pago.act = date.today(); pago.usu_id = current_user.id
        db.session.commit()
        flash(f'Cuota {pago.nro_cuota} registrada como pagada.', 'success')
        ins = Inscrito.query.get(pago.ins_id)
        return redirect(url_for('pago.index', alu_id=ins.alu_id))
    return render_template('pago/form.html', pago=pago)
