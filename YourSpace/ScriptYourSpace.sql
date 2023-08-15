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

drop view vw_info;

select * from vw_info;
drop view vw_info;
create view vw_info as
select distinct
    m.id as id,
    m.material,
    sae.fecha,
    sae.lugar,
    se.espe,
    u.usuario,
    p.correo,
    t.tipo,
    sv.materia,
    sv.descripcion,
    sv.id as id_servicio
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
	foreign key (id_servicio) references material_servicio_asesor_espe (id) on delete cascade on update cascade,
	id_estudiante int not null,
	foreign key (id_estudiante) references estudiantes (id) on delete cascade on update cascade,
    fecha datetime
);

select * from servicio_estudiante;


create view vw_allinfo as
SELECT DISTINCT
    se_est.id as id,
    m.material,
    sae.fecha,
    sae.lugar,
    se.espe,
    u_asesor.usuario AS usuario_asesor,
    u_estudiante.usuario AS usuario_estudiante,
    p.correo,
    t.tipo,
    sv.materia,
    sv.descripcion
FROM
    material_servicio_asesor_espe m
    INNER JOIN servicio_asesor_espe sae ON m.id_servicio_asesor_espe = sae.id
    INNER JOIN asesor_espe ae ON sae.id_asesor_espe = ae.id
    INNER JOIN asesores a ON ae.id_asesor = a.id
    INNER JOIN personas p ON a.id_persona = p.id
    INNER JOIN espe se ON ae.id_espe = se.id
    INNER JOIN servicios sv ON sae.id_servicio = sv.id
    INNER JOIN tipos t ON sv.id_tipo = t.id
    INNER JOIN usuarios u_asesor ON p.id = u_asesor.id_persona
    INNER JOIN servicio_estudiante se_est ON sae.id = se_est.id_servicio
    INNER JOIN estudiantes e ON se_est.id_estudiante = e.id
    INNER JOIN personas p_estudiante ON e.id_persona = p_estudiante.id
    INNER JOIN usuarios u_estudiante ON p_estudiante.id = u_estudiante.id_persona;

    
select * from vw_allinfo;

/*
select vw.* from vw_info vw 
inner join material_servicio_asesor_espe msa on vw.id = msa.id_servicio_asesor_espe 
inner join servicio_asesor_espe sae on msa.id_servicio_asesor_espe = sae.id 
inner join servicio_estudiante se on sae.id_servicio = se.id_servicio 
inner join estudiantes e on se.id_estudiante = e.id 
inner join personas p on p.id = e.id_persona;

select * from material_servicio_asesor_espe msae
inner join servicio_asesor_espe sae on msae.id_servicio_asesor_espe = sae.id
join servicio_estudiante se on sae.id_servicio = se.id_servicio
;

select * from vw_info where vw_info.id_servicio not in (select id_servicio from servicio_estudiante where id_estudiante in (select e.id from estudiantes e join personas p on e.id_persona = p.id where e.id <> 1));
select * from vw_info;
select id from estudiantes where usuario = 'diego_d';

select * from estudiantes;
select * from personas;
select * from servicio_estudiantes;

select p.id from personas p join usuarios u on p.id = u.id_persona where u.usuario = 'diego_d';
select e.id from estudiantes e join personas p on e.id_persona = p.id;

select p.* from personas p join usuarios u on p.id = u.id_persona join estudiantes e on e.id = p.id_estudiante where u.usuario = 'diego_d';

select * from personas;
select * from usuarios;
select * from estudiantes;

select id_estudiante, id_servicio from servicio_estudiante;

select * from material_servicio_asesor_espe;
select * from servicio_asesor_espe;
select * from material_servicio_asesor_espe;
select * from servicio_estudiante;
drop view vw_allinfo;
select * from material_servicio_asesor_espe;
select * from usuarios;
select * from estudiantes;
*/