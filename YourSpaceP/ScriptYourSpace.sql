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

create table asesores(
	id int not null primary key auto_increment,
	id_persona int not null,
	foreign key (id_persona) references personas (id) on delete cascade on update cascade
);

create table espe(
	id int not null primary key auto_increment,
	espe varchar(500) default null
);

create table asesor_espe(
	id int not null primary key auto_increment,
    id_asesor int not null,
	foreign key (id_asesor) references asesores (id) on delete cascade on update cascade,
    id_espe int default null,
	foreign key (id_espe) references espe (id) on delete cascade on update cascade
);

create table tipos(
	id int not null primary key auto_increment,
	tipo varchar(50)
);

create table servicios(
	id int not null primary key auto_increment,
    materia varchar(50),
	id_tipo int not null,
	foreign key (id_tipo) references tipos (id) on delete cascade on update cascade,
    descripcion varchar(500)
);


create table servicio_asesor_espe(
	id int not null primary key auto_increment,
	id_servicio int not null,
	foreign key (id_servicio) references servicios (id) on delete cascade on update cascade,
	id_asesor_espe int not null,
	foreign key (id_asesor_espe) references asesor_espe (id) on delete cascade on update cascade,
    fecha datetime,
    lugar varchar(500)
);

create table material_servicio_asesor_espe(
	id int not null primary key auto_increment,
	id_servicio_asesor_espe int not null,
	foreign key (id_servicio_asesor_espe) references servicio_asesor_espe (id) on delete cascade on update cascade,
    material varchar(500)
);




-- drop view vw_info;

select * from vw_info;

create view vw_info as
select distinct
    m.material,
    sae.fecha,
    sae.lugar,
    se.espe,
    u.usuario,
    p.correo,
    t.tipo,
    sv.materia,
    sv.descripcion
from
    material_servicio_asesor_espe m
    inner join servicio_asesor_espe sae on m.id_servicio_asesor_espe = sae.id
    inner join asesor_espe ae on sae.id_asesor_espe = ae.id
    inner join asesores a on ae.id_asesor = a.id
    inner join personas p on a.id_persona = p.id
    inner join espe se on ae.id_espe = se.id
    inner join servicios sv on sae.id_servicio = sv.id
    inner join tipos t on sv.id_tipo = t.id
    inner join usuarios u on p.id = u.id_persona;
*/


-- -------------------------------------------------

create table usuarios(
	id int not null primary key auto_increment,
	id_persona int not null,
	foreign key (id_persona) references personas (id) on delete cascade on update cascade,
    usuario varchar(50),
    pass varchar(50)
);
-- -------------------------------------------------

create table carreras(
	id int not null primary key auto_increment,
	carrera varchar(50)
);

create table estudiantes(
	id int not null primary key auto_increment,
	id_carrera int not null,
	foreign key (id_carrera) references carreras (id) on delete cascade on update cascade,
    id_persona int not null,
	foreign key (id_persona) references personas (id) on delete cascade on update cascade,
    cuatri int 
);

create table servicio_estudiante(
	id int not null primary key auto_increment,
	id_servicio int not null,
	foreign key (id_servicio) references servicios (id) on delete cascade on update cascade,
	id_estudiante int not null,
	foreign key (id_estudiante) references estudiantes (id) on delete cascade on update cascade,
    fecha datetime
);
	






