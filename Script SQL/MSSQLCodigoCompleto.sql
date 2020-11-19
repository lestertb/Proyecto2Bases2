--C�digo para el Monitor de privilegios

--Procedure retorna tablas de la base de datos usando
CREATE OR ALTER PROCEDURE getTables
AS
	BEGIN
		SELECT DISTINCT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
	END
GO

--EXEC getTables

--Procedure retorna privilegios de una tabla especifica.
CREATE OR ALTER PROCEDURE getPrivilegesXTable
	@nameTable VARCHAR(50)
AS
	BEGIN
		EXEC sp_table_privileges @nameTable
	END
GO

--EXEC getPrivilegesXTable personas

--Procedure retorna los atributos de una tabla
CREATE OR ALTER PROCEDURE getTableColumns
	@nameTable VARCHAR(50)
AS
	BEGIN
		SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = @nameTable;
	END
GO

--EXEC getTableColumns personas


--Procedure retorna privilegios de una columna especifica.
CREATE OR ALTER PROCEDURE getPrivilegesTablesXColumn
	@nameTable VARCHAR(50),
	@nameColumn VARCHAR(50)
AS
	BEGIN
		EXEC sp_column_privileges @nameTable, NULL, NULL, @nameColumn
	END
GO

--EXEC getPrivilegesTablesXColumn personas, nombre





--------Código para usar en python (Monitor)--------

--Retorna tablas de la base de datos usando
--GO
--SELECT DISTINCT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES


--Retorna privilegios de una tabla especifica.
--GO
--EXEC sp_table_privileges @nameTable


--Retorna los atributos de una tabla
--GO
--SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = @nameTable;


--Retorna privilegios de una columna especifica.
--GO
--EXEC sp_column_privileges @nameTable, NULL, NULL, @nameColumn



--------Código para usar en python (Plan de ejecusión)--------

--Este solo crea un link para mostrar el plan de ejecución en el Management
SET SHOWPLAN_XML OFF --(Plan estimado)
GO

--Este rea un link para mostrar el plan de ejecución en el Management junto a los valores de la tabla consultada
SET STATISTICS XML OFF --(Plan Real ó Actual)
GO

--Este muestra toda la información del plan de ejecución en formato consulta
SET SHOWPLAN_ALL OFF --(Algunos datos del plan estimado)
GO

--Este muestra toda la información del plan de ejecución en formato consulta y además la info de la tabla consultada o de lo que se consulte
SET STATISTICS PROFILE OFF --(Algunos datos del plan estimado, pero también retorna el resultado de la consulta)
GO


SELECT * FROM personas
GO


--Manejo de índices

--Procedure retorna indices

EXEC sp_helpindex 'personas'
GO

--Obtiene todos los índices de una tabla y de las vistas
SELECT
 name AS Index_Name,
 type_desc  As Index_Type,
 is_unique,
 OBJECT_NAME(object_id) As Table_Name
FROM
 sys.indexes
WHERE
 is_hypothetical = 0 AND
 index_id != 0 AND
 object_id = OBJECT_ID('view_Persona');
GO


CREATE OR ALTER VIEW dbo.view_Persona
WITH SCHEMABINDING
AS   
    SELECT idPersona, nombre, edad, cedula
	FROM dbo.personas
GO

CREATE UNIQUE CLUSTERED INDEX IX_view_Persona
ON dbo.view_Persona
(
     cedula ASC
)

select * from view_Persona

select * from personas

select * from usuarios

GO

--SELECT * FROM testSinPK

SELECT * FROM personas WITH (INDEX(IX_Edad_Personas))

--Indice 

CREATE NONCLUSTERED INDEX IX_Edad_Personas ON [personas] (edad)

