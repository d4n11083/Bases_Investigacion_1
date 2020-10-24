DROP TABLE Usuario cascade constraints;

CREATE TABLE Usuario(
    idUsuario NUMBER,
    nombreUsuario VARCHAR(100),
    direccionUsuario VARCHAR(100),
    PRIMARY KEY (idUsuario)
);


INSERT INTO USUARIO( idUsuario, nombreUsuario, direccionUsuario ) VALUES (1001,'Joshua', 'Heredia');
INSERT INTO USUARIO( idUsuario, nombreUsuario, direccionUsuario ) VALUES (1002,'Josue', 'Zarcero');
INSERT INTO USUARIO( idUsuario, nombreUsuario, direccionUsuario ) VALUES (1003,'David', 'Grecia???');

SELECT * FROM USUARIO;

