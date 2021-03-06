# -*- coding: utf-8 -*-
from trytond.model import ModelView, ModelSQL, ModelSingleton, fields

from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from trytond.pool import Pool
from trytond.res import User
from trytond.pyson import Eval, If, Bool, Equal, Not, And, Or

from cefiro import *

#def  __init__(self):
#	super(Formulario, self).__init__()
    #self._error_messages.update({
        #'alumnos_out': 'No se pueden agregar mas alumnos. Numero de asientos!',
    #})

    #self._transitions |= set((      # Si existe te lo reescribe. NO podes tener una transition repetida
        #('draft', 'confirmed'),   # (origen, destino)
        #('confirmed', 'done'),  # Podria tener la de (done,confirmed)
        #('done', 'cancel'),
        #))

	#self._transitions.update({
	#	'derivador': {  ## Nombre del field. Nombre de la function
	#		'invisible': ~Eval('tipoConsulta').in_(['der']),
		#},
	#})

class Formulario(ModelSQL,ModelView):
	'Formulario'
	_name = 'cefiro.formulario'
	_description = __doc__
	_rec_name = 'fecha'
	#_history = True
#	name = fields.Char('Nombre del paciente')
	#Paciente Asociado y datos autocompletados. Implementar esto. Tema de las edades (el paciente tiene una edad actual, y va yendo a consultas con distintas edades).
	paciente = fields.Many2One('cefiro.paciente','Paciente')

	#name = fields.Char('Name', required=True)

	#Tipo de consulta
	fecha = fields.Date('Fecha de consulta inicial',required=True)

	tipoConsulta = fields.Selection([('esp',u'Consulta espontánea'),('tra',u'Traído'),('ori',u'Consulta por orientación'),('der','Derivado')],'Tipo de Consulta',required=True) #['tipoConsulta', 'in', ('ori','tra','esp')] Auto completar este dato [('special_deduction_type', '!=', 'bank')]

	derivador = fields.Selection([('med',u'Especialidad Médica'),('psiq','Psiquiatra'),('edu',u'Institución Educativa'),('otra','Otra')],'Derivado por', states={'invisible': Not(Equal(Eval('tipoConsulta'), 'der')),'required': Equal(Eval('tipoConsulta'), 'der')},domain=[('der','=',Eval('tipoConsulta'))]) #states={'readonly': "state != 'draft'" #Equal(Eval('state'), 'draft')) 
    #Not(Equal(Eval('tipoConsulta'), 'der'))
#	def default_derivador(self):
#		return 'med'
	derivEspec = fields.Char('Especifique',

		states={'invisible': Not(Equal(Eval('derivador'), 'otra')),'required': Equal(Eval('derivador'), 'otra')}) #states={'readonly': "state != 'draft'" #Equal(Eval('state'), 'draft')) 


	acompanante = fields.Selection([('sol','Solo'),('ami',u'Amigo/a'),('mad',u'Madre'),('pad','Padre'),('paj','Pareja'),('amb','Ambos padres'),('par','Pariente'),('otr','Otros')],u'Acompañante',required=True)

	#Motivo de consulta
	motivoPaciente1 = fields.Char(u'Motivo según el paciente (1)',required=True)
	motivoPaciente1Cod = fields.Char(u'Código',required=True)
	motivoPaciente2 = fields.Char(u'Motivo según el paciente (2)')
	motivoPaciente2Cod = fields.Char(u'Código')
	motivoPaciente3 = fields.Char(u'Motivo según el paciente (3)')
	motivoPaciente3Cod = fields.Char(u'Código')

	motivoAcompa1 = fields.Char(u'Motivo según el Acompañante (1)')
	motivoAcompa1Cod = fields.Char(u'Código')
	motivoAcompa2 = fields.Char(u'Motivo según el Acompañante (2)')
	motivoAcompa2Cod = fields.Char(u'Código')
	motivoAcompa3 = fields.Char(u'Motivo según el Acompañante (3)')
	motivoAcompa3Cod = fields.Char(u'Código')

	motivoPsico1 = fields.Char(u'Motivo según el Psicólogo (1)',required=True)
	motivoPsico1Cod = fields.Char(u'Código',required=True)
	motivoPsico2 = fields.Char(u'Motivo según el Psicólogo (2)')
	motivoPsico2Cod = fields.Char(u'Código')
	motivoPsico3 = fields.Char(u'Motivo según el Psicólogo (3)')
	motivoPsico3Cod = fields.Char(u'Código')

	motivoComplementaria = fields.Text(u'Descripción Comlpementaria')

	#Datos personales extra
	lugarNacimiento = fields.Char('Lugar de Nacimiento')

	#########################
	### Vivienda y Trabajo ##
	#########################

	#formVivTrabajo = fields.One2One('cefiro.formVivTrabajo','formulario','id','Vivienda y Trabajo')
	#formVivTrabajo = fields.One2One('cefiro.formvivtrabajo','formvivtrabajoid','formularioid', 'Vivienda y Trabajo', required=True)
	formularioViviendaTrabajo = fields.One2One('cefiro.auxformvivtrabajo','formulario','formvt','Formvt')

	#####################
	##### Educación #####
	#####################

	## Edu formal ##
#	eduFormal = fields.Boolean(u'Educación Formal')

	eduFormalNivel = fields.Selection([('no','No escolarizado'),('priInc','Primaria Incompleta'),('pri','Primaria Completa'),('secInc','Secundaria Incompleta'),('sec','Secundaria Completa'),('tercInc','Terciaria Incompleta'),('terc','Terciaria Completa'),('uniInc','Universitaria Incompleta'),('uni','Universitaria Completa')],u'Nivel de Educación Formal',required=True)
	eduFormalNivelMax = fields.Integer(


u'Máximo año aprobado (en caso de no haber completado lo último que estudió)'

,states={'invisible': Not(Or(Equal(Eval('eduFormalNivel'),'priInc'),Equal(Eval('eduFormalNivel'),'secInc'),Equal(Eval('eduFormalNivel'),'tercInc'),Equal(Eval('eduFormalNivel'),'uniInc'))),

'required': 

		Or(
			Equal(Eval('eduFormalNivel'),'priInc'),
			Equal(Eval('eduFormalNivel'),'secInc'),
			Equal(Eval('eduFormalNivel'),'tercInc'),
			Equal(Eval('eduFormalNivel'),'uniInc')
		)
	}
	) #states={'invisible': Equal(Eval('eduFormalNivel'), 'no')}

	## Edu primaria ##
#	eduPrimaria = fields.Boolean(u'Educación Primaria')
	eduCentrosPrimaria = fields.Char(u'Centros en los que estudió',

		states={'required': 
									Or(
										Equal(Eval('eduFormalNivel'),'pri'),
										Equal(Eval('eduFormalNivel'),'sec'),
										Equal(Eval('eduFormalNivel'),'terc'),
										Equal(Eval('eduFormalNivel'),'uni'),

										Equal(Eval('eduFormalNivel'),'priInc'),
										Equal(Eval('eduFormalNivel'),'secInc'),
										Equal(Eval('eduFormalNivel'),'tercInc'),
										Equal(Eval('eduFormalNivel'),'uniInc')

									)})
		#,states={'invisible': Not(Equal(Eval('eduFormalNivel'),'pri'))})
		#,states={'invisible': Not(Bool(Eval('eduPrimaria')))})
	
	eduPubliPrimaria = fields.Selection([('publi',u'Pública'),('priv','Privada')],u'Tipo de institución',
		states={'required': 
									Or(
										Equal(Eval('eduFormalNivel'),'pri'),
										Equal(Eval('eduFormalNivel'),'sec'),
										Equal(Eval('eduFormalNivel'),'terc'),
										Equal(Eval('eduFormalNivel'),'uni'),

										Equal(Eval('eduFormalNivel'),'priInc'),
										Equal(Eval('eduFormalNivel'),'secInc'),
										Equal(Eval('eduFormalNivel'),'tercInc'),
										Equal(Eval('eduFormalNivel'),'uniInc')
									)})
	eduDifPrimaria = fields.Boolean(u'Presentó dificultades de aprendizaje')
	eduDifTipoPrimaria = fields.Char(u'Tipo de dificultad que presentó',
		states={'required': 

								And(
									Or(
										Equal(Eval('eduFormalNivel'),'pri'),
										Equal(Eval('eduFormalNivel'),'sec'),
										Equal(Eval('eduFormalNivel'),'terc'),
										Equal(Eval('eduFormalNivel'),'uni'),

										Equal(Eval('eduFormalNivel'),'priInc'),
										Equal(Eval('eduFormalNivel'),'secInc'),
										Equal(Eval('eduFormalNivel'),'tercInc'),
										Equal(Eval('eduFormalNivel'),'uniInc')
									),
									Bool(Eval('eduDifPrimaria'))
								),
			'invisible':
				Not(Bool(Eval('eduDifPrimaria')))
	})	
	eduRepePrimaria = fields.Integer(u'Cantidad de años repetidos (si no hay dejar vacío)')
	eduRepeCausaPrimaria = fields.Char(u'Causa de la repetición de años',
			states={'required': 
							And(
									Or(
										Equal(Eval('eduFormalNivel'),'pri'),
										Equal(Eval('eduFormalNivel'),'sec'),
										Equal(Eval('eduFormalNivel'),'terc'),
										Equal(Eval('eduFormalNivel'),'uni'),

										Equal(Eval('eduFormalNivel'),'priInc'),
										Equal(Eval('eduFormalNivel'),'secInc'),
										Equal(Eval('eduFormalNivel'),'tercInc'),
										Equal(Eval('eduFormalNivel'),'uniInc')

									),
									Bool(Eval('eduRepePrimaria'))
							),
					'invisible': 
						Not(Bool(Eval('eduRepePrimaria')))

					}
			)
	eduDeserPrimaria = fields.Boolean(u'Deserción o Exclusión')
	
	## Edu secundaria
#	eduSecundaria = fields.Boolean(u'Educación Secundaria')
	eduCentrosSecundaria = fields.Char(u'Centros en los que estudió',
				states={'required': 
									Or(
										Equal(Eval('eduFormalNivel'),'sec'),
										Equal(Eval('eduFormalNivel'),'terc'),
										Equal(Eval('eduFormalNivel'),'uni'),

										Equal(Eval('eduFormalNivel'),'secInc'),
										Equal(Eval('eduFormalNivel'),'tercInc'),
										Equal(Eval('eduFormalNivel'),'uniInc')
				)})
		 #,states={'invisible': Not(Bool(Eval('eduSecundaria')))})
	eduPubliSecundaria = fields.Selection([('publi',u'Pública'),('priv','Privada')],u'Tipo de institución',
				states={'required': 
									Or(
										Equal(Eval('eduFormalNivel'),'sec'),
										Equal(Eval('eduFormalNivel'),'terc'),
										Equal(Eval('eduFormalNivel'),'uni'),

										Equal(Eval('eduFormalNivel'),'secInc'),
										Equal(Eval('eduFormalNivel'),'tercInc'),
										Equal(Eval('eduFormalNivel'),'uniInc')
				)})
	eduDifSecundaria = fields.Boolean(u'Presentó dificultades de aprendizaje')
	eduDifTipoSecundaria = fields.Char(u'Tipo de dificultad que presentó',
				states={'required': 
							And(
									Or(
										Equal(Eval('eduFormalNivel'),'sec'),
										Equal(Eval('eduFormalNivel'),'terc'),
										Equal(Eval('eduFormalNivel'),'uni'),

										Equal(Eval('eduFormalNivel'),'secInc'),
										Equal(Eval('eduFormalNivel'),'tercInc'),
										Equal(Eval('eduFormalNivel'),'uniInc')
									),
								Bool(Eval('eduDifSecundaria'))
							),

		                        'invisible':
                		                Not(Bool(Eval('eduDifSecundaria')))

				})
	eduRepeSecundaria = fields.Integer(u'Cantidad de años repetidos (si no hay dejar vacío)')
	eduRepeCausaSecundaria = fields.Char(u'Causa de la repetición de años',
				states={'required': 
								And(
									Or(
										Equal(Eval('eduFormalNivel'),'sec'),
										Equal(Eval('eduFormalNivel'),'terc'),
										Equal(Eval('eduFormalNivel'),'uni'),

										Equal(Eval('eduFormalNivel'),'secInc'),
										Equal(Eval('eduFormalNivel'),'tercInc'),
										Equal(Eval('eduFormalNivel'),'uniInc')
									),
									Bool(Eval('eduRepeSecundaria'))
								),
						'invisible': 
								Not(Bool(Eval('eduRepeSecundaria')))
						})
	
	eduDeserSecundaria = fields.Boolean(u'Deserción o Exclusión')

	## Edu terciaria
	eduCentrosTerciaria = fields.Char(u'Centros en los que estudió',
							states={'required': 
									Or( Equal(Eval('eduFormalNivel'),'terc'),
										Equal(Eval('eduFormalNivel'),'tercInc')
									)
							})
	eduPubliTerciaria = fields.Selection([('publi',u'Pública'),('priv','Privada')],u'Tipo de institución',
							states={'required': 
									Or( Equal(Eval('eduFormalNivel'),'terc'),
										Equal(Eval('eduFormalNivel'),'tercInc')
									)
							})

	eduCentrosUniv = fields.Char(u'Centros en los que estudió',
							states={'required': 
									Or( Equal(Eval('eduFormalNivel'),'uni'),
										Equal(Eval('eduFormalNivel'),'uniInc')
									)
							})
	eduPubliUniv = fields.Selection([('publi',u'Pública'),('priv','Privada')],u'Tipo de institución',
				states={'required': 
						Or(
							Equal(Eval('eduFormalNivel'),'uni'),
							Equal(Eval('eduFormalNivel'),'uniInc')
						)})		

	## Edu no formal
	#eduNoFormal = fields.Boolean(u'Educación No Formal')
	eduNoFormal = fields.Selection([('si','Si'),('no','No')],u'EDUCACION NO FORMAL')
	eduNoForCurso1 = fields.Char('Curso',
				states = {'required': Equal(Eval('eduNoFormal'),'si')})
	eduNoForCentro1 = fields.Char('Centro',
				states = {'required': Equal(Eval('eduNoFormal'),'si')})
	eduNoForPubli1 = fields.Selection([('publi',u'Pública'),('priv','Privada')],u'Tipo de institución',
				states = {'required': Equal(Eval('eduNoFormal'),'si')})
	eduNoForAsis1 = fields.Selection([('actual','Asiste'),('pasado',u'Asistió')],'Momento',
				states = {'required': Equal(Eval('eduNoFormal'),'si')})
	eduNoForCurso2 = fields.Char('Curso')
	eduNoForCentro2 = fields.Char('Centro')
	eduNoForPubli2 = fields.Selection([('publi',u'Pública'),('priv','Privada')],u'Tipo de institución')
	eduNoForAsis2 = fields.Selection([('actual','Asiste'),('pasado',u'Asistió')],'Momento')

	eduNoForCurso3 = fields.Char('Curso')
	eduNoForCentro3 = fields.Char('Centro')
	eduNoForPubli3 = fields.Selection([('publi',u'Pública'),('priv','Privada')],u'Tipo de institución')
	eduNoForAsis3 = fields.Selection([('actual','Asiste'),('pasado',u'Asistió')],'Momento')

	### Edu familiar
	eduPadre = fields.Selection([('no','No escolarizado'),('priInc','Primaria Incompleta'),('pri','Primaria Completa'),('secInc','Secundaria Incompleta'),('sec','Secundaria Completa'),('tercInc','Terciaria Incompleta'),('terc','Terciaria Completa'),('uniInc','Universitaria Incompleta'),('uni','Universitaria Completa')],u'Nivel de Educación Formal del Padre')
	eduMadre = fields.Selection([('no','No escolarizado'),('priInc','Primaria Incompleta'),('pri','Primaria Completa'),('secInc','Secundaria Incompleta'),('sec','Secundaria Completa'),('tercInc','Terciaria Incompleta'),('terc','Terciaria Completa'),('uniInc','Universitaria Incompleta'),('uni','Universitaria Completa')],u'Nivel de Educación Formal de la Madre')
	eduPareja = fields.Selection([('no','No escolarizado'),('priInc','Primaria Incompleta'),('pri','Primaria Completa'),('secInc','Secundaria Incompleta'),('sec','Secundaria Completa'),('tercInc','Terciaria Incompleta'),('terc','Terciaria Completa'),('uniInc','Universitaria Incompleta'),('uni','Universitaria Completa')],u'Nivel de Educación Formal de la Pareja')

	########################
	##### Discapacidad #####
	########################

	# 1) En cuales de las siguientes areas tiene esta persona limitaciones?
	limVisual = fields.Boolean('VISUAL')
	limAuditiva = fields.Boolean('AUDITIVA')
	limMental = fields.Boolean('MENTAL')
	limIntelectual = fields.Boolean('INTELECTUAL')
	limFisicoMotoras = fields.Boolean('FISICO-MOTORAS')
	limVisceral = fields.Boolean('VISCERAL')

	# 2) Su deficiencia es:

	deficiencia = fields.Selection([('con',u'Congénita'),('adq','Adquirida'),('amb','Ambas'),('ns','NS/NC')],'Deficiencia') # Si es congenita ir a la pregunta (numero 6 del formulario)

	# 3) Cual fue el determinante de la discapacidad?

	deterDisc = fields.Selection([('acdom',u'Accidente doméstico/deportivo'),('actra','Accidente de trabajo'),('par','Problemas de Parto'),('vio','Violencia'),('desnat','Desastres naturales'),('actrans',u'Accidentes de tránsito'),('int',u'Intoxicación química'),('trasnut','Trastornos nutricionales'),('pat',u'Patología'),('otros','Otros')],u'¿Cuál fue el determinante de la discapacidad?', states = {'invisible': Equal(Eval('deficiencia'),'con')}) 
	otroDeterDisc = fields.Char('Especifique',states = {'invisible': 
		Not(Equal(Eval('deterDisc'),'otros'))
	})

	# 4) A que edad manifesto la discapacidad?

#	edadManDisc = fields.Selection([('menosuno',u'Menos de 1 año'),('unoacuatro',u'1-4 Años'),('cincoadiez',u'5-10 años'),('diezacatorce',u'10-14 años'),('quinceadiecinueve',u'15-19 años'),('veinteaveinticuatro',u'20-24 años'),('veinticincoaveintinueve',u'25-29 años'),('treintatreintaicuatro',u'30-34 años'),('treintaicincoatreintainueve',u'35-39 años'),('cuarentacuarentaicuatro',u'40-44 años'),('cuarentaicincoacuarentainueve',u'45-49 años'),('cincuentacincuentaicuatro',u'50-54 años'),('cincuentaicincoasesenta',u'55-60 años'),('sesentasesentaicuatro',u'60-64 años'),('mayorsesentaicinco',u'Más de 65 años'),('ns',u'NS/NC')],u'¿A qué edad se manifestó la discapacidad?')
	edadManDisc = fields.Selection([('menor1',u'Menos de 1 año'),('1a4',u'01-04 años'),('5a10',u'05-10 años'),('10a14',u'10-14 años'),('15a19',u'15-19 años'),('20a24',u'20-24 años'),('25a29',u'25-29 años'),('30a34',u'30-34 años'),('35a39',u'35-39 años'),('40a44',u'40-44 años'),('45a49',u'45-49 años'),('50a54',u'50-54 años'),('55a60',u'55-60 años'),('60a64',u'60-64 años'),('mayor65',u'Más de 65 años'),('ns',u'NS/NC')],u'¿A qué edad se manifestó la discapacidad?',states = {'invisible': Equal(Eval('deficiencia'),'con')}) 

	# 5) Conoce el diagnostico especifico de la discapacidad?

	diagEspec = fields.Selection([('si',u'Sí'),('no','No')],u'¿Conoce el diagnóstico específico de la discapacidad?')

	# 6) Cual fue el diagnostico que le dijeron?

	diaDijeron = fields.Text(u'¿Cuál fue el diagnóstico que le dijeron?',states = {'invisible': Equal(Eval('diagEspec'),'no')})

	# 7) Diagnóstico Medico (si tienen papel que lo corrobore)

	diagMedico = fields.Selection([('si',u'Sí'),('no','No')],u'Diagnóstico Médico',states = {'invisible': Equal(Eval('diagEspec'),'no')})

	# 8) Cual es el diagnostico que indica el papel del medico?


	diagPapelMedico = fields.Text(u'¿Cuál es el diagnóstico que indica el papel del médico?',states = {'invisible': Or(And(Or(Equal(Eval('diagMedico'),'no'),Not(Equal(Eval('diagMedico'),'si'))),Not(Equal(Eval('diagEspec'),'no'))),Equal(Eval('diagEspec'),'no'))})

	# 9) Dada su dificultad, ¿utiliza algun dispositivo de apoyo?

	disApoyo = fields.Selection([('si',u'Sí'),('no','No')],u'Dada su dificultad, ¿utiliza algún dispositivo de apoyo?')

	#10) Que dispositivo utiliza dada su dificultad?

	anAdcr = fields.Boolean('Andador adulto con ruedas')
	anAdsr = fields.Boolean('Andador adulto sin ruedas')
	anIncr = fields.Boolean('Andador infantil con ruedas')
	anInsr = fields.Boolean('Andador infantil sin ruedas')	

	bVer = fields.Boolean(u'Bastón Verde')
	bBl = fields.Boolean(u'Bastón Blanco')
	bCa = fields.Boolean('Bastones Canadienses')

	cPosAd = fields.Boolean('Coche Postural Adulto')
	cPosIn = fields.Boolean('Coche Postural Infantil')

	pAd = fields.Boolean(u'Pañal Adulto')
	pIn = fields.Boolean(u'Pañal Infantil')

	fil = fields.Boolean('Filtro')

	telesc = fields.Boolean('Telescopio')
	lupa = fields.Boolean('Lupa')

	audif = fields.Boolean(u'Audífono')

	guin =  fields.Boolean('Guinche')

	violin = fields.Boolean(u'Violín')

	sBaEv = fields.Boolean(u'Silla para bañarse y evacuar')

	bUnPto = fields.Boolean(u'Bastón de 1 punto')

	btrecuaPtos = fields.Boolean(u'Bastón de 3 o 4 puntos')

	bRa = fields.Boolean(u'Bastón de rastreo')

	colAnti = fields.Boolean(u'Colchón Antiescaras')

	prote = fields.Boolean(u'Prótesis')
	
	almAnti = fields.Boolean(u'Almohadón Antiescaras')
	sRA = fields.Boolean('Silla de ruedas adulto')
	sRI = fields.Boolean('Silla de ruedas infantil')

	otroDisp = fields.Boolean('Otro')
	otroEspec = fields.Char('Especifique',states = {'invisible': Not(Bool(Eval('otroDisp')))})

	# 11) Es beneficiario/a de alguna prestacion social por discapacidad?
	benPrestaSocial = fields.Boolean(u'¿Es beneficiario/a de alguna prestación social por discapacidad?')

	# 12) Indique cual en caso de contestar si
	penoCon = fields.Boolean(u'Pensión no contributiva')
	jubincap = fields.Boolean(u'Jubilación por incapacidad')
	asigdob = fields.Boolean(u'Asignación doble')
	ayesbps = fields.Boolean('Ayuda especial BPS')
	asiPsC = fields.Boolean('Asistente Personal/Sistema de ciudados')
	tutMil = fields.Boolean('Tutela Militar')
	sPol = fields.Boolean('Sanidad Policial')
	otrBenDisc = fields.Boolean('Otro')
	otroBenDiscEspec = fields.Char('Especifique',states = {'invisible': Not(Bool(Eval('otrBenDisc')))})

	########################
	##### Antecedentes #####
	########################

	intAnt = fields.Boolean('Intervenciones anteriores')

	antPedagogica = fields.Selection([('conc',u'Concluida'),('aba','Abandonada'),('cur','En Curso')],u'Intervención Pedagógica')
	antPedagogicaPocas = fields.Boolean('Menos de 3 consultas')
	antPedagogicaMeses = fields.Integer(u'Duración en meses')
	antPedagogicaMedicacion = fields.Boolean(u'Medicación')
	antPedagogicaMedTipo = fields.Selection([('ansiolitico',u'Ansiolíticos'),('antidepre','Antidepresivos'),('neurolep',u'Neurolépticos'),('otro','Otros')],u'Tipo de Medicación')
	antPedagogicaObs = fields.Char(u'Motivo y Obs.')

	antMedica = fields.Selection([('conc',u'Concluida'),('aba','Abandonada'),('cur','En Curso')],u'Intervención Médica')
	antMedicaPocas = fields.Boolean('Menos de 3 consultas')
	antMedicaMeses = fields.Integer(u'Duración en meses')
	antMedicaMedicacion = fields.Boolean(u'Medicación')
	antMedicaMedTipo = fields.Selection([('ansiolitico',u'Ansiolíticos'),('antidepre','Antidepresivos'),('neurolep',u'Neurolépticos'),('otro','Otros')],u'Tipo de Medicación')
	antMedicaObs = fields.Char(u'Motivo y Obs.')

	antPsicologica = fields.Selection([('conc',u'Concluida'),('aba','Abandonada'),('cur','En Curso')],u'Intervención Psicológica')
	antPsicologicaPocas = fields.Boolean('Menos de 3 consultas')
	antPsicologicaMeses = fields.Integer(u'Duración en meses')
	antPsicologicaMedicacion = fields.Boolean(u'Medicación')
	antPsicologicaMedTipo = fields.Selection([('ansiolitico',u'Ansiolíticos'),('antidepre','Antidepresivos'),('neurolep',u'Neurolépticos'),('otro','Otros')],u'Tipo de Medicación')
	antPsicologicaObs = fields.Char(u'Motivo y Obs.')

	antPsiquiatrica = fields.Selection([('conc',u'Concluida'),('aba','Abandonada'),('cur','En Curso')],u'Intervención Psiquiátrica')
	antPsiquiatricaPocas = fields.Boolean('Menos de 3 consultas')
	antPsiquiatricaMeses = fields.Integer(u'Duración en meses')
	antPsiquiatricaMedicacion = fields.Boolean(u'Medicación')
	antPsiquiatricaMedTipo = fields.Selection([('ansiolitico',u'Ansiolíticos'),('antidepre','Antidepresivos'),('neurolep',u'Neurolépticos'),('otro','Otros')],u'Tipo de Medicación')
	antPsiquiatricaObs = fields.Char(u'Motivo y Obs.')

	antPsiqInter = fields.Selection([('conc',u'Concluida'),('aba','Abandonada'),('cur','En Curso')],u'Internación Psiquiátrica')
	antPsiqInterPocas = fields.Boolean('Menos de 3 consultas')
	antPsiqInterMeses = fields.Integer(u'Duración en meses')
	antPsiqInterMedicacion = fields.Boolean(u'Medicación')
	antPsiqInterMedTipo = fields.Selection([('ansiolitico',u'Ansiolíticos'),('antidepre','Antidepresivos'),('neurolep',u'Neurolépticos'),('otro','Otros')],u'Tipo de Medicación')
	antPsiqInterObs = fields.Char(u'Motivo y Obs.')

	antIntOtra = fields.Selection([('conc',u'Concluida'),('aba','Abandonada'),('cur','En Curso')],u'Otra')
	antIntOtraPocas = fields.Boolean('Menos de 3 consultas')
	antIntOtraMeses = fields.Integer(u'Duración en meses')
	antIntOtraMedicacion = fields.Boolean(u'Medicación')
	antIntOtraMedTipo = fields.Selection([('ansiolitico',u'Ansiolíticos'),('antidepre','Antidepresivos'),('neurolep',u'Neurolépticos'),('otro','Otros')],u'Tipo de Medicación')
	antIntOtraObs = fields.Char(u'Motivo y Obs.')

	antAsma = fields.Boolean(u'Asma')
	antEpilepsia = fields.Boolean(u'Epilepsia')
	antDiabetes = fields.Boolean(u'Diabetes')
	antTiroides = fields.Boolean(u'Enf. Tiroidea')
	antCancer = fields.Boolean(u'Cáncer')
	antVIH = fields.Boolean(u'VIH/SIDA')
	antOsteo = fields.Boolean(u'Pat. Osteoarticular')
	antCardio = fields.Boolean(u'Enf. Cardiovascular')

	accicirusino = fields.Boolean(u'¿Ha tenido algún accidente y/o cirugía?')
	antAccidente1Edad = fields.Integer('Edad')
	antAccidente1Tipo = fields.Char('Tipo')
	antAccidente2Edad = fields.Integer('Edad')
	antAccidente2Tipo = fields.Char('Tipo')
	antCirugia1Edad = fields.Integer('Edad')
	antCirugia1Tipo = fields.Char('Tipo')
	antCirugia2Edad = fields.Integer('Edad')
	antCirugia2Tipo = fields.Char('Tipo')

	antAutoTuvo = fields.Boolean(u'¿Ha tenido algún intento de autoeliminación?')
	antAutoeliminCant = fields.Integer(u'Especifique cantidad de intentos de autoeliminación')
	antAutoelim1Edad = fields.Integer('Edad')
	antAutoelim1Tipo = fields.Char('Tipo')
	antAutoelim2Edad = fields.Integer('Edad')
	antAutoelim2Tipo = fields.Char('Tipo')

	######################################
	#### Violencia y Uso de Sustancias ###
	######################################

	### Danio psicologico ###
	tvioDanoPsico = u'¿Su pareja o alguien importante para usted le ha causado daño emocional o psicológico en forma repetida?'

	## Lo que seguia en string tvioDanoPsico: \n (Por ej.: por medio de alguna de las siguientes situaciones: insultos, maltrato a sus hijos, hacerlo/a\n sentir avergonzado/a o humillado/a desprecio por las tareas que usted realiza, destrucción de objetos\n de amigos o parientes, otras.)

	vioDanoPsico = fields.Selection([('si',u'Sí'),('no','No'),('nc','No desea contestar')],tvioDanoPsico)
	vioDanoPsicoQuien = fields.Char(u'¿Quién/es lo hizo/cieron?',states = {'invisible': 
		Or(
			Not(Equal(Eval('vioDanoPsico'),'si')),
					Or( 
						Equal(Eval('vioDanoPsico'),'no'),Equal(Eval('vioDanoPsico'),'nc')
					)
				)
		})
	vioDanoPsicoNino = fields.Boolean(u'Niño/a')

	vioDanoPsicoAdoles = fields.Boolean(u'Adolescente')
	vioDanoPsicoJoven = fields.Boolean(u'Joven')
	vioDanoPsicoAdulto = fields.Boolean(u'Adulto/a')
	vioDanoPsicoMayor = fields.Boolean(u'Mayor de 65')
	vioDanoPsicoEmbarazo = fields.Boolean(u'Embarazo/postparto')
	vioDanoPsicoActual = fields.Boolean(u'¿Sucede actualmente?',states = {'invisible': 
		Or(
			Not(Equal(Eval('vioDanoPsico'),'si')),
					Or( 
						Equal(Eval('vioDanoPsico'),'no'),Equal(Eval('vioDanoPsico'),'nc')
					)
				)
		})

	### Danio fisico ###
	tvioDanoFisico = u'¿Su pareja o alguien importante para usted le ha causado daño físico grave al menos una vez, o le ha hecho agresiones menores en forma reiterada?'

	## Lo que seguia en string tvioDanoFisico: \n (Por ej.: empujones, golpe de puños, quemaduras, zamarreos, mordeduras, ahorcamiento, pellizcos, palizas, golpes con objetos,\n tirón de pelo, patadas, daño con armas, cachetadas, otra forma.)
	vioDanoFisico = fields.Selection([('si',u'Sí'),('no','No'),('nc','No desea contestar')],tvioDanoFisico)
	vioDanoFisicoQuien = fields.Char(u'¿Quién/es lo hizo/cieron?',states = {'invisible': 
		Or(
			Not(Equal(Eval('vioDanoFisico'),'si')),
					Or( 
						Equal(Eval('vioDanoFisico'),'no'),Equal(Eval('vioDanoFisico'),'nc')
					)
				)
		})
	vioDanoFisicoNino = fields.Boolean(u'Niño/a')
	vioDanoFisicoAdoles = fields.Boolean(u'Adolescente')
	vioDanoFisicoJoven = fields.Boolean(u'Joven')
	vioDanoFisicoAdulto = fields.Boolean(u'Adulto/a')
	vioDanoFisicoMayor = fields.Boolean(u'Mayor de 65')
	vioDanoFisicoEmbarazo = fields.Boolean(u'Embarazo/postparto')
	vioDanoFisicoActual = fields.Boolean(u'¿Sucede actualmente?',states = {'invisible': 
		Or(
			Not(Equal(Eval('vioDanoFisico'),'si')),
					Or( 
						Equal(Eval('vioDanoFisico'),'no'),Equal(Eval('vioDanoFisico'),'nc')
					)
				)
		})

	### Danio sexual ###
	tvioDanoSexual = u'¿Cuando usted era niño/a recuerda haber sido tocado/a de manera inapropiada por alguien o haber tenido relaciones o contacto sexual?'
	vioDanoSexual = fields.Selection([('si',u'Sí'),('no','No'),('nc','No desea contestar')],tvioDanoSexual)
	vioDanoSexualQuien = fields.Char(u'¿Quién/es lo hizo/hicieron?',states = {'invisible': 
		Or(
			Not(Equal(Eval('vioDanoSexual'),'si')),
					Or( 
						Equal(Eval('vioDanoSexual'),'no'),Equal(Eval('vioDanoSexual'),'nc')
					)
				)
		})

	tvioViola = u'¿Alguna vez en su vida ha sido obligado/a a tener relaciones o contacto sexual?\n (Por ej.: empleo de la fuerza física, de intimidación o amenaza para mantener relaciones sexuales no deseadas.)'
	vioViola = fields.Selection([('si',u'Sí'),('no','No'),('nc','No desea contestar')],tvioViola)
	vioViolaQuien = fields.Char(u'¿Quién/es lo hizo/cieron?',states = {'invisible': 
		Or(
			Not(Equal(Eval('vioViola'),'si')),
					Or( 
						Equal(Eval('vioViola'),'no'),Equal(Eval('vioViola'),'nc')
					)
				)
		})
	vioViolaNino = fields.Boolean(u'Niño/a')
	vioViolaAdoles = fields.Boolean(u'Adolescente')
	vioViolaJoven = fields.Boolean(u'Joven')
	vioViolaAdulto = fields.Boolean(u'Adulto/a')
	vioViolaMayor = fields.Boolean(u'Mayor de 65')
	vioViolaEmbarazo = fields.Boolean(u'Embarazo/postparto')

	vioViolaActual = fields.Boolean(u'¿Sucede actualmente?',states = {'invisible': 
											And(
										Or(
											Not(Equal(Eval('vioViola'),'si')),
												Or(
													Equal(Eval('vioViola'),'no'),
													Equal(Eval('vioViola'),'nc')
												)
										),
											Or(
												Not(Equal(Eval('vioDanoSexual'),'si')),
												Or( 
													Equal(Eval('vioDanoSexual'),'no'),
													Equal(Eval('vioDanoSexual'),'nc')
												)
											)
									)	
		})


	vioPensamiento = fields.Selection([('si',u'Sí'),('no','No'),('nc','No desea contestar')],u'Hoy, en su casa, ¿piensa usted que podría sufrir alguna de las situaciones antes nombradas?')


	tsustAlcohol = u'Durante los últimos 30 días, ¿con qué frecuencia usted bebió al menos 4 medidas de cualquier\n clase de bebida con alcohol en un mismo día?'
	sustAlcohol = fields.Selection([('nunca','Nunca'),('unames','Una vez al mes'),('dosmes','2 o 3 veces al mes'),('unasemana','Una vez a la semana'),('dossemana',u'2 días a la semana o más')],tsustAlcohol)
	tsustCigarro = u'Durante los últimos 30 días, ¿con qué frecuencia usted fumó cigarrillos, tabaco o pipa?'
	sustCigarro = fields.Selection([('nunca','Nunca'),('unames','Una vez al mes'),('dosmes','2 o 3 veces al mes'),('unasemana','Una vez a la semana'),('dossemana',u'2 días a la semana o más')],tsustCigarro)
	tsustMedicamento = u'Durante los últimos 30 días, ¿con qué frecuencia usted usó algunos de los siguientes medicamentos \n POR SU CUENTA (esto es sin una receta de su médico o en cantidades mayores a las recetadas)?\n Medicamentos para el dolor como tramadol o morfina, estimulantes como ritalina, tranquilizantes como Lexotán.'
	sustMedicamento = fields.Selection([('nunca','Nunca'),('unames','Una vez al mes'),('dosmes','2 o 3 veces al mes'),('unasemana','Una vez a la semana'),('dossemana',u'2 días a la semana o más')],tsustMedicamento)
	tsustDroga = u'Durante los últimos 30 días, ¿con qué frecuencia usted usó algunas de las siguientes sustancias:\n Marihuana, Cocaína, Pasta Base, Crack, Estimulantes como éxtasis, Halucinógenos como hongos o LSD,\n Heroína, Inhalantes como pegamento?'
	sustDroga = fields.Selection([('nunca','Nunca'),('unames','Una vez al mes'),('dosmes','2 o 3 veces al mes'),('unasemana','Una vez a la semana'),('dossemana',u'2 días a la semana o más')],tsustDroga)


	#Antecedentes Familiares
	antFamIntervencion1 = fields.Selection([('madre','Madre'),('padre','Padre'),('hermano',u'Hermano/a'),('abuelo','Abuelo/a'),('tio',u'Tío/a'),('pareja','Pareja'),('hijo',u'Hijo/a'),('otro','Otro')],'Familiar')
	antFamIntervencionTipo1 = fields.Selection([('pedagogica',u'Intervención Pedagógica'),('medica',u'Intervención Médica'),('psico',u'Intervención Psicológica'),('psiq',u'Intervención Psiquiátrica'),('ipsiq',u'Internación Psiquiátrica')],'Tipo')
	antFamIntervencionMed1 = fields.Selection([('ninguna','Ninguna'),('ansiolitico',u'Ansiolíticos'),('antidepre','Antidepresivos'),('neurolep',u'Neurolépticos'),('otro','Otros')],u'Tipo de Medicación')
	antFamIntervencion2 = fields.Selection([('madre','Madre'),('padre','Padre'),('hermano',u'Hermano/a'),('abuelo','Abuelo/a'),('tio',u'Tío/a'),('pareja','Pareja'),('hijo',u'Hijo/a'),('otro','Otro')],'Familiar')
	antFamIntervencionTipo2 = fields.Selection([('pedagogica',u'Intervención Pedagógica'),('medica',u'Intervención Médica'),('psico',u'Intervención Psicológica'),('psiq',u'Intervención Psiquiátrica'),('ipsiq',u'Internación Psiquiátrica')],'Tipo')
	antFamIntervencionMed2 = fields.Selection([('ninguna','Ninguna'),('ansiolitico',u'Ansiolíticos'),('antidepre','Antidepresivos'),('neurolep',u'Neurolépticos'),('otro','Otros')],u'Tipo de Medicación')
	antFamIntervencion3 = fields.Selection([('madre','Madre'),('padre','Padre'),('hermano',u'Hermano/a'),('abuelo','Abuelo/a'),('tio',u'Tío/a'),('pareja','Pareja'),('hijo',u'Hijo/a'),('otro','Otro')],'Familiar')
	antFamIntervencionTipo3 = fields.Selection([('pedagogica',u'Intervención Pedagógica'),('medica',u'Intervención Médica'),('psico',u'Intervención Psicológica'),('psiq',u'Intervención Psiquiátrica'),('ipsiq',u'Internación Psiquiátrica')],'Tipo')
	antFamIntervencionMed3 = fields.Selection([('ninguna','Ninguna'),('ansiolitico',u'Ansiolíticos'),('antidepre','Antidepresivos'),('neurolep',u'Neurolépticos'),('otro','Otros')],u'Tipo de Medicación')

	antFamEnfyDef1 = fields.Selection([('madre','Madre'),('padre','Padre'),('hermano',u'Hermano/a'),('abuelo','Abuelo/a'),('tio',u'Tío/a'),('pareja','Pareja'),('hijo',u'Hijo/a'),('otro','Otro')],'Familiar')
	antFamEnf1 = fields.Selection([('asma',u'Asma'),('epilepsia',u'Epilepsia'),('cancer',u'Cáncer'),('vih',u'VIH/SIDA'),('diabetes',u'Diabetes'),('osteo',u'Pat. Osteoarticular'),('tiroides',u'Enf. Tiroidea'),('cardios',u'Enf. Cardiovascular')],u'Enfermedades Crónicas')
	antFamDiscap1 = fields.Selection([('ceguera',u'Ceguera y/o dism. de visión'),('sordera',u'Sordera / hipoacusia'),('motriz',u'Def. Motriz'),('depen',u'Dependencia de otra persona')],u'Discapacidades')
	antFamEnfyDef2 = fields.Selection([('madre','Madre'),('padre','Padre'),('hermano',u'Hermano/a'),('abuelo','Abuelo/a'),('tio',u'Tío/a'),('pareja','Pareja'),('hijo',u'Hijo/a'),('otro','Otro')],'Familiar')
	antFamEnf2 = fields.Selection([('asma',u'Asma'),('epilepsia',u'Epilepsia'),('cancer',u'Cáncer'),('vih',u'VIH/SIDA'),('diabetes',u'Diabetes'),('osteo',u'Pat. Osteoarticular'),('tiroides',u'Enf. Tiroidea'),('cardios',u'Enf. Cardiovascular')],u'Enfermedades Crónicas')
	antFamDiscap2 = fields.Selection([('ceguera',u'Ceguera y/o dism. de visión'),('sordera',u'Sordera / hipoacusia'),('motriz',u'Def. Motriz'),('depen',u'Dependencia de otra persona')],u'Discapacidades')
	antFamEnfyDef3 = fields.Selection([('madre','Madre'),('padre','Padre'),('hermano',u'Hermano/a'),('abuelo','Abuelo/a'),('tio',u'Tío/a'),('pareja','Pareja'),('hijo',u'Hijo/a'),('otro','Otro')],'Familiar')
	antFamEnf3 = fields.Selection([('asma',u'Asma'),('epilepsia',u'Epilepsia'),('cancer',u'Cáncer'),('vih',u'VIH/SIDA'),('diabetes',u'Diabetes'),('osteo',u'Pat. Osteoarticular'),('tiroides',u'Enf. Tiroidea'),('cardios',u'Enf. Cardiovascular')],u'Enfermedades Crónicas')
	antFamDiscap3 = fields.Selection([('ceguera',u'Ceguera y/o dism. de visión'),('sordera',u'Sordera / hipoacusia'),('motriz',u'Def. Motriz'),('depen',u'Dependencia de otra persona')],u'Discapacidades')

	antFamAutoelim1 = fields.Selection([('madre','Madre'),('padre','Padre'),('hermano',u'Hermano/a'),('abuelo','Abuelo/a'),('tio',u'Tío/a'),('pareja','Pareja'),('hijo',u'Hijo/a'),('otro','Otro')],'Familiar')
	antFamAutoelimEdad1 = fields.Integer('Edad')
	antFamAutoelimConsu1 = fields.Boolean('Consumado')
	antFamAutoelim2 = fields.Selection([('madre','Madre'),('padre','Padre'),('hermano',u'Hermano/a'),('abuelo','Abuelo/a'),('tio',u'Tío/a'),('pareja','Pareja'),('hijo',u'Hijo/a'),('otro','Otro')],'Familiar')
	antFamAutoelimEdad2 = fields.Integer('Edad')
	antFamAutoelimConsu2 = fields.Boolean('Consumado')
	antFamAutoelim3 = fields.Selection([('madre','Madre'),('padre','Padre'),('hermano',u'Hermano/a'),('abuelo','Abuelo/a'),('tio',u'Tío/a'),('pareja','Pareja'),('hijo',u'Hijo/a'),('otro','Otro')],'Familiar')
	antFamAutoelimEdad3 = fields.Integer('Edad')
	antFamAutoelimConsu3 = fields.Boolean('Consumado')

	### Violencia y Uso de Sustancias en familiares ###
	vioFam1 = fields.Selection([('madre','Madre'),('padre','Padre'),('hermano',u'Hermano/a'),('abuelo','Abuelo/a'),('tio',u'Tío/a'),('pareja','Pareja'),('hijo',u'Hijo/a'),('otro','Otro')],'Familiar')

	vioDanoPsicoFam1 = fields.Boolean(u'Daño emocional o psicológico')
	vioDanoPsicoActualFam1 = fields.Selection([('si',u'Sí'),('no','No'),('nc','No desea contestar')],u'¿Sucede actualmente?')

	vioDanoFisicoFam1 = fields.Boolean(u'Daño físico')
	vioDanoFisicoActualFam1 = fields.Selection([('si',u'Sí'),('no','No'),('nc','No desea contestar')],u'¿Sucede actualmente?')
    
	vioDanoSexualFam1 = fields.Boolean(u'Abuso sexual')
	vioDanoSexualActualFam1 = fields.Selection([('si',u'Sí'),('no','No'),('nc','No desea contestar')],u'¿Sucede actualmente?')
    

	vioFam2 = fields.Selection([('madre','Madre'),('padre','Padre'),('hermano',u'Hermano/a'),('abuelo','Abuelo/a'),('tio',u'Tío/a'),('pareja','Pareja'),('hijo',u'Hijo/a'),('otro','Otro')],'Familiar')
	
	vioDanoPsicoFam2 = fields.Boolean(u'Daño emocional o psicológico')
	vioDanoPsicoActualFam2 = fields.Selection([('si',u'Sí'),('no','No'),('nc','No desea contestar')],u'¿Sucede actualmente?')

	vioDanoFisicoFam2 = fields.Boolean(u'Daño físico')
	vioDanoFisicoActualFam2 = fields.Selection([('si',u'Sí'),('no','No'),('nc','No desea contestar')],u'¿Sucede actualmente?')
    
	vioDanoSexualFam2 = fields.Boolean(u'Abuso sexual')
	vioDanoSexualActualFam2 = fields.Selection([('si',u'Sí'),('no','No'),('nc','No desea contestar')],u'¿Sucede actualmente?')


	vioFam3 = fields.Selection([('madre','Madre'),('padre','Padre'),('hermano',u'Hermano/a'),('abuelo','Abuelo/a'),('tio',u'Tío/a'),('pareja','Pareja'),('hijo',u'Hijo/a'),('otro','Otro')],'Familiar')
	vioDanoPsicoFam3 = fields.Boolean(u'Daño emocional o psicológico')
	vioDanoPsicoActualFam3 = fields.Selection([('si',u'Sí'),('no','No'),('nc','No desea contestar')],u'¿Sucede actualmente?')

	vioDanoFisicoFam3 = fields.Boolean(u'Daño físico')
	vioDanoFisicoActualFam3 = fields.Selection([('si',u'Sí'),('no','No'),('nc','No desea contestar')],u'¿Sucede actualmente?')
    
	vioDanoSexualFam3 = fields.Boolean(u'Abuso sexual')
	vioDanoSexualActualFam3 = fields.Selection([('si',u'Sí'),('no','No'),('nc','No desea contestar')],u'¿Sucede actualmente?')

    ######################################
    ##### SUSTANCIAS (de familiares) #####
    ######################################

    # Familiar 1
	sustFam1 = fields.Selection([('madre','Madre'),('padre','Padre'),('hermano',u'Hermano/a'),('abuelo','Abuelo/a'),('tio',u'Tío/a'),('pareja','Pareja'),('hijo',u'Hijo/a'),('otro','Otro')],'Familiar')

	sustAlcoholFam1 = fields.Selection([('nunca','Nunca'),('sinosabfreq','Si (no sabe freq.)'),('unames','Una vez al mes'),('dosmes','2 o 3 veces al mes'),('unasemana','Una vez a la semana'),('dossemana',u'2 días a la semana o más')],'Alcoholismo')

	sustCigarroFam1 = fields.Selection([('nunca','Nunca'),('sinosabfreq','Si (no sabe freq.)'),('unames','Una vez al mes'),('dosmes','2 o 3 veces al mes'),('unasemana','Una vez a la semana'),('dossemana',u'2 días a la semana o más')],'Tabaquismo')

	sustMedicamentoFam1 = fields.Selection([('nunca','Nunca'),('sinosabfreq','Si (no sabe freq.)'),('unames','Una vez al mes'),('dosmes','2 o 3 veces al mes'),('unasemana','Una vez a la semana'),('dossemana',u'2 días a la semana o más')],'Abuso de medicamentos')

	sustDrogaFam1 = fields.Selection([('nunca','Nunca'),('sinosabfreq','Si (no sabe freq.)'),('unames','Una vez al mes'),('dosmes','2 o 3 veces al mes'),('unasemana','Una vez a la semana'),('dossemana',u'2 días a la semana o más')],'Consumo de drogas')

    # Familiar 2
	sustFam2 = fields.Selection([('madre','Madre'),('padre','Padre'),('hermano',u'Hermano/a'),('abuelo','Abuelo/a'),('tio',u'Tío/a'),('pareja','Pareja'),('hijo',u'Hijo/a'),('otro','Otro')],'Familiar')

	tsustAlcoholFam2 = u'Alcoholismo'
	sustAlcoholFam2 = fields.Selection([('nunca','Nunca'),('sinosabfreq','Si (no sabe freq.)'),('unames','Una vez al mes'),('dosmes','2 o 3 veces al mes'),('unasemana','Una vez a la semana'),('dossemana',u'2 días a la semana o más')],tsustAlcoholFam2)

	tsustCigarroFam2 = u'Tabaquismo'
	sustCigarroFam2 = fields.Selection([('nunca','Nunca'),('sinosabfreq','Si (no sabe freq.)'),('unames','Una vez al mes'),('dosmes','2 o 3 veces al mes'),('unasemana','Una vez a la semana'),('dossemana',u'2 días a la semana o más')],tsustCigarroFam2)

	tsustMedicamentoFam2 = u'Abuso de medicamentos'
	sustMedicamentoFam2 = fields.Selection([('nunca','Nunca'),('sinosabfreq','Si (no sabe freq.)'),('unames','Una vez al mes'),('dosmes','2 o 3 veces al mes'),('unasemana','Una vez a la semana'),('dossemana',u'2 días a la semana o más')],tsustMedicamentoFam2)

	tsustDrogaFam2 = u'Consumo de drogas'
	sustDrogaFam2 = fields.Selection([('nunca','Nunca'),('sinosabfreq','Si (no sabe freq.)'),('unames','Una vez al mes'),('dosmes','2 o 3 veces al mes'),('unasemana','Una vez a la semana'),('dossemana',u'2 días a la semana o más')],tsustDrogaFam2)

    # Familiar 3
	sustFam3 = fields.Selection([('madre','Madre'),('padre','Padre'),('hermano',u'Hermano/a'),('abuelo','Abuelo/a'),('tio',u'Tío/a'),('pareja','Pareja'),('hijo',u'Hijo/a'),('otro','Otro')],'Familiar')

	tsustAlcoholFam3 = u'Alcoholismo'
	sustAlcoholFam3 = fields.Selection([('nunca','Nunca'),('sinosabfreq','Si (no sabe freq.)'),('unames','Una vez al mes'),('dosmes','2 o 3 veces al mes'),('unasemana','Una vez a la semana'),('dossemana',u'2 días a la semana o más')],tsustAlcoholFam3)

	tsustCigarroFam3 = u'Tabaquismo'
	sustCigarroFam3 = fields.Selection([('nunca','Nunca'),('sinosabfreq','Si (no sabe freq.)'),('unames','Una vez al mes'),('dosmes','2 o 3 veces al mes'),('unasemana','Una vez a la semana'),('dossemana',u'2 días a la semana o más')],tsustCigarroFam3)

	tsustMedicamentoFam3 = u'Abuso de medicamentos'
	sustMedicamentoFam3 = fields.Selection([('nunca','Nunca'),('sinosabfreq','Si (no sabe freq.)'),('unames','Una vez al mes'),('dosmes','2 o 3 veces al mes'),('unasemana','Una vez a la semana'),('dossemana',u'2 días a la semana o más')],tsustMedicamentoFam3)

	tsustDrogaFam3 = u'Consumo de drogas'
	sustDrogaFam3 = fields.Selection([('nunca','Nunca'),('sinosabfreq','Si (no sabe freq.)'),('unames','Una vez al mes'),('dosmes','2 o 3 veces al mes'),('unasemana','Una vez a la semana'),('dossemana',u'2 días a la semana o más')],tsustDrogaFam3)

    #####################################################
    ####### Tratamiento e invervenciones actuales #######
    #####################################################

	fechaIntervePeda = fields.Date(u'Fecha de inicio')
	fechaInterveMedica = fields.Date(u'Fecha de inicio')
	fechaIntervePsico = fields.Date(u'Fecha de inicio')
	fechaIntervePsiqui = fields.Date(u'Fecha de inicio')
	fechaInternaPsiqui = fields.Date(u'Fecha de inicio')
	fechaTrataOtra1 = fields.Date('Fecha de inicio')
	fechaTrataOtra2 = fields.Date('Fecha de inicio')
	fechaTrataOtra3 = fields.Date('Fecha de inicio')

	#fechaIntervePeda = fields.Date(u'Intervención pedagógica')
	#fechaInterveMedica = fields.Date(u'Intervención médica')
	#fechaIntervePsico = fields.Date(u'Intervención psicológica')
	#fechaIntervePsiqui = fields.Date(u'Intervención psiquiátrica')
	#fechaInternaPsiqui = fields.Date(u'Internación psiquiátrica')
	#fechaTrataOtra1 = fields.Date('Otra')
	#fechaTrataOtra2 = fields.Date('Otra')
	#fechaTrataOtra3 = fields.Date('Otra')

	mediIntervePeda = fields.Boolean(u'Medicación')
	mediInterveMedica = fields.Boolean(u'Medicación')
	mediIntervePsico = fields.Boolean(u'Medicación')
	mediIntervePsiqui = fields.Boolean(u'Medicación')
	mediInternaPsiqui = fields.Boolean(u'Medicación')
	mediTrataOtra1 = fields.Boolean(u'Medicación')
	mediTrataOtra2 = fields.Boolean(u'Medicación')
	mediTrataOtra3 = fields.Boolean(u'Medicación')

	tipoMediIntervePeda = fields.Selection([('antisoliticos',u'Antisolíticos'),('antidepresivos','Antidepresivos'),('neurolepticos',u'Neurolépticos'),('otro','Otro')],u'Tipo de medicación')
	tipoMediInterveMedica = fields.Selection([('antisoliticos',u'Antisolíticos'),('antidepresivos','Antidepresivos'),('neurolepticos',u'Neurolépticos'),('otro','Otro')],u'Tipo de medicación')
	tipoMediIntervePsico = fields.Selection([('antisoliticos',u'Antisolíticos'),('antidepresivos','Antidepresivos'),('neurolepticos',u'Neurolépticos'),('otro','Otro')],u'Tipo de medicación')
	tipoMediIntervePsiqui = fields.Selection([('antisoliticos',u'Antisolíticos'),('antidepresivos','Antidepresivos'),('neurolepticos',u'Neurolépticos'),('otro','Otro')],u'Tipo de medicación')
	tipoMediInternaPsiqui = fields.Selection([('antisoliticos',u'Antisolíticos'),('antidepresivos','Antidepresivos'),('neurolepticos',u'Neurolépticos'),('otro','Otro')],u'Tipo de medicación')
	tipoMediTrataOtra1 = fields.Selection([('antisoliticos',u'Antisolíticos'),('antidepresivos','Antidepresivos'),('neurolepticos',u'Neurolépticos'),('otro','Otro')],u'Tipo de medicación')
	tipoMediTrataOtra2 = fields.Selection([('antisoliticos',u'Antisolíticos'),('antidepresivos','Antidepresivos'),('neurolepticos',u'Neurolépticos'),('otro','Otro')],u'Tipo de medicación')
	tipoMediTrataOtra3 = fields.Selection([('antisoliticos',u'Antisolíticos'),('antidepresivos','Antidepresivos'),('neurolepticos',u'Neurolépticos'),('otro','Otro')],u'Tipo de medicación')

	ObsIntervePeda = fields.Text('Obs. y motivos')
	ObsInterveMedica = fields.Text('Obs. y motivos')
	ObsIntervePsico = fields.Text('Obs. y motivos')
	ObsIntervePsiqui = fields.Text('Obs. y motivos')
	ObsInternaPsiqui = fields.Text('Obs. y motivos')
	ObsTrataOtra1 = fields.Text('Obs. y motivos')
	ObsTrataOtra2 = fields.Text('Obs. y motivos')
	ObsTrataOtra3 = fields.Text('Obs. y motivos')

	#########################################################
	##################### RELATO ############################
	#########################################################

	#### Afectos - Emociones - Estados afectivos ####
	angustia = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Angustia')
	ansiedad = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Ansiedad')
	sentCulpa = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Sentimientos de culpa')
	sentTristeza = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Sentimientos de tristeza')
	sentSoledad = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Sentimientos de soledad')
	sentDesconfianza = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Sentimientos de desconfianza')
	sentGrandeza = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Sentimientos de grandeza (omnipotencia)')
	sentCelos = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Sentimientos de celos')
	sentEnvidia = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Sentimientos de envidia')
	elevNivelExigencia = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Elevado nivel de exigencia')
	malHumor = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Malhumor')

	### Subgrupo: Estado afectivo o humor ###
	depresivo = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Depresivo')
	expansivo = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Expansivo')
	melancolico = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Melancólico')

	#### Autoestima o imagen de si ####
	imgMismoDevaluada = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Imagen de si mismo devaluada')
	imgMismoSobrevaluada = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Imagen de si mismo sobrevaluada')
	inseguridad = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Inseguridad')
	cmbsImgMismo = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Cambios en la imagen de si mismo (con o sin sentimientos de desconocimiento)')
	vivenciasVacio = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Vivencias de vacío')

	#### Sintomas neuroticos ####
	fobias = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Fobias')
	sintomasConversivos = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Síntomas conversivos')
	sintomasObsesivos = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Síntomas obsesivos')

	#### El cuerpo y sus funciones ####
	transtornoSueno = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Transtorno de sueño')
	disfuncionSexual = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Disfunción sexual')
	sintomasPsicosomaticos = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Síntomas psicosomáticos')
	quejasHipocondria = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Quejas - hipocondría')
	
	#### Regulacion de los afectos e impulsos ####
	bajaTolFrustracion = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Baja tolerancia a la frustración')
	dificultadCtrlImpulsos = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Dificultad en el control de los impulsos')
	hiperactividad = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Hiperactividad')
	iae = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'IAE')

	### Subgrupo: Adicciones ###
	adiJuegoAzar = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Juego/Azar')
	adiTabaco = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Tabaco')
	adiAlcohol = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Alcohol')
	adiDrogas = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Drogas')

	### Subgrupo: Consumo problematico ###
	consumoProbJuegoAzar = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Juego/Azar')
	consumoProbTabaco = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Tabaco')
	consumoProbAlcohol = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Alcohol')
	consumoProbDrogas = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Drogas')

	alimenticias = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Alimenticias')
	sexual = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Sexual')
	otro = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Otro')

	#### Sintomas delirantes o pensamientos ####
	
	### Subgrupo: sintomas delirantes ###
	sintDelirantesAgudos = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Agudos')
	sintDelirantesCronicos = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Crónicos')
	sintDelirantesCronicosReagudizados = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Crónicos reagudizados')
	proyResponsabilidadOtros = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Proyección de responsabilidad en otros o la realidad')
	proyMasivaResponsabilidadOtros = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Proyección masiva de responsabilidad en otros o realidad')
	ideasPersecutorias = fields.Selection([('mcpcte','M.C. pcte.'),('mcacomp','M.C. acomp.'),('mcpsico','M.C. psico.'), ('Relato','Relato')],u'Ideas persecutorias')

	### DEFAULT VALUES ###
	@staticmethod 
	def default_tipoConsulta():
        #tipoConsulta = fields.Selection([('esp',u'Consulta espontánea'),('tra',u'Traído'),('ori',u'Consulta por orientación'),('der','Derivado')],'Tipo de Consulta') #Auto completar este dato
       # tConsulta = ([
        #    ('esp', u'Consulta espontánea'),
         #   ('tra', u'Traído'),
         #   ('ori', u'Consulta por orientación'),
         #   ('der', 'Derivado'),
        #], 'Tipo de Consulta') 
        #('ori', u'Consulta por orientación')

		return 'der'

		#super(Formulario, cls).default_motivoPaciente1() 

	@staticmethod 
	def default_deficiencia():
		return 'con'

	@staticmethod 
	def default_eduNoFormal():
		return 'no'

	@staticmethod 
	def default_diagEspec():
		return 'no'

	@staticmethod 
	def default_trabSituacion():
		return 'no'

	#Books = Pool().get('library.book')
	#	pool = Pool()
	#	ModeloPaciente = pool.get('cefiro.paciente')

		
		
		#return str(idA

Formulario()

