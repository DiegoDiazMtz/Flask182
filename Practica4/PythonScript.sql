-- drop database bebidas;
create database bebidas;
use bebidas;

create table Clasificaciones (
id int not null primary key auto_increment,
clasificacion varchar(50)
);

create table Marca (
id int not null primary key auto_increment,
Marca varchar(50)
);

CREATE TABLE Bebidas (
  id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  Nombre VARCHAR(50),
  Precio DECIMAL(10,2),
  id_clasificacion int not null,
  id_marca int not null,
  foreign key (id_clasificacion) references Clasificaciones(id) on delete cascade,
  foreign key (id_marca) references Marca(id) on delete cascade
);

-- create user 'almacenbeb'@'localhost' identified by '';
-- grant all privileges on bebidas.* to 'almacenbeb'@'localhost';

insert into Marca (Marca) values 
('Coca-Cola'),
('Ciel'),
('Fresca')
;

insert into Clasificaciones (clasificacion) values 
('Agua'),
('Bebida gaseosa')
;

insert into Bebidas (Nombre, Precio, id_clasificacion, id_marca) values
('Coca-Cola 600ml',18,2,1),
('Agua 600ml',14,1,1),
('Refresco 600ml',15,2,3);

select * from Marca;
select * from Clasificaciones;
select * from Bebidas;