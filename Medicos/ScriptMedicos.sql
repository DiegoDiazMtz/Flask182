drop database if exists consultorio;
create database consultorio;
use consultorio;

create table Pacientes(
id int not null auto_increment primary key,
Nombres varchar(100),
ApellidoP varchar(100),
ApellidoM varchar(100),
Fecha_nac date
);

create table Datos_meds(
id int not null auto_increment primary key,
RFC varchar(18) unique,
nombres varchar(100),
apellidoP varchar(100),
apellidoM varchar(100),
Cedula_prof varchar(18),
Correo varchar(50),
Rol enum('Medico_Admin','Medico'),
contraseña varchar(50)
);

select TIMESTAMPDIFF(YEAR, fecha_nac, CURDATE()) AS Edad from pacientes;
select * from pacientes;

-- select pac.nombres, pac.ApellidoP, pac.ApellidoM, pac.Fecha_nac from Pacientes pac inner join Expedientes exp on pac.id = exp.id_paciente inner join Datos_meds datmed on exp.id_medico = datmed.id;
-- select * from Pacientes pac inner join Expedientes exp on pac.id = exp.id_paciente inner join Datos_meds datmed on exp.id_medico = datmed.id ;

create table Expedientes(
id_paciente int not null primary key,
foreign key (id_paciente) references Pacientes (id) on delete cascade on update cascade,
id_medico int not null,
foreign key (id_medico) references Datos_meds (id) on delete cascade on update cascade,
Enfermedades_cronicas varchar(200),
Alergias varchar(200),
Antecedentes_familiares varchar(200)
);

create table Exploraciones (
id int not null auto_increment primary key,
id_paciente int not null,
foreign key (id_paciente) references Pacientes (id) on delete cascade on update cascade,
Fecha datetime,
Peso dec(3.2),
Altura dec(3.2),
Temperatura dec(2.2),
Latidos_minuto dec(3.2),
Saturacion_oxigeno varchar(10),
Glucosa varchar(10)
);

create table Diagnosticos(
id int not null auto_increment primary key,
id_exploracion int not null,
foreign key (id_exploracion) references Exploraciones (id) on update cascade on delete cascade,
Sintomas varchar(150),
Tratamiento varchar(200),
Estudios varchar(150) default null
);

create table Recetas(
id int not null auto_increment primary key,
id_exploracion int not null,
foreign key (id_exploracion) references Exploraciones (id) on update cascade on delete cascade,
id_diagnostico int not null,
foreign key (id_diagnostico) references Diagnosticos (id) on update cascade on delete cascade
);

select * from recetas;

select * from diagnosticos;
select * from exploraciones;

select * from datos_meds;
select * from Pacientes;
-- select * from datos_meds where nombre_com like "%Patricio%";

insert into Datos_meds (RFC, nombres, apellidoP, apellidoM, Cedula_prof, Correo, Rol, contraseña) value 
('GOMP670106HQTMRTA3', 'Patricio Misael', 'Gómez',  'Morales', 'ABCD12345XYZW', 'patitobida@gmail.com', 'Medico_Admin', '1234');

select * from exploraciones;
select * from diagnosticos;



/*
personas = [
    {
        'Nombres': 'John',
        'ApellidoP': 'Doe',
        'ApellidoM': 'Smith',
        'Fecha_nac': '1990-01-01',
        'Enfermedades_cronicas': 'Asma',
        'Alergias': 'Polen',
        'Antecedentes_familiares': 'Diabetes'
    },
    {
        'Nombres': 'Jane',
        'ApellidoP': 'Smith',
        'ApellidoM': 'Doe',
        'Fecha_nac': '1985-03-15',
        'Enfermedades_cronicas': 'Hipertensión',
        'Alergias': 'Nueces',
        'Antecedentes_familiares': 'Ninguno'
    },
    {
        'Nombres': 'Michael',
        'ApellidoP': 'Johnson',
        'ApellidoM': 'Brown',
        'Fecha_nac': '1988-06-20',
        'Enfermedades_cronicas': 'Artritis',
        'Alergias': 'Penicilina',
        'Antecedentes_familiares': 'Cáncer'
    },
    {
        'Nombres': 'Emily',
        'ApellidoP': 'Williams',
        'ApellidoM': 'Miller',
        'Fecha_nac': '1992-12-10',
        'Enfermedades_cronicas': 'Depresión',
        'Alergias': 'Mariscos',
        'Antecedentes_familiares': 'Asma'
    },
    {
        'Nombres': 'Daniel',
        'ApellidoP': 'Brown',
        'ApellidoM': 'Johnson',
        'Fecha_nac': '1982-07-05',
        'Enfermedades_cronicas': 'Diabetes',
        'Alergias': 'Ninguna',
        'Antecedentes_familiares': 'Hipertensión'
    },
    {
        'Nombres': 'Sophia',
        'ApellidoP': 'Miller',
        'ApellidoM': 'Williams',
        'Fecha_nac': '1995-09-25',
        'Enfermedades_cronicas': 'Ninguna',
        'Alergias': 'Lácteos',
        'Antecedentes_familiares': 'Ninguno'
    },
    {
        'Nombres': 'Matthew',
        'ApellidoP': 'Taylor',
        'ApellidoM': 'Anderson',
        'Fecha_nac': '1989-04-14',
        'Enfermedades_cronicas': 'Alergias',
        'Alergias': 'Polvo',
        'Antecedentes_familiares': 'Artritis'
    },
    {
        'Nombres': 'Olivia',
        'ApellidoP': 'Johnson',
        'ApellidoM': 'Brown',
        'Fecha_nac': '1998-11-30',
        'Enfermedades_cronicas': 'Ninguna',
        'Alergias': 'Ninguna',
        'Antecedentes_familiares': 'Ninguno'
    },
    {
        'Nombres': 'William',
        'ApellidoP': 'Miller',
        'ApellidoM': 'Williams',
        'Fecha_nac': '1993-08-08',
        'Enfermedades_cronicas': 'Ninguna',
        'Alergias': 'Ninguna',
        'Antecedentes_familiares': 'Ninguno'
    },
    {
        'Nombres': 'Ava',
        'ApellidoP': 'Smith',
        'ApellidoM': 'Doe',
        'Fecha_nac': '1987-02-18',
        'Enfermedades_cronicas': 'Hipertensión',
        'Alergias': 'Ninguna',
        'Antecedentes_familiares': 'Diabetes'
    }
    ]
    for persona in personas:
        VnombreP = persona['Nombres']
        VapellidoPP = persona['ApellidoP']
        VapellidoPM = persona['ApellidoM']
        VfechaNP = persona['Fecha_nac']
        VEnfermedadesP = persona['Enfermedades_cronicas']
        ValergiasP = persona['Alergias']
        VantecedentesP = persona['Antecedentes_familiares']

        # Insertar datos en la tabla Pacientes
        CS = mysql.connection.cursor()
        CS.execute('INSERT INTO Pacientes (Nombres, ApellidoP, ApellidoM, Fecha_nac) VALUES (%s, %s, %s, %s)', (VnombreP, VapellidoPP, VapellidoPM, VfechaNP))
        mysql.connection.commit()

        # Obtener el ID del paciente insertado
        CS.execute('SELECT id FROM Pacientes WHERE Nombres=%s AND ApellidoP=%s AND ApellidoM=%s AND Fecha_nac=%s', (VnombreP, VapellidoPP, VapellidoPM, VfechaNP))
        idP = CS.fetchone()[0]

        # Insertar datos en la tabla Expedientes
        idM = 1  # Cambiar esto por el ID del médico correspondiente
        CS.execute('INSERT INTO Expedientes (id_paciente, id_medico, Enfermedades_cronicas, Alergias, Antecedentes_familiares) VALUES (%s, %s, %s, %s, %s)', (idP, idM, VEnfermedadesP, ValergiasP, VantecedentesP))
        mysql.connection.commit()
*/
