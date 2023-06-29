-- drop database yourSpace;
create database yourSpace; 
use yourSpace;

create table roles (
id int not null primary key auto_increment,
rol varchar (20)
);
insert into roles(rol)
values
('asesor'),
('asesorado');
select * from roles;
create table materias (
id int not null primary key auto_increment,
nombre varchar (50),
descripcion varchar (1000)
);
insert into materias (nombre, descripcion)
values
('Matematicas', 'Estudia las propiedades y relaciones de los números, las formas geométricas y los patrones matemáticos.'),
('Ciencias Naturales', 'Comprende los fenómenos y leyes que gobiernan el mundo natural, incluyendo la biología (estudio de los seres vivos), la química (propiedades de la materia) y la física (interacciones de la energía y la materia).'),
('Historia', 'Explora los eventos pasados y su influencia en la sociedad, analizando cambios políticos, económicos, sociales y culturales.	'),
('Lenguaje y Literatura', 'Desarrolla habilidades de comunicación oral y escrita, así como la comprensión e interpretación de textos literarios y no literarios.'),
('Geografia', 'Estudia la Tierra y sus características físicas, políticas, sociales y culturales, así como los patrones espaciales de la humanidad.'),
('Educacion Fisica', 'Promueve la actividad física y el desarrollo de habilidades motrices, la importancia de la salud y el bienestar.'),
('Artes', 'Explora diferentes expresiones artísticas como la música, la pintura y el teatro, fomentando la creatividad y la apreciación estética.'),
('Idiomas', 'Enseña habilidades lingüísticas y comunicativas en diferentes idiomas, lo que facilita la comunicación y el entendimiento intercultural.'),
('Economia', 'Analiza la producción, distribución y consumo de bienes y servicios, así como el estudio de los sistemas económicos y las políticas relacionadas.'),
('Informatica', 'Introduce conceptos y habilidades relacionadas con el uso de la tecnología, programación, hardware y software, así como la resolución de problemas tecnológicos.');
select * from materias;
SELECT nombre FROM materias where nombre = 'Matematicas';

create table horarios (
id int not null primary key auto_increment,
horario datetime
);
insert into horarios(horario)
values
('2023-03-01 08:30:00'),
('2023-03-02 06:15:22'),
('2023-03-03 08:40:00'),
('2023-03-08 05:25:11'),
('2023-03-10 09:30:25'),
('2023-03-13 22:50:17'),
('2023-03-14 08:35:16'),
('2023-03-04 10:30:50'),
('2023-03-07 08:10:45'),
('2023-03-05 09:25:11');
select * from horarios;

create table localizaciones (
id int not null primary key auto_increment,
nombre varchar (50),
descripcion varchar (200)
);
insert into localizaciones(nombre, descripcion)
values
('Edificio A','Se encuentra cerca de la cafeteria chica, dentro del eidificio se encuentra un cajero de BBVA'),
('Edificio B','Se encuentra al lado del edificio B, de frente a la entrada principal de la universidad, el salon se encuentra en el segungo piso'),
('Edificio C','Se encuentra atras del edificio B y de frente tiene el LT1, es el ultimo edificio de la parte de atras de la universidad'),
('Edificio D','Se encuntre al frende de la cafeteria, de la entrada de la universidad a mando derecha, dentro del edificio esta la papeleria y control escolar'),
('LT1','Se encuantra al lado del edificio B, arriba de fabrica de ideas'),
('LT2','Se encuentra al lado del edificio B y del LT1'),
('Cafeteria','Se encuentra en la parte de atras del edificio D atras de la cafateria esta el estaciomaniento'),
('Sala 3D','Se encuntra al lado del edifcio A y de frente le queda la cafe chica'),
('Cafe Chica','Esta frente a la Sala 3D y de frete de la cafe chica estan las canchas'),
('Cubiculo','Todos los cubiculos se encuentran en la pare de arriba de los edificios');
select * from localizaciones;

create table usuarios (
id int not null primary key auto_increment,
nombre varchar (50),
apellido_paterno varchar (50),
apellido_materno varchar (50),
id_rol int not null,
foreign key (id_rol) references roles (id) on delete cascade on update cascade
);
insert into usuarios(nombre, apellido_paterno, apellido_materno, id_rol)
values
('Alejandro', 'López', 'García', '1'),
('Sofía', 'Rodríguez', 'Morales', '2'),
('Juan Carlos', 'Torres ', 'Navarro', '1'),
('Valentina', 'Martínez', 'Jiménez', '2'),
('Andrés', 'Pérez', 'Silva', '1'),
('Isabella', 'González', 'Ruiz', '2'),
('Daniel', 'Ramírez', 'Castro', '1'),
('Camila', 'Herrera', 'Vargas', '2'),
('Eduardo', 'Castro', 'López', '1'),
('Ana', 'Torres', 'Rodríguez', '2');
select * from usuarios;

create table cursos (
id int not null primary key auto_increment,
id_usuario int not null,
foreign key (id_usuario) references usuarios (id) on delete cascade on update cascade,
id_materia int not null,
foreign key (id_materia) references materias (id) on delete cascade on update cascade,
id_horario int not null,
foreign key (id_horario) references horarios (id) on delete cascade on update cascade,
id_locacion int not null,
foreign key (id_locacion) references locaciones (id) on delete cascade on update cascade
);
insert into cursos(id_usuario, id_materia, id_horario, id_locacion)
values
('1','10','1','2'),
('2','9','2','1'),
('3','8','4','3'),
('4','7','3','4'),
('5','6','5','6'),
('6','5','6','5'),
('7','4','8','7'),
('8','3','7','8'),
('9','2','9','10'),
('10','1','10','9');

-- select * from cursos;*
