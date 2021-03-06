# -*- coding: utf-8 -*-
from trytond.model import ModelView, ModelSQL, ModelSingleton, fields

from dateutil.relativedelta import *#relativedelta
from datetime import * #datetime, date
from trytond.pool import Pool
from trytond.res import User
from trytond.pyson import Eval, If, DateTime

from perfil import *

#Clases asociadas a personas ------------------------
class Persona(ModelSQL,ModelView):
	'Persona'
	_name = 'cefiro.persona'
	_description = __doc__
	name = fields.Char('Nombre',required=True)
	cedula = fields.Char('C.I.',required=True)

Persona()

class Psicologo(Persona):
	'Psicologo'
	_name = 'cefiro.psicologo'
	_description = __doc__


	login = fields.Char('Nombre de usuario interno',required=True)
	password = fields.Function(fields.Char(u'Contraseña',required=True),'mensaje','crear')
	telefono = fields.Char(u'Teléfono')
	mail = fields.Char(u'Correo electrónico')
	pacientes = fields.Many2Many('cefiro.psicopac','psicologo','paciente','Pacientes')
	consultas = fields.Many2Many('cefiro.encuentropsi','persona','evento','Consultas')

	#Esto es para crear el usuario interno

	def mensaje(self,ids,name):
		res = {}
		for elem in self.browse(ids):
			res[elem.id] = "xxxxxxxxxxxxxxxxxxxx"
		return res

	def crear(self,ids,name,value):
		user_obj = Pool().get('res.user')
		for elem in self.browse(ids):
			yaCreados = user_obj.search([('login','=','elem.login')])
			if len(yaCreados)==0:
				user_obj.create({'name':elem.name,'login':elem.login,'password':value})
			else:
				user_obj.write(yaCreados,{'password':value})
					
		return
	#Fin de lo del usuario interno

Psicologo()


#Implemento una clase que maneje las secuencias numéricas a crear. Principalmente para tener un número de paciente definido automáticamente.
class Sec(ModelSingleton,ModelSQL,ModelView):
	'Sec'
	_name = 'cefiro.sec'
	_description = __doc__

	numeropaciente = fields.Property(fields.Many2One('ir.sequence',u'Número de Paciente', required=True,domain=[('code', '=', 'cefiro.paciente')]))

Sec()
#----------------------------------------------------------------------

class Paciente(Persona):
	'Paciente'
	_name = 'cefiro.paciente'
	_description = __doc__
	_rpc={'on_change_with_edad':True}
	#_rec_name = 'identidad'

	identidad = fields.Char('ID',readonly=True)

	def create(self, values):
		sequence_obj = Pool().get('ir.sequence')
		config_obj = Pool().get('cefiro.sec')

		values = values.copy()
		config = config_obj.browse(1)
		values['identidad'] = sequence_obj.get_id(config.numeropaciente.id)

	        return super(Paciente, self).create(values)


	sexo = fields.Selection([('M','Masculino'),('F','Femenino')],'Sexo')
	nacimiento = fields.Date('Fecha de Nacimiento')
	edad = fields.Function(fields.Char('Edad',depends=['nacimiento'],on_change_with=['nacimiento']),'get_edad')
	def on_change_with_edad(self,values):
		ahora = date.today()
		edadtemp = relativedelta(ahora,values.get('nacimiento'))
         	res = str(edadtemp.years)+u' años'
		return res
		

	telefono = fields.Char(u'Teléfono fijo') #Char por si hay telefonos internacionales, u otros símbolos
	celular = fields.Char(u'Teléfono celular') #Char por si hay códigos que no sean números
	#
	lista = fields.Many2Many('cefiro.listapac','paciente','lista','Lista de espera')
	#
	convenioSAPPA = fields.Selection([('f','Funcionario'),('c',u'Cónyuge'),('p',u'Padre/Madre'),('h',u'Hijo/a')],u'Relación para el convenio')
	lugarTrabajo = fields.Char('Lugar de trabajo')
	funcionario = fields.Char(u'Número de funcionario') #Lo pongo char por si hay letras
	#
	atencionMedica = fields.Selection([('msp',u'MSP/ASSE'),('mut','Mutualista')],u'Tipo de Atención Médica')
	mutualista = fields.Char('Nombre de la Mutualista')
	#
	fechaIngresoExpediente = fields.Date('Fecha de ingreso del expediente')
	motivo = fields.Text('Motivo de Consulta')
	observaciones = fields.Text('Observaciones')
	#	
	horarioPref = fields.Char('Horario de Preferencia')
	psicologo = fields.Many2Many('cefiro.psicopac','paciente','psicologo',u'Psicólogo')
	consultas = fields.Many2Many('cefiro.encuentro','persona','evento','Consultas')
	#
	#Formularios entregados para el SAPPA
	form_OQ45T1 = fields.Boolean(u'OQ45-T1')
	form_OQ45T2 = fields.Boolean(u'OQ45-T2')
	form_EncuestaSatisfaccion = fields.Boolean(u'Encuesta de Satisfacción')
	form_EcuestaSatPExtProfesional = fields.Boolean(u'Encuesta de Satisfacción - Prof. Externo : Profesional')
	form_EncuestaSatPExtPaciente = fields.Boolean(u'Encuesta de Satisfacción - Prof. Externo: Paciente')
	#
	profExternoDerivacion = fields.Boolean('Derivado a profesional externo')
	profExternoNombre = fields.Char('Nombre del profesional externo')
	profExternoFecha = fields.Date(u'Fecha de derivación')

	#Cálculo de la edad
	def get_edad(self,ids,name):
		#usu = User()
		#usu.create([('name','pruebalala'),('login','loolololo')])
		ahora = date.today()
		res = {}
        	for pac in self.browse(ids):
			edadtemp = relativedelta(ahora,pac.nacimiento)
            		res[pac.id] = str(edadtemp.years)+u' años'
        	return res

	#Ahora agrego la parte de historias clínicas
	formularioInicial = fields.One2Many('cefiro.formulario','paciente','Formulario Inicial')

	informesSesion = fields.One2Many('cefiro.sesion','paciente',u'Informes de Sesión')
	formularioFinal = fields.One2Many('cefiro.final','paciente',u'Formularios de Fin de Intevención')

Paciente()


#Clases auxiliares para Paciente

class PsicoPac(ModelSQL):
	'PsicoPac'
	_name = 'cefiro.psicopac'
	_description = __doc__
	psicologo = fields.Many2One('cefiro.psicologo',u'Psicólogo(s)',select=1)
	paciente = fields.Many2One('cefiro.paciente','Pacientes',select=1)

PsicoPac()

#class PacienteFormulario(ModelSQL):
#	'PacienteFormulario'
#	_name = 'cefiro.pacienteformulario'
#	_description = __doc__
#
#	paciente = fields.Many2One('cefiro.paciente','Paciente',select=1,)
#	formulario = fields.Many2One('cefiro.formulario','Formulario Inicial',select=1)
#
#PacienteFormulario()

#--------------------------------------------------------------------------------------



class Estudiante(Persona):
	'Estudiante'
	_name = 'cefiro.estudiante'
	_description = __doc__
	telefono = fields.Char(u'Teléfono')
	mail = fields.Char(u'Correo electrónico')
	consultas = fields.Many2Many('cefiro.encuentroest','persona','evento','Consultas')

Estudiante()
#--------------------------------------------------------------------------------------

#Clases asociadas a lugares ------------------------

class Consultorio(ModelSQL,ModelView):
	'Consultorio'
	_name = 'cefiro.consultorio'
	_description = __doc__
	name = fields.Char('Nombre')
	consultas = fields.One2Many('cefiro.consulta','consultorio','Consultas')
	ocupado = fields.DateTime(u'fecha de ocupación') #debug

Consultorio()
#--------------------------------------------------------------------------------------


#Clase Consulta-------------------------------------
class Consulta(ModelSQL,ModelView):
	'Consulta'
	_name = 'cefiro.consulta'
	_description = __doc__
	_rec_name = 'horaini'

	name = fields.Char('Nombre')

	#num = 1
	#idN = fields.Function(fields.Integer('ID'),'get_id')
	#def get_id(self,ids,name):
	#	res = {}
	#	for elem in self.browse(ids):
	#		res[elem.id] = self.num
	#	self.num = self.num + 1
	#	return res

	

	libres=[]

	psicologos = fields.Many2Many('cefiro.encuentropsi','evento','persona',u'Psicólogos')
	pacientes = fields.Many2Many('cefiro.encuentro','evento','persona','Pacientes')	
	estudiantes = fields.Many2Many('cefiro.encuentroest','evento','persona','Estudiantes')

	#informe = fields.One2One('cefiro.consultainforme','consulta','informe','Informe')

	horaini = fields.DateTime('Fecha y hora de inicio',required=True)
	horaFin = fields.DateTime('Fecha y hora de fin',required=True)

	consulLibres = fields.Function(fields.One2Many('cefiro.consultorio',None,'Consultorios libres',on_change_with=['horaini','horaFin']),'get_libres')

	consultorio = fields.Many2One('cefiro.consultorio','Consultorio',required=True,domain=[('id','in',Eval('consulLibres'))])

	def get_libres(self,ids,name):
		res = {}
		objConsul = Pool().get('cefiro.consultorio')
		for elem in self.browse(ids):
			res[elem.id] = elem.libres
		return res


	def on_change_with_consulLibres(self,values):
		objConsultorio = Pool().get('cefiro.consultorio')
		objConsulta = Pool().get('cefiro.consulta')
		consultoriosTotId = objConsultorio.search([])
		res=[]
		for cons in objConsultorio.browse(consultoriosTotId):
			estaVacio = True
			consultasIDs = cons.consultas
			
			listaDic = objConsulta.read(consultasIDs)
			for dic in listaDic:
				i1 = values.get('horaini')
				f1 = values.get('horaFin')
				i2=dic.get('horaini')
				f2=dic.get('horaFin')
				if not ((i1==None) or (f1==None)):
					if not((f2<i1) or (f1<i2)):
						estaVacio = False
			if estaVacio:
				res.append(cons.id)

		self.libres = res		

		return res


Consulta()

#Clases auxiliares para Consulta
class Encuentro(ModelSQL):
	'Encuentro'
	_name = 'cefiro.encuentro'
	_description = __doc__
	persona = fields.Many2One('cefiro.paciente','Pacientes',select=1)
	evento = fields.Many2One('cefiro.consulta','Consultas',select=1)

Encuentro()

class EncuentroPsi(ModelSQL):
	'EncuentroPsi'
	_name = 'cefiro.encuentropsi'
	_description = __doc__
	persona = fields.Many2One('cefiro.psicologo',u'Psicólogos',select=1)
	evento = fields.Many2One('cefiro.consulta','Consultas',select=1)

EncuentroPsi()

class EncuentroEst(ModelSQL):
	'EncuentroEst'
	_name = 'cefiro.encuentroest'
	_description = __doc__
	persona = fields.Many2One('cefiro.estudiante','Estudiantes',select=1)
	evento = fields.Many2One('cefiro.consulta','Consultas',select=1)

EncuentroEst()

#class ConsultaInforme(ModelSQL):
#	'ConsultaInforme'
#	_name = 'cefiro.consultainforme'
#	_description = __doc__
#
#	consulta = fields.Many2One('cefiro.consulta','Consulta',select=1)
#	informe = fields.Many2One('cefiro.sesion',u'Informe de sesión',select=1)
#
#ConsultaInforme()
#--------------------------------------------------------------------------------------

#Clases auxiliares para Psicólogo
class PsicoUsuario(ModelSQL):
	'PsicoUsuario'
	_name = 'cefiro.psicousuario'
	_description = __doc__
	#psicologo = Psicologo()
	#usuario = User()
	psicologo = fields.Many2One('cefiro.psicologo',u'Psicólogo',select=1)
	usuario = fields.Many2One('res.user','Usuario',select=1)

PsicoUsuario()
#--------------------------------------------------------------------------------------

class Reserva(ModelSQL,ModelView):
	'Reserva'
	_name = 'cefiro.reserva'
	

	horaIni = fields.DateTime('Fecha y hora de inicio')
	horaFin = fields.DateTime('Fecha y hora de fin')
	consulLibres = fields.Function(fields.One2Many('cefiro.consultorio',None,'Consultorios libres',on_change_with=['horaIni','horaFin']),'get_libres')
	consultorio = fields.Many2One('cefiro.consultorio','Consultorio',required=True,domain=[('name','=','Consultorio 9')])

	def get_libres(self,ids,name):
		res = {}
		objConsul = Pool().get('cefiro.consultorio')
		consultorio_ids = objConsul.search([('name','=','Consultorio 9')])
		for elem in self.browse(ids):
			res[elem.id] = []
			if consultorio_ids:
				res[elem.id].extend(consultorio_ids)
		return res


	def on_change_with_consulLibres(self,values):
		objConsul = Pool().get('cefiro.consultorio')
		res = objConsul.search([('name','=','Consultorio 9')])
		return res

Reserva()


