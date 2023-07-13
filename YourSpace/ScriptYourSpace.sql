-- drop database yourSpace;
create database yourSpace; 
use yourSpace;

create table personas(
	id int not null primary key auto_increment,
    nombre varchar(50),
    ap varchar(50),
    am varchar(50),
    correo varchar(50)
);

create table carreras(
	id int not null primary key auto_increment,
	carrera varchar(50)
);

create table asesores(
	id int not null primary key auto_increment,
	id_persona int not null,
	foreign key (id_persona) references personas (id) on delete cascade on update cascade
);

create table espe(
	id int not null primary key auto_increment,
	espe varchar(50)
);

create table asesor_espe(
	id int not null primary key auto_increment,
    id_asesor int not null,
	foreign key (id_asesor) references asesores (id) on delete cascade on update cascade,
    id_espe int not null,
	foreign key (id_espe) references espe (id) on delete cascade on update cascade
);

create table tipos(
	id int not null primary key auto_increment,
	tipo varchar(50)
);

create table estudiantes(
	id int not null primary key auto_increment,
	id_carrera int not null,
	foreign key (id_carrera) references carreras (id) on delete cascade on update cascade,
    id_persona int not null,
	foreign key (id_persona) references personas (id) on delete cascade on update cascade,
    cuatri int 
);

create table servicios(
	id int not null primary key auto_increment,
	id_tipo int not null,
	foreign key (id_tipo) references tipos (id) on delete cascade on update cascade,
    descripcion varchar(200)
);

create table servicio_asesor(
	id int not null primary key auto_increment,
	id_servicio int not null,
	foreign key (id_servicio) references servicios (id) on delete cascade on update cascade,
	id_asesor int not null,
	foreign key (id_asesor) references asesores (id) on delete cascade on update cascade,
    fecha datetime,
    lugar varchar(200)
);

create table servicio_estudiante(
	id int not null primary key auto_increment,
	id_servicio_asesor int not null,
	foreign key (id_servicio_asesor) references servicio_asesor (id) on delete cascade on update cascade,
	id_estudiante int not null,
	foreign key (id_estudiante) references estudiantes (id) on delete cascade on update cascade,
    fecha datetime
);

create table material_clase(
	id int not null primary key auto_increment,
	id_servicio_asesor int not null,
	foreign key (id_servicio_asesor) references servicio_asesor (id) on delete cascade on update cascade,
    material varchar(200)
);

create table usuarios(
	id int not null primary key auto_increment,
	id_persona int not null,
	foreign key (id_persona) references personas (id) on delete cascade on update cascade,
    usuario varchar(50),
    pass varchar(50)
);

