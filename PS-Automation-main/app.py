from flask import Flask, flash, render_template, request, redirect, url_for, session, make_response, send_file
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from datetime import datetime
import pandas as pd
import os, io
from msal import ConfidentialClientApplication
#Librerias para PDF
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer, Paragraph
from reportlab.lib import colors
from io import BytesIO
from flask import make_response
from reportlab.lib.units import inch
from decimal import Decimal


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Pro2DB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




class ManualData(db.Model):
    so = db.Column(db.String(50), primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    group = db.Column(db.String(100), nullable=False)
    project_name = db.Column(db.String(200), nullable=False)
    po = db.Column(db.String(50), nullable=False)
    direct_quote_approved = db.Column(db.Numeric(20, 2), nullable=False)
    vendor = db.Column(db.String(100), nullable=False)
    ms = db.Column(db.String(10), nullable=False)
    business_unit = db.Column(db.String(100), nullable=False)
    pm = db.Column(db.String(100), nullable=False)
    project_type = db.Column(db.String(100), nullable=False)
    start_date = db.Column(DateTime, default=datetime.utcnow)
    end_date = db.Column(DateTime, default=datetime.utcnow)
    aging_month = db.Column(db.Integer, nullable=False)
    aging_group = db.Column(db.String(100), nullable=False)
    psg_p_budgeted = db.Column(db.Numeric(20, 2), nullable=False)
    gp_budgeted_3rd_parties = db.Column(db.Numeric(20, 2), nullable=False)
    total_gp_budgeted = db.Column(db.Numeric(20, 2), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    budgeted_ps_nntcl_revenue_po_currency = db.Column(db.Numeric(20, 2), nullable=False)
    budgeted_3rd_party_revenue_po_currency = db.Column(db.Numeric(20, 2), nullable=False)
    total_budgeted_revenue_po_currency = db.Column(db.Numeric(20, 2), nullable=False)
    budgeted_ps_cost_po_currency = db.Column(db.Numeric(20, 2), nullable=False)
    budgeted_3rd_parties_cost_po_currency = db.Column(db.Numeric(20, 2), nullable=False)
    total_budgeted_cost_po_currency = db.Column(db.Numeric(20, 2), nullable=False)
    budgeted_ps_nntcl_revenue_usd = db.Column(db.Numeric(20, 2), nullable=False)
    budgeted_3rd_party_revenue_usd = db.Column(db.Numeric(20, 2), nullable=False)
    total_budgeted_revenue_usd = db.Column(db.Numeric(20, 2), nullable=False)
    budgeted_ps_cost_usd = db.Column(db.Numeric(20, 2), nullable=False)
    budgeted_3rd_parties_cost_usd = db.Column(db.Numeric(20, 2), nullable=False)
    total_budgeted_cost_usd = db.Column(db.Numeric(20, 2), nullable=False)
    subcontractor_currency = db.Column(db.String(3), nullable=False)
    total_subcontractor_cost_rq_currency = db.Column(db.Numeric(20, 2), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    previous_fy_recognition = db.Column(db.Numeric(10, 2), nullable=False)
    actual_revenue_recognition_percent = db.Column(db.Numeric(10, 2), nullable=False)
    pending_revenue_recognition_fy23_percent = db.Column(db.Numeric(10, 2), nullable=False)
    forecast_project_completed_fy23_percent = db.Column(db.Numeric(10, 2), nullable=False)
    actual_backlog_usd = db.Column(db.Numeric(20, 2), nullable=False)
    project_state = db.Column(db.String(100), nullable=False)
    advanced_category2 = db.Column(db.String(100), nullable=False)
    tecnologia_principal = db.Column(db.String(100), nullable=False)
    tecnologia_secundaria = db.Column(db.String(100), nullable=False)
    tecnologia_secundaria2 = db.Column(db.String(100), nullable=False)
    technical_lead = db.Column(db.String(100), nullable=False)
    ingeniero1 = db.Column(db.String(100), default="-")
    ingeniero2 = db.Column(db.String(100), default="-")
    ingeniero3 = db.Column(db.String(100), default="-")
    ingeniero4 = db.Column(db.String(100), default="-")
    ingeniero5 = db.Column(db.String(100), default="-")
    ingeniero6 = db.Column(db.String(100), default="-")
    ingeniero7 = db.Column(db.String(100), default="-")
    responsible_name = db.Column(db.String(100), nullable=False)
    responsible_name_edit = db.Column(db.String(100))
    responsible_edited_at = db.Column(db.DateTime) 
class DataForecastApr(db.Model):
    __tablename__ = 'data_forecast_apr'
    id = db.Column(db.Integer, primary_key=True)
    so_id = db.Column(db.String(50), db.ForeignKey('manual_data.so'), nullable=False)
    forecast_advance_apr_percent = db.Column(db.Numeric(10, 2), nullable=False)
    forecast_project_completed_apr_percent = db.Column(db.Numeric(10, 2), nullable=False)
    forecast_total_recognition_apr_usd = db.Column(db.Numeric(20, 2), nullable=False)
    real_advance_apr_percent = db.Column(db.Numeric(10, 2), nullable=False)
    real_project_completed_apr_percent = db.Column(db.Numeric(10, 2), nullable=False)
    real_total_recognition_apr_usd = db.Column(db.Numeric(20, 2), nullable=False)
    manual_data = db.relationship('ManualData', backref='data_forecast_apr')

class DataForecastMay(db.Model):
    __tablename__ = 'data_forecast_may'
    id = db.Column(db.Integer, primary_key=True)
    so_id = db.Column(db.String(50), db.ForeignKey('manual_data.so'), nullable=False)
    forecast_advance_may_percent = db.Column(db.Numeric(10, 2), nullable=False)
    forecast_project_completed_may_percent = db.Column(db.Numeric(10, 2), nullable=False)
    forecast_total_recognition_may_usd = db.Column(db.Numeric(20, 2), nullable=False)
    real_advance_may_percent = db.Column(db.Numeric(10, 2), nullable=False)
    real_project_completed_may_percent = db.Column(db.Numeric(10, 2), nullable=False)
    real_total_recognition_may_usd = db.Column(db.Numeric(20, 2), nullable=False)
    manual_data = db.relationship('ManualData', backref='data_forecast_may')

class DataForecastJun(db.Model):
    __tablename__ = 'data_forecast_jun'
    id = db.Column(db.Integer, primary_key=True)
    so_id = db.Column(db.String(50), db.ForeignKey('manual_data.so'), nullable=False)
    forecast_advance_jun_percent = db.Column(db.Numeric(10, 2), nullable=False)
    forecast_project_completed_jun_percent = db.Column(db.Numeric(10, 2), nullable=False)
    forecast_total_recognition_jun_usd = db.Column(db.Numeric(20, 2), nullable=False)
    real_advance_jun_percent = db.Column(db.Numeric(10, 2), nullable=False)
    real_project_completed_jun_percent = db.Column(db.Numeric(10, 2), nullable=False)
    real_total_recognition_jun_usd = db.Column(db.Numeric(20, 2), nullable=False)
    manual_data = db.relationship('ManualData', backref='data_forecast_jun')

class DataForecastJul(db.Model):
    __tablename__ = 'data_forecast_jul'
    id = db.Column(db.Integer, primary_key=True)
    so_id = db.Column(db.String(50), db.ForeignKey('manual_data.so'), nullable=False)
    forecast_advance_jul_percent = db.Column(db.Numeric(10, 2), nullable=False)
    forecast_project_completed_jul_percent = db.Column(db.Numeric(10, 2), nullable=False)
    forecast_total_recognition_jul_usd = db.Column(db.Numeric(20, 2), nullable=False)
    real_advance_jul_percent = db.Column(db.Numeric(10, 2), nullable=False)
    real_project_completed_jul_percent = db.Column(db.Numeric(10, 2), nullable=False)
    real_total_recognition_jul_usd = db.Column(db.Numeric(20, 2), nullable=False)
    manual_data = db.relationship('ManualData', backref='data_forecast_jul')

class DataForecastAug(db.Model):
    __tablename__ = 'data_forecast_aug'
    id = db.Column(db.Integer, primary_key=True)
    so_id = db.Column(db.String(50), db.ForeignKey('manual_data.so'), nullable=False)
    forecast_advance_aug_percent = db.Column(db.Numeric(10, 2), nullable=False)
    forecast_project_completed_aug_percent = db.Column(db.Numeric(10, 2), nullable=False)
    forecast_total_recognition_aug_usd = db.Column(db.Numeric(20, 2), nullable=False)
    real_advance_aug_percent = db.Column(db.Numeric(10, 2), nullable=False)
    real_project_completed_aug_percent = db.Column(db.Numeric(10, 2), nullable=False)
    real_total_recognition_aug_usd = db.Column(db.Numeric(20, 2), nullable=False)
    manual_data = db.relationship('ManualData', backref='data_forecast_aug')

class DataForecastSep(db.Model):
    __tablename__ = 'data_forecast_sep'
    id = db.Column(db.Integer, primary_key=True)
    so_id = db.Column(db.String(50), db.ForeignKey('manual_data.so'), nullable=False)
    forecast_advance_sep_percent = db.Column(db.Numeric(10, 2), nullable=False)
    forecast_project_completed_sep_percent = db.Column(db.Numeric(10, 2), nullable=False)
    forecast_total_recognition_sep_usd = db.Column(db.Numeric(20, 2), nullable=False)
    real_advance_sep_percent = db.Column(db.Numeric(10, 2), nullable=False)
    real_project_completed_sep_percent = db.Column(db.Numeric(10, 2), nullable=False)
    real_total_recognition_sep_usd = db.Column(db.Numeric(20, 2), nullable=False)
    manual_data = db.relationship('ManualData', backref='data_forecast_sep')

class DataForecastOct(db.Model):
    __tablename__ = 'data_forecast_oct'
    id = db.Column(db.Integer, primary_key=True)
    so_id = db.Column(db.String(50), db.ForeignKey('manual_data.so'), nullable=False)
    forecast_advance_oct_percent = db.Column(db.Numeric(10, 2), nullable=False)
    forecast_project_completed_oct_percent = db.Column(db.Numeric(10, 2), nullable=False)
    forecast_total_recognition_oct_usd = db.Column(db.Numeric(20, 2), nullable=False)
    real_advance_oct_percent = db.Column(db.Numeric(10, 2), nullable=False)
    real_project_completed_oct_percent = db.Column(db.Numeric(10, 2), nullable=False)
    real_total_recognition_oct_usd = db.Column(db.Numeric(20, 2), nullable=False)
    manual_data = db.relationship('ManualData', backref='data_forecast_oct')

class DataForecastNov(db.Model):
    __tablename__ = 'data_forecast_nov'
    id = db.Column(db.Integer, primary_key=True)
    so_id = db.Column(db.String(50), db.ForeignKey('manual_data.so'), nullable=False)
    forecast_advance_nov_percent = db.Column(db.Numeric(10, 2), nullable=False)
    forecast_project_completed_nov_percent = db.Column(db.Numeric(10, 2), nullable=False)
    forecast_total_recognition_nov_usd = db.Column(db.Numeric(20, 2), nullable=False)
    real_advance_nov_percent = db.Column(db.Numeric(10, 2), nullable=False)
    real_project_completed_nov_percent = db.Column(db.Numeric(10, 2), nullable=False)
    real_total_recognition_nov_usd = db.Column(db.Numeric(20, 2), nullable=False)
    manual_data = db.relationship('ManualData', backref='data_forecast_nov')

class DataForecastDec(db.Model):
    __tablename__ = 'data_forecast_dec'
    id = db.Column(db.Integer, primary_key=True)
    so_id = db.Column(db.String(50), db.ForeignKey('manual_data.so'), nullable=False)
    forecast_advance_dec_percent = db.Column(db.Numeric(10, 2), nullable=False)
    forecast_project_completed_dec_percent = db.Column(db.Numeric(10, 2), nullable=False)
    forecast_total_recognition_dec_usd = db.Column(db.Numeric(20, 2), nullable=False)
    real_advance_dec_percent = db.Column(db.Numeric(10, 2), nullable=False)
    real_project_completed_dec_percent = db.Column(db.Numeric(10, 2), nullable=False)
    real_total_recognition_dec_usd = db.Column(db.Numeric(20, 2), nullable=False)
    manual_data = db.relationship('ManualData', backref='data_forecast_dec')

class DataForecastJan(db.Model):
    __tablename__ = 'data_forecast_jan'
    id = db.Column(db.Integer, primary_key=True)
    so_id = db.Column(db.String(50), db.ForeignKey('manual_data.so'), nullable=False)
    forecast_advance_jan_percent = db.Column(db.Numeric(10, 2), nullable=False)
    forecast_project_completed_jan_percent = db.Column(db.Numeric(10, 2), nullable=False)
    forecast_total_recognition_jan_usd = db.Column(db.Numeric(20, 2), nullable=False)
    real_advance_jan_percent = db.Column(db.Numeric(10, 2), nullable=False)
    real_project_completed_jan_percent = db.Column(db.Numeric(10, 2), nullable=False)
    real_total_recognition_jan_usd = db.Column(db.Numeric(20, 2), nullable=False)
    manual_data = db.relationship('ManualData', backref='data_forecast_jan')

class DataForecastFeb(db.Model):
    __tablename__ = 'data_forecast_feb'
    id = db.Column(db.Integer, primary_key=True)
    so_id = db.Column(db.String(50), db.ForeignKey('manual_data.so'), nullable=False)
    forecast_advance_feb_percent = db.Column(db.Numeric(10, 2), nullable=False)
    forecast_project_completed_feb_percent = db.Column(db.Numeric(10, 2), nullable=False)
    forecast_total_recognition_feb_usd = db.Column(db.Numeric(20, 2), nullable=False)
    real_advance_feb_percent = db.Column(db.Numeric(10, 2), nullable=False)
    real_project_completed_feb_percent = db.Column(db.Numeric(10, 2), nullable=False)
    real_total_recognition_feb_usd = db.Column(db.Numeric(20, 2), nullable=False)
    manual_data = db.relationship('ManualData', backref='data_forecast_feb')

class DataForecastMar(db.Model):
    __tablename__ = 'data_forecast_mar'
    id = db.Column(db.Integer, primary_key=True)
    so_id = db.Column(db.String(50), db.ForeignKey('manual_data.so'), nullable=False)
    forecast_advance_mar_percent = db.Column(db.Numeric(10, 2), nullable=False)
    forecast_project_completed_mar_percent = db.Column(db.Numeric(10, 2), nullable=False)
    forecast_total_recognition_mar_usd = db.Column(db.Numeric(20, 2), nullable=False)
    real_advance_mar_percent = db.Column(db.Numeric(10, 2), nullable=False)
    real_project_completed_mar_percent = db.Column(db.Numeric(10, 2), nullable=False)
    real_total_recognition_mar_usd = db.Column(db.Numeric(20, 2), nullable=False)
    real_ps_recognition_mar_usd = db.Column(db.Numeric(20, 2), nullable=False)
    real_contractor_recognition_mar_usd = db.Column(db.Numeric(20, 2), nullable=False)
    real_backlog_mar_usd = db.Column(db.Numeric(20, 2), nullable=False)
    real_total_cost_mar_usd = db.Column(db.Numeric(20, 2), nullable=False)
    real_cost_ps_mar_usd = db.Column(db.Numeric(20, 2), nullable=False)
    real_cost_3rd_party_mar_usd = db.Column(db.Numeric(20, 2), nullable=False)
    real_total_recognition_mar_currency_po = db.Column(db.Numeric(20, 2), nullable=False)
    real_ps_recognition_mar_currency_po = db.Column(db.Numeric(20, 2), nullable=False)
    real_contractor_recognition_mar_currency_po = db.Column(db.Numeric(20, 2), nullable=False)
    real_total_cost_mar_currency_po = db.Column(db.Numeric(20, 2), nullable=False)
    real_cost_ps_mar_currency_po = db.Column(db.Numeric(20, 2), nullable=False)
    real_cost_3rd_party_mar_currency_po = db.Column(db.Numeric(20, 2), nullable=False)
    manual_data = db.relationship('ManualData', backref='data_forecast_mar')


class Comment(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    so_id = db.Column(db.Integer, db.ForeignKey('manual_data.so'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(DateTime, default=datetime.now)
    edited_at = db.Column(db.DateTime) 
    manual_data = db.relationship('ManualData', backref='comments')
#Datos desde EIP
#datos_pedidos = [
#    {"Source": "Fuente 1", "OrderItemNumber": 1, "Client": "Cliente A", "OrderingCountry": "País 1"},
#    {"Source": "Fuente 2", "OrderItemNumber": 2, "Client": "Cliente B", "OrderingCountry": "País 2"},

#]


@app.route('/')
def index():
    return render_template('base.html')

#Mostrar datos de DB EIP
#@app.route('/render_datos_edw')
#def mostrar_datos():
#    return render_template('render_datos_edw.html', datos_pedidos=datos_pedidos)

#@app.route('/')
#def home():
#   if not azure.authorized:
#      return redirect(url_for('azure.login'))
#   resp = azure.get('/v1.0/me')
#   assert resp.ok, resp.text
#   return render_template('home.html', user=resp.json())

#@app.route('/logout')
#def logout():
#    azure.logout()
#    return redirect('/')



@app.route('/visualizar_so', methods=['GET', 'POST'])
def visualizar_so():
    search_query = request.args.get('search_query')
    
    if search_query:
        # Buscar todos los datos de ManualData que contengan el carácter ingresado
        manual_data = ManualData.query.filter(ManualData.so.contains(search_query)).all()
    else:
        # Obtener todos los datos de ManualData
        manual_data = ManualData.query.all()
    return render_template('visualizar_so.html', manual_data=manual_data, search_query=search_query,)

@app.route('/Select_month', methods=['GET'])
def Select_month():
    return render_template('Select_month.html', )

@app.route('/visualizar_forecast_mes', methods=['GET'])
def visualizar_forecast_mes():
    mes = request.args.get('mes')
    if not mes:
        flash('Seleccione un mes para visualizar los datos.', 'warning')
        return redirect(url_for('Select_month'))

    # Obtener la clase de modelo correspondiente al mes
    model_class = globals().get(f'DataForecast{mes.capitalize()}')
    if not model_class:
        flash('Mes no válido seleccionado.', 'danger')
        return redirect(url_for('Select_month'), )

    # Obtener los datos del mes seleccionado
    forecasts = model_class.query.all()
    return render_template('visualizar_forecast_mes.html', forecasts=forecasts, mes=mes)


@app.route('/cargar_datos_manuales', methods=['GET', 'POST'])
def cargar_datos_manuales():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        errors = {}

        numeric_fields = [
            'psg_p_budgeted', 'gp_budgeted_3rd_parties', 'total_gp_budgeted',
            'budgeted_ps_nntcl_revenue_po_currency', 'budgeted_3rd_party_revenue_po_currency',
            'total_budgeted_revenue_po_currency', 'budgeted_ps_cost_po_currency',
            'budgeted_3rd_parties_cost_po_currency', 'total_budgeted_cost_po_currency',
            'budgeted_ps_nntcl_revenue_usd', 'budgeted_3rd_party_revenue_usd',
            'total_budgeted_revenue_usd', 'budgeted_ps_cost_usd',
            'budgeted_3rd_parties_cost_usd', 'total_budgeted_cost_usd',
            'previous_fy_recognition', 'actual_revenue_recognition_percent',
            'pending_revenue_recognition_fy23_percent', 'forecast_project_completed_fy23_percent',
            'actual_backlog_usd', 'direct_quote_approved'
        ]

        for field in numeric_fields:
            try:
                form_data[field] = float(form_data[field].replace(',', '.')) if form_data[field] else 0.0
            except ValueError:
                errors[field] = 'Solo se permiten números y decimales en los campos numéricos.'

        if errors:
            for field, error in errors.items():
                flash(f'Error en el campo {field}: {error}', 'danger')
            return render_template('cargar_datos_manuales.html', form_data=form_data, errors=errors)

        existing_record = ManualData.query.filter_by(so=form_data['so']).first()
        if existing_record:
            flash(f'El Sales Order {form_data["so"]} ya existe.', 'danger')
            return render_template('cargar_datos_manuales.html', form_data=form_data, errors={})

        try:
             # Procesar ingenieros dinámicamente
            ingenieros = []
            for key, value in form_data.items():
                if key.startswith('ingeniero') and value:
                    ingenieros.append(value)
            form_data['total_budgeted_revenue_po_currency'] = form_data['budgeted_ps_nntcl_revenue_po_currency'] + form_data['budgeted_3rd_party_revenue_po_currency']
            form_data['total_budgeted_cost_po_currency'] = form_data['budgeted_ps_cost_po_currency'] + form_data['budgeted_3rd_parties_cost_po_currency']
            form_data['total_budgeted_revenue_usd'] = form_data['budgeted_ps_nntcl_revenue_usd'] + form_data['budgeted_3rd_party_revenue_usd']
            form_data['total_budgeted_cost_usd'] = form_data['budgeted_ps_cost_usd'] + form_data['budgeted_3rd_parties_cost_usd']

            manual_data = ManualData(
                so=form_data['so'],
                client_name=form_data['client_name'],
                group=form_data['group'],
                project_name=form_data['project_name'],
                po=form_data['po'],
                direct_quote_approved=form_data['direct_quote_approved'],
                vendor=form_data['vendor'],
                ms=form_data['ms'],
                business_unit=form_data['business_unit'],
                pm=form_data['pm'],
                project_type=form_data['project_type'],
                start_date=datetime.strptime(form_data['start_date'], '%Y-%m-%d'),
                end_date=datetime.strptime(form_data['end_date'], '%Y-%m-%d'),
                aging_month=int(form_data['aging_month']),
                aging_group=form_data['aging_group'],
                psg_p_budgeted=form_data['psg_p_budgeted'],
                gp_budgeted_3rd_parties=form_data['gp_budgeted_3rd_parties'],
                total_gp_budgeted=form_data['total_gp_budgeted'],
                currency=form_data['currency'],
                budgeted_ps_nntcl_revenue_po_currency=form_data['budgeted_ps_nntcl_revenue_po_currency'],
                budgeted_3rd_party_revenue_po_currency=form_data['budgeted_3rd_party_revenue_po_currency'],
                total_budgeted_revenue_po_currency=form_data['total_budgeted_revenue_po_currency'],
                budgeted_ps_cost_po_currency=form_data['budgeted_ps_cost_po_currency'],
                budgeted_3rd_parties_cost_po_currency=form_data['budgeted_3rd_parties_cost_po_currency'],
                total_budgeted_cost_po_currency=form_data['total_budgeted_cost_po_currency'],
                budgeted_ps_nntcl_revenue_usd=form_data['budgeted_ps_nntcl_revenue_usd'],
                budgeted_3rd_party_revenue_usd=form_data['budgeted_3rd_party_revenue_usd'],
                total_budgeted_revenue_usd=form_data['total_budgeted_revenue_usd'],
                budgeted_ps_cost_usd=form_data['budgeted_ps_cost_usd'],
                budgeted_3rd_parties_cost_usd=form_data['budgeted_3rd_parties_cost_usd'],
                total_budgeted_cost_usd=form_data['total_budgeted_cost_usd'],
                subcontractor_currency=form_data['subcontractor_currency'],
                total_subcontractor_cost_rq_currency=form_data['total_subcontractor_cost_rq_currency'],
                country=form_data['country'],
                previous_fy_recognition=form_data['previous_fy_recognition'],
                actual_revenue_recognition_percent=0.0,
                pending_revenue_recognition_fy23_percent=form_data['pending_revenue_recognition_fy23_percent'],
                forecast_project_completed_fy23_percent=0.0,
                actual_backlog_usd=form_data['actual_backlog_usd'],
                project_state=form_data['project_state'],
                advanced_category2='',
                tecnologia_principal=form_data['tecnologia_principal'],
                tecnologia_secundaria=form_data['tecnologia_secundaria'],
                tecnologia_secundaria2=form_data['tecnologia_secundaria2'],
                technical_lead=form_data['technical_lead'],
            
                responsible_name=form_data['responsible_name'],
            )
            # Asignar ingenieros al proyecto
            for i, ingeniero in enumerate(ingenieros):
                setattr(manual_data, f'ingeniero{i+1}', ingeniero)

            db.session.add(manual_data)
            db.session.commit()
            # Creación del comentario por defecto
            default_comment = Comment(
                so_id=manual_data.so,
                comment=f"SO creado por {manual_data.responsible_name}",
                created_at=datetime.now()
            )
            db.session.add(default_comment)
            db.session.commit()
            
            flash('Datos guardados exitosamente.', 'success')
            return redirect(url_for('visualizar_so', ))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al guardar los datos: {str(e)}', 'danger')
            return render_template('cargar_datos_manuales.html', form_data=form_data, errors={}, )

    return render_template('cargar_datos_manuales.html', form_data={}, errors={}, )



# Función para calcular el reconocimiento de ingresos
def calculate_recognition(form_data, month, total_budgeted_revenue_usd, actual_revenue_recognition_percent):
    # Generar las claves dinámicas para los diferentes campos
    forecast_advance_key = f'forecast_advance_{month}_percent'
    forecast_total_recognition_key = f'forecast_total_recognition_{month}_usd'
    real_advance_key = f'real_advance_{month}_percent'
    real_total_recognition_key = f'real_total_recognition_{month}_usd'
    forecast_project_completed_key = f'forecast_project_completed_{month}_percent'
    real_project_completed_key = f'real_project_completed_{month}_percent'

    # Calcular el total de reconocimiento proyectado en USD
    form_data[forecast_total_recognition_key] = Decimal(0.01) * Decimal(form_data.get(forecast_advance_key, 0)) * total_budgeted_revenue_usd
    # Calcular el total de reconocimiento real en USD
    form_data[real_total_recognition_key] = Decimal(0.01) * Decimal(form_data.get(real_advance_key, 0)) * total_budgeted_revenue_usd

    # Calcular el porcentaje de proyecto completado proyectado
    form_data[forecast_project_completed_key] = actual_revenue_recognition_percent + Decimal(form_data.get(forecast_advance_key, 0))
    # Calcular el porcentaje de proyecto completado real
    form_data[real_project_completed_key] = actual_revenue_recognition_percent + Decimal(form_data.get(real_advance_key, 0))

    # Debugging prints (puedes eliminarlos si no los necesitas)
    print(f"Calculated {forecast_total_recognition_key}: {form_data[forecast_total_recognition_key]}")
    print(f"Calculated {real_total_recognition_key}: {form_data[real_total_recognition_key]}")
    print(f"Calculated {forecast_project_completed_key}: {form_data[forecast_project_completed_key]}")
    print(f"Calculated {real_project_completed_key}: {form_data[real_project_completed_key]}")

# Función para manejar el forecast mensual
def handle_monthly_forecast(form_data, month):
    so_id = form_data['so_id']  # Obtener el ID del Sales Order

    # Definir los campos numéricos que deben ser procesados
    numeric_fields = [
        f'forecast_advance_{month}_percent', f'forecast_project_completed_{month}_percent', f'forecast_total_recognition_{month}_usd',
        f'real_advance_{month}_percent', f'real_project_completed_{month}_percent', f'real_total_recognition_{month}_usd'
    ]

    # Si el mes es marzo, añadir campos adicionales específicos para marzo
    if month == 'mar':
        numeric_fields.extend([
            'real_ps_recognition_mar_usd', 'real_contractor_recognition_mar_usd', 'real_backlog_mar_usd',
            'real_total_cost_mar_usd', 'real_cost_ps_mar_usd', 'real_cost_3rd_party_mar_usd',
            'real_total_recognition_mar_currency_po', 'real_ps_recognition_mar_currency_po', 'real_contractor_recognition_mar_currency_po',
            'real_total_cost_mar_currency_po', 'real_cost_ps_mar_currency_po', 'real_cost_3rd_party_mar_currency_po'
        ])

    # Convertir valores numéricos del formulario a Decimal
    for field in numeric_fields:
        try:
            form_data[field] = Decimal(form_data.get(field, 0).replace(',', '.')) if form_data.get(field) else Decimal(0.0)
        except ValueError:
            flash(f'Error en el campo {field}: Solo se permiten números y decimales.', 'danger')
            return False

    # Obtener datos manuales del Sales Order
    manual_data = ManualData.query.filter_by(so=so_id).first()
    if not manual_data:
        flash('No se encontró un Sales Order con el ID proporcionado.', 'danger')
        return False

    total_budgeted_revenue_usd = Decimal(manual_data.total_budgeted_revenue_usd)

    # Listas para almacenar los avances reales y proyectados de los meses anteriores
    real_advances = []
    forecast_advances = []
    for m in ['apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'jan', 'feb', 'mar']:
        if m == month:
            break
        # `globals()` se utiliza para acceder dinámicamente a la clase del mes correspondiente
        previous_forecast = db.session.query(globals()[f'DataForecast{m.capitalize()}']).filter_by(so_id=so_id).first()
        if previous_forecast:
            # `getattr()` se utiliza para obtener dinámicamente los atributos de las instancias de las clases
            real_advances.append(getattr(previous_forecast, f'real_advance_{m}_percent', Decimal(0.0)))
            forecast_advances.append(getattr(previous_forecast, f'forecast_advance_{m}_percent', Decimal(0.0)))

    # Calcular actual_revenue_recognition_percent sin incluir el mes actual
    actual_revenue_recognition_percent = Decimal(manual_data.previous_fy_recognition) + sum(real_advances)

    # Calcular real_project_completed_percent sumando el avance real del mes actual
    real_project_completed_percent = actual_revenue_recognition_percent + Decimal(form_data.get(f'real_advance_{month}_percent', 0))

    # Calcular forecast_project_completed_percent sumando el avance proyectado del mes actual
    forecast_project_completed_percent = actual_revenue_recognition_percent + Decimal(form_data.get(f'forecast_advance_{month}_percent', 0))

    # Actualizar actual_revenue_recognition_percent para uso futuro
    actual_revenue_recognition_percent += Decimal(form_data.get(f'real_advance_{month}_percent', 0))
    manual_data.actual_revenue_recognition_percent = actual_revenue_recognition_percent

    # Llamar a la función de cálculo de reconocimiento
    calculate_recognition(form_data, month, total_budgeted_revenue_usd, actual_revenue_recognition_percent)

    # Actualizar los campos de proyecto completado en el formulario
    form_data[f'forecast_project_completed_{month}_percent'] = forecast_project_completed_percent
    form_data[f'real_project_completed_{month}_percent'] = real_project_completed_percent

    # Calcular el porcentaje de reconocimiento de ingresos pendientes para el FY23
    pending_revenue_recognition_fy23_percent = sum(forecast_advances) + Decimal(form_data.get(f'forecast_advance_{month}_percent', 0))
    manual_data.pending_revenue_recognition_fy23_percent = pending_revenue_recognition_fy23_percent

    # Actualizar forecast_project_completed_fy23_percent
    manual_data.forecast_project_completed_fy23_percent = pending_revenue_recognition_fy23_percent + actual_revenue_recognition_percent

    # Calcular el backlog real en USD si el proyecto no está cancelado
    if manual_data.project_state.lower() == 'cancelled':
        actual_backlog_usd = Decimal(0.0)
    else:
        actual_backlog_usd = (Decimal(1.0) - Decimal(0.01) * actual_revenue_recognition_percent) * total_budgeted_revenue_usd

    manual_data.actual_backlog_usd = actual_backlog_usd

    # Si el mes es marzo, calcular el backlog real específico para marzo
    if month == 'mar':
        if form_data['real_project_completed_mar_percent'] == "":
            real_backlog_mar_usd = Decimal(0.0)
        else:
            real_backlog_mar_usd = (Decimal(1.0) - Decimal(0.01) * Decimal(form_data['real_project_completed_mar_percent'])) * total_budgeted_revenue_usd
        form_data['real_backlog_mar_usd'] = real_backlog_mar_usd

    # Crear una nueva instancia del modelo para el mes específico
    # `globals()` se utiliza para obtener dinámicamente la clase del modelo correspondiente al mes
    model_class = globals()[f'DataForecast{month.capitalize()}'] 
    new_forecast = model_class(
        so_id=so_id,
        **{f'forecast_advance_{month}_percent': form_data[f'forecast_advance_{month}_percent'],
           f'forecast_project_completed_{month}_percent': form_data[f'forecast_project_completed_{month}_percent'],
           f'forecast_total_recognition_{month}_usd': form_data[f'forecast_total_recognition_{month}_usd'],
           f'real_advance_{month}_percent': form_data[f'real_advance_{month}_percent'],
           f'real_project_completed_{month}_percent': form_data[f'real_project_completed_{month}_percent'],
           f'real_total_recognition_{month}_usd': form_data[f'real_total_recognition_{month}_usd']}
    )

    # Si es marzo, añadir campos adicionales específicos para marzo
    if month == 'mar':
        new_forecast.real_ps_recognition_mar_usd = form_data['real_ps_recognition_mar_usd']
        new_forecast.real_contractor_recognition_mar_usd = form_data['real_contractor_recognition_mar_usd']
        new_forecast.real_backlog_mar_usd = form_data['real_backlog_mar_usd']
        new_forecast.real_total_cost_mar_usd = form_data['real_total_cost_mar_usd']
        new_forecast.real_cost_ps_mar_usd = form_data['real_cost_ps_mar_usd']
        new_forecast.real_cost_3rd_party_mar_usd = form_data['real_cost_3rd_party_mar_usd']
        new_forecast.real_total_recognition_mar_currency_po = form_data['real_total_recognition_mar_currency_po']
        new_forecast.real_ps_recognition_mar_currency_po = form_data['real_ps_recognition_mar_currency_po']
        new_forecast.real_contractor_recognition_mar_currency_po = form_data['real_contractor_recognition_mar_currency_po']
        new_forecast.real_total_cost_mar_currency_po = form_data['real_total_cost_mar_currency_po']
        new_forecast.real_cost_ps_mar_currency_po = form_data['real_cost_ps_mar_currency_po']
        new_forecast.real_cost_3rd_party_mar_currency_po = form_data['real_cost_3rd_party_mar_currency_po']

    # Añadir la nueva instancia a la sesión y guardar en la base de datos
    db.session.add(new_forecast)
    db.session.commit()

    return True

# Ruta para agregar datos de forecast
@app.route('/add_data_forecast', methods=['GET', 'POST'])
def add_data_forecast():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        so_id = form_data.get('so_id')
        month = form_data.get('month')
        return redirect(url_for('add_data_forecast_month', month=month, so_id=so_id))
    
    # Obtener la lista de Sales Orders
    sales_orders = ManualData.query.order_by(ManualData.start_date.desc()).all()
    return render_template('add_data_forecast.html', sales_orders=sales_orders)

# Ruta para agregar datos de forecast para un mes específico
@app.route('/add_data_forecast/<month>', methods=['GET', 'POST'])
def add_data_forecast_month(month):
    so_id = request.args.get('so_id')
    manual_data = ManualData.query.filter_by(so=so_id).first()
    
    if not manual_data:
        flash('No se encontró un Sales Order con el ID proporcionado.', 'danger')
        return redirect(url_for('add_data_forecast'))

    if request.method == 'POST':
        form_data = request.form.to_dict()
        form_data['so_id'] = so_id  # Añadir el so_id al form_data
        if handle_monthly_forecast(form_data, month):
            flash(f'Datos de forecast para {month} guardados exitosamente.', 'success')
            return redirect(url_for('visualizar_so', month=month, so_id=so_id))
    
    sales_orders = ManualData.query.order_by(ManualData.start_date.desc()).all()
    return render_template(f'month/{month}.html', sales_orders=sales_orders, so_id=so_id, manual_data=manual_data)

# Ruta para agregar datos de forecast
@app.route('/add_data_forecast', methods=['GET', 'POST'])
def add_data_forecast():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        so_id = form_data.get('so_id')
        month = form_data.get('month')
        return redirect(url_for('add_data_forecast_month', month=month, so_id=so_id))
    
    # Obtener la lista de Sales Orders
    sales_orders = ManualData.query.order_by(ManualData.start_date.desc()).all()
    return render_template('add_data_forecast.html', sales_orders=sales_orders)

# Ruta para agregar datos de forecast para un mes específico
@app.route('/add_data_forecast/<month>', methods=['GET', 'POST'])
def add_data_forecast_month(month):
    so_id = request.args.get('so_id')
    manual_data = ManualData.query.filter_by(so=so_id).first()
    
    if not manual_data:
        flash('No se encontró un Sales Order con el ID proporcionado.', 'danger')
        return redirect(url_for('add_data_forecast'))

    if request.method == 'POST':
        form_data = request.form.to_dict()
        form_data['so_id'] = so_id  # Añadir el so_id al form_data
        if handle_monthly_forecast(form_data, month):
            flash(f'Datos de forecast para {month} guardados exitosamente.', 'success')
            return redirect(url_for('visualizar_so', month=month, so_id=so_id))
    
    sales_orders = ManualData.query.order_by(ManualData.start_date.desc()).all()
    return render_template(f'month/{month}.html', sales_orders=sales_orders, so_id=so_id, manual_data=manual_data)


@app.route('/editar_comen/<int:comment_id>', methods=['GET', 'POST'])
def editar_comen(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    manual_data = comment.manual_data

    if request.method == 'POST':
        # Obtener los datos del formulario
        new_comment = request.form['comment']

        # Actualizar el comentario
        comment.comment = new_comment

        #Fecha edicion
        comment.edited_at = datetime.now()
        db.session.commit()

        return redirect(url_for('detalles_so', so=manual_data.so, ))

    return render_template('editar_comen.html', comment=comment, manual_data=manual_data,)
    
#Vista para visualizar detalles de cada SO individual
@app.route('/detalles_so/<string:so>',methods=['GET', 'POST'])
def detalles_so(so):
    manual_data = ManualData.query.get_or_404(so)
        
    if request.method == 'POST':
        #Comentarios del formulario
        comments = request.form.get('comments')
        new_comment = Comment(so_id=manual_data.so, comment=comments)
        db.session.add(new_comment)
        db.session.commit()

    datos_so = {
        "so":manual_data.so,
        "client_name":manual_data.client_name,
        "group":manual_data.group,
        "project_name":manual_data.project_name,
        "po":manual_data.po,
        "direct_quote_approved":manual_data.direct_quote_approved,
        "vendor":manual_data.vendor,
        "ms":manual_data.ms,
        "business_unit":manual_data.business_unit,
        "pm":manual_data.pm,
        "project_type":manual_data.project_type,
        "start_date":manual_data.start_date,
        "end_date":manual_data.end_date,
        "aging_month":manual_data.aging_month,
        "aging_group":manual_data.aging_group,
        "psg_p_budgeted":manual_data.psg_p_budgeted,
        "gp_budgeted_3rd_parties":manual_data.gp_budgeted_3rd_parties,
        "total_gp_budgeted":manual_data.total_gp_budgeted,
        "currency":manual_data.currency,
        "budgeted_ps_nntcl_revenue_po_currency":manual_data.budgeted_ps_nntcl_revenue_po_currency,
        "budgeted_3rd_party_revenue_po_currency":manual_data.budgeted_3rd_party_revenue_po_currency,
        "total_budgeted_revenue_po_currency":manual_data.total_budgeted_revenue_po_currency,
        "budgeted_ps_cost_po_currency":manual_data.budgeted_ps_cost_po_currency,
        "budgeted_3rd_parties_cost_po_currency":manual_data.budgeted_3rd_parties_cost_po_currency,
        "total_budgeted_cost_po_currency":manual_data.total_budgeted_cost_po_currency,
        "budgeted_ps_nntcl_revenue_usd":manual_data.budgeted_ps_nntcl_revenue_usd,
        "budgeted_3rd_party_revenue_usd":manual_data.budgeted_3rd_party_revenue_usd,
        "total_budgeted_revenue_usd":manual_data.total_budgeted_revenue_usd,
        "budgeted_ps_cost_usd":manual_data.budgeted_ps_cost_usd,
        "budgeted_3rd_parties_cost_usd":manual_data.budgeted_3rd_parties_cost_usd,
        "total_budgeted_cost_usd":manual_data.total_budgeted_cost_usd,
        "subcontractor_currency":manual_data.subcontractor_currency,
        "total_subcontractor_cost_rq_currency":manual_data.total_subcontractor_cost_rq_currency,
        "country":manual_data.country,
        "previous_fy_recognition": manual_data.previous_fy_recognition,
        "actual_revenue_recognition_percent": manual_data.actual_revenue_recognition_percent,
        "pending_revenue_recognition_fy23_percent": manual_data.pending_revenue_recognition_fy23_percent,
        "forecast_project_completed_fy23_percent": manual_data.forecast_project_completed_fy23_percent,
        "actual_backlog_usd":manual_data.actual_backlog_usd,
        "project_state":manual_data.project_state,
        "advanced_category2":manual_data.advanced_category2,
        "tecnologia_principal":manual_data.tecnologia_principal,
        "tecnologia_secundaria":manual_data.tecnologia_secundaria,
        "tecnologia_secundaria2":manual_data.tecnologia_secundaria2,
        "technical_lead":manual_data.technical_lead,
        "ingeniero1":manual_data.ingeniero1,
        "ingeniero2":manual_data.ingeniero2,
        "ingeniero3":manual_data.ingeniero3,
        "ingeniero4":manual_data.ingeniero4,
        "ingeniero5":manual_data.ingeniero5,
        "ingeniero6":manual_data.ingeniero6,
        "ingeniero7":manual_data.ingeniero7,
        "comments":manual_data.comments,
        "responsible_name":manual_data.responsible_name,
    }
    return render_template('detalles.html', datos_so=datos_so, )

@app.route('/editar_datos/<string:so>', methods=['GET', 'POST'])
def editar_datos(so):
    manual_data = ManualData.query.get_or_404(so)

    if request.method == 'POST':
        form_data = request.form.to_dict()
        errors = {}

        # Validación de campos de porcentaje
        percentage_fields = [
            'psg_p_budgeted', 'gp_budgeted_3rd_parties', 'total_gp_budgeted',
            'previous_fy_recognition', 'actual_revenue_recognition_percent',
            'pending_revenue_recognition_fy23_percent', 'forecast_project_completed_fy23_percent'
        ]
        
        for field in percentage_fields:
            try:
                form_data[field] = float(form_data[field].replace('%', ''))
            except ValueError:
                errors[field] = 'Solo se permiten números y decimales en los campos de presupuesto.'

        if errors:
            for field, error in errors.items():
                flash(f'Error en el campo {field}: {error}', 'danger')
            return render_template('editar_datos.html', manual_data=manual_data, errors=errors)

        try:
            manual_data.client_name = form_data['client_name']
            manual_data.group = form_data['group']
            manual_data.project_name = form_data['project_name']
            manual_data.po = form_data['po']
            manual_data.direct_quote_approved = form_data.get('direct_quote_approved') == 'on'
            manual_data.vendor = form_data['vendor']
            manual_data.ms = form_data['ms']
            manual_data.business_unit = form_data['business_unit']
            manual_data.pm = form_data['pm']
            manual_data.project_type = form_data['project_type']
            manual_data.start_date = datetime.strptime(form_data['start_date'], '%Y-%m-%d')
            manual_data.end_date = datetime.strptime(form_data['end_date'], '%Y-%m-%d')
            manual_data.aging_month = int(form_data['aging_month'])
            manual_data.aging_group = form_data['aging_group']
            manual_data.psg_p_budgeted = form_data['psg_p_budgeted']
            manual_data.gp_budgeted_3rd_parties = form_data['gp_budgeted_3rd_parties']
            manual_data.total_gp_budgeted = form_data['total_gp_budgeted']
            manual_data.currency = form_data['currency']
            manual_data.budgeted_ps_nntcl_revenue_po_currency = form_data['budgeted_ps_nntcl_revenue_po_currency']
            manual_data.budgeted_3rd_party_revenue_po_currency = form_data['budgeted_3rd_party_revenue_po_currency']
            manual_data.total_budgeted_revenue_po_currency = form_data['total_budgeted_revenue_po_currency']
            manual_data.budgeted_ps_cost_po_currency = form_data['budgeted_ps_cost_po_currency']
            manual_data.budgeted_3rd_parties_cost_po_currency = form_data['budgeted_3rd_parties_cost_po_currency']
            manual_data.total_budgeted_cost_po_currency = form_data['total_budgeted_cost_po_currency']
            manual_data.budgeted_ps_nntcl_revenue_usd = form_data['budgeted_ps_nntcl_revenue_usd']
            manual_data.budgeted_3rd_party_revenue_usd = form_data['budgeted_3rd_party_revenue_usd']
            manual_data.total_budgeted_revenue_usd = form_data['total_budgeted_revenue_usd']
            manual_data.budgeted_ps_cost_usd = form_data['budgeted_ps_cost_usd']
            manual_data.budgeted_3rd_parties_cost_usd = form_data['budgeted_3rd_parties_cost_usd']
            manual_data.total_budgeted_cost_usd = form_data['total_budgeted_cost_usd']
            manual_data.subcontractor_currency = form_data['subcontractor_currency']
            manual_data.total_subcontractor_cost_rq_currency = form_data['total_subcontractor_cost_rq_currency']
            manual_data.country = form_data['country']
            manual_data.previous_fy_recognition = form_data['previous_fy_recognition']
            manual_data.actual_revenue_recognition_percent = form_data['actual_revenue_recognition_percent']
            manual_data.pending_revenue_recognition_fy23_percent = form_data['pending_revenue_recognition_fy23_percent']
            manual_data.forecast_project_completed_fy23_percent = form_data['forecast_project_completed_fy23_percent']
            manual_data.actual_backlog_usd = form_data['actual_backlog_usd']
            manual_data.project_state = form_data['project_state']
            manual_data.advanced_category2 = form_data['advanced_category2']
            manual_data.tecnologia_principal = form_data['tecnologia_principal']
            manual_data.tecnologia_secundaria = form_data['tecnologia_secundaria']
            manual_data.tecnologia_secundaria2 = form_data['tecnologia_secundaria2']
            manual_data.technical_lead = form_data['technical_lead']
            manual_data.ingeniero1 = form_data['ingeniero1']
            manual_data.ingeniero2 = form_data['ingeniero2']
            manual_data.ingeniero3 = form_data['ingeniero3']
            manual_data.ingeniero4 = form_data['ingeniero4']
            manual_data.ingeniero5 = form_data['ingeniero5']
            manual_data.ingeniero6 = form_data['ingeniero6']
            manual_data.ingeniero7 = form_data['ingeniero7']
            manual_data.responsible_name_edit = form_data['responsible_name_edit']
            #Fecha edicion
            manual_data.responsible_edited_at = datetime.now()

            db.session.commit()

             
            # Creación del comentario por defecto
            default_comment = Comment(
                so_id=manual_data.so,
                #comment=f"SO Editado por {manual_data.responsible_name_edit}, el {manual_data.responsible_edited_at.strftime('%d-%m-%Y %H:%M:%S')}"
                comment=f"SO Editado por {manual_data.responsible_name_edit}",
                created_at=datetime.now()
            )
            db.session.add(default_comment)
            db.session.commit()

            flash('Datos actualizados exitosamente.', 'success')
            return redirect(url_for('visualizar_so', ))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al actualizar los datos: {str(e)}', 'danger')
            return render_template('editar_datos.html', manual_data=manual_data, errors={},)

    return render_template('editar_datos.html', manual_data=manual_data, errors={}, )

@app.route('/export_to_excel')
def export_to_excel():
    manual_data = ManualData.query.all()

    # Convierte los objetos SQLAlchemy a un diccionario
    data = []
    for obj in manual_data:
        obj_dict = {}
        for column in obj.__table__.columns:
            obj_dict[column.name] = getattr(obj, column.name)
        data.append(obj_dict)

    df = pd.DataFrame(data)

    # Excluir campos 
    df = df.drop('responsible_name_edit', axis=1)
    df = df.drop('responsible_edited_at', axis=1)

    # Convertir campos de fecha y hora, esto es porque no se muestran adecuadamente en el excel
    df['end_date'] = pd.to_datetime(df['end_date'], format='%d/%m/%Y %H:%M:%S')
    df['start_date'] = pd.to_datetime(df['start_date'], format='%d/%m/%Y %H:%M:%S')
    workbook = Workbook()
    worksheet = workbook.active

    # Escribe los datos en la hoja de cálculo
    for row in dataframe_to_rows(df, index=False, header=True):
        worksheet.append(row)

   
    excel_file = io.BytesIO()
    workbook.save(excel_file)
    excel_file.seek(0)

    # Crea la respuesta HTTP con el archivo de Excel
    response = make_response(excel_file.getvalue())
    response.headers.set('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response.headers.set('Content-Disposition', 'attachment', filename='manual_data.xlsx')

    return response

# Exportar a PDF
@app.route('/export_to_pdf/<so_value>')
def export_to_pdf(so_value):
    manual_data = ManualData.query.filter_by(so=so_value).first()
    comments = Comment.query.filter_by(so_id=manual_data.so).all()

    if manual_data:
        pdf_file = BytesIO()
        doc = SimpleDocTemplate(pdf_file, pagesize=letter, leftMargin=0*inch, rightMargin=0*inch, topMargin=0.2*inch, bottomMargin=0.5*inch)
        elements = []
        # Logo de NTT
        logo = Image('static/nttdata_logo.png', width=100, height=30)
        logo.hAlign = 'LEFT'
        elements.append(logo)

        # Crear una separación entre las tablas
        elements.append(Spacer(1, 12))


        # Tabla de datos
        table_data = [[column.name, getattr(manual_data, column.name)] for column in manual_data.__table__.columns]

        # Campos a eliminar
        fields_to_remove = ['responsible_name_edit', 'responsible_edited_at']

        # Eliminar los campos de la tabla de datos
        table_data = [[row[0], row[1]] for row in table_data if row[0] not in fields_to_remove]
         
        table = Table(table_data, colWidths=[200, 300])

        style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), '#007bff'),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 14),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 16),  
            ('LEFTPADDING', (0,0), (-1,-1), 2),  
            ('BACKGROUND', (0,1), (-1,-1), colors.white),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
        ])
        table.setStyle(style)

        elements.append(table)

        # Crear una separación entre las tablas
        elements.append(Spacer(1, 12))

        # Tabla de comentarios
        comment_table_data = [['Comentarios', 'Creado', 'Editado']]
        for comment in comments:
            comment_table_data.append([comment.comment, comment.created_at.strftime('%Y-%m-%d %H:%M:%S'), comment.edited_at.strftime('%Y-%m-%d %H:%M:%S') if comment.edited_at else ''])
        comment_table = Table(comment_table_data)
        comment_table_style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), '#007bff'),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 14),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.white),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
        ])
        comment_table.setStyle(comment_table_style)
        elements.append(comment_table)

        doc.build(elements)

        pdf_file.seek(0)
        response = make_response(pdf_file.getvalue())
        response.headers.set('Content-Type', 'application/pdf')
        response.headers.set('Content-Disposition', 'attachment', filename=f'So_{manual_data.so}.pdf')

        return response
    else:
        return "No se encontró ningún registro con el valor de 'so' proporcionado.", 404


# Ruta para imprimir
@app.route('/print_data', methods=['GET'])
def print_data():
    manual_data = ManualData.query.all()
    return render_template('print_data.html', manual_data=manual_data)

# Aging project
@app.route('/project_aging')
def project_aging():
    # Recupera todos los datos de la base de datos ordenados por fecha
    data = ManualData.query.order_by(ManualData.date).all()
    return render_template('project_aging.html', data=data)

#Flask Email
# @app.route('/enviar_correo/<string:sales_order>')
# def enviar_correo(sales_order):
    #  msg = Message('Nuevo SO ingresado', sender='antonio.castillodiaz014@outlook.com', recipients=['castillodiaz.antonio@gmail.com'])
    #  msg.body = f'Se ha ingresado una nueva orden de venta con el número: {sales_order}.'
#  mail.send(msg)

# Código para SSO AZURE AD 

#@app.route('/') 
#def index(): 
    if not session.get("user"): 
        return redirect(url_for("login")) 
    print(session["user"])
    #return f"Hello, {session['user']['name']}!" 
    return render_template('base.html', )

@app.route('/login') 
def login(): 
    session["state"] = os.urandom(24).hex() 
    auth_url = msal_app.get_authorization_request_url( 
        scopes=["user.read"],  # Cambiar según los permisos requeridos 
        state=session["state"], 
        redirect_uri=url_for("authorized", _external=True) 
    ) 
    return redirect(auth_url)

#@app.route(REDIRECT_PATH) 
#def authorized(): 
    if request.args.get('state') != session.get("state"): 
        return redirect(url_for("index"))  # Estado erróneo, posiblemente un ataque CSRF 
    result = msal_app.acquire_token_by_authorization_code( 
        code=request.args.get('code'), 
        scopes=["user.read"],  # Cambiar según los permisos requeridos 
        redirect_uri=url_for("authorized", _external=True) 
    ) 
    if "error" in result: 
        return f"Login failure: {result.get('error_description')}" 
    session["user"] = result.get("id_token_claims") 
    return redirect(url_for("index")) 


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    #app.run(debug=True)
    app.run(ssl_context="adhoc", debug=True)
    
