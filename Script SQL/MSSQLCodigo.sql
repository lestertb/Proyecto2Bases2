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


--Procedure retorna indices

CREATE OR ALTER PROCEDURE getIndixes
	@nameTable VARCHAR(50)
AS
	BEGIN
		SELECT s.name AS schemaName, t.name AS tableName, i.name AS indexName, c.name AS columnName
		FROM sys.tables t
		INNER JOIN sys.schemas s on t.schema_id = s.schema_id
		INNER JOIN sys.indexes i on i.object_id = t.object_id
		INNER JOIN sys.index_columns ic on ic.object_id = t.object_id
		INNER JOIN sys.columns c on c.object_id = t.object_id
		AND ic.column_id = c.column_id
		WHERE t.name = @nameTable
	END
GO

--EXEC getIndixes personas

/*
SET SHOWPLAN_XML OFF

select * from usuarios FOR JSON PATH

*/




--------Código para usar en python--------

--Retorna tablas de la base de datos usando
GO
SELECT DISTINCT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES


--Retorna privilegios de una tabla especifica.
GO
EXEC sp_table_privileges @nameTable

--Retorna los atributos de una tabla
GO
SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = @nameTable;

--Retorna privilegios de una columna especifica.
GO
EXEC sp_column_privileges @nameTable, NULL, NULL, @nameColumn
