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
SET STATISTICS XML ON --(Plan Real ó Actual)
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
GO
CREATE OR ALTER PROCEDURE getIndixes
	@nameTable VARCHAR(50)
AS
	BEGIN
		SELECT  Tab.name  Table_Name 
			 ,IX.name  Index_Name
			 ,IX.type_desc Index_Type
			 ,Col.name  Index_Column_Name
			 ,IXC.is_included_column Is_Included_Column
			 ,IX.fill_factor 
			 ,IX.is_disabled
			 ,IX.is_primary_key
			 ,IX.is_unique
			 		  
           FROM  sys.indexes IX 
           INNER JOIN sys.index_columns IXC  ON  IX.object_id   =   IXC.object_id AND  IX.index_id  =  IXC.index_id  
           INNER JOIN sys.columns Col   ON  IX.object_id   =   Col.object_id  AND IXC.column_id  =   Col.column_id     
           INNER JOIN sys.tables Tab      ON  IX.object_id = Tab.object_id 
		   WHERE Tab.name = 'personas'
	END
GO

--EXEC getIndixes personas

--Muestra todos los índices utilizados desde que inicio el servidor, ordenados primero los más recientes.
SELECT OBJECT_NAME(IX.OBJECT_ID) Table_Name
	   ,IX.name AS Index_Name
	   ,IX.type_desc Index_Type
	   ,SUM(PS.[used_page_count]) * 8 IndexSizeKB
	   ,IXUS.user_seeks AS NumOfSeeks
	   ,IXUS.user_scans AS NumOfScans
	   ,IXUS.user_lookups AS NumOfLookups
	   ,IXUS.user_updates AS NumOfUpdates
	   ,IXUS.last_user_seek AS LastSeek
	   ,IXUS.last_user_scan AS LastScan
	   ,IXUS.last_user_lookup AS LastLookup
	   ,IXUS.last_user_update AS LastUpdate
FROM sys.indexes IX
INNER JOIN sys.dm_db_index_usage_stats IXUS ON IXUS.index_id = IX.index_id AND IXUS.OBJECT_ID = IX.OBJECT_ID
INNER JOIN sys.dm_db_partition_stats PS on PS.object_id=IX.object_id
WHERE OBJECTPROPERTY(IX.OBJECT_ID,'IsUserTable') = 1
GROUP BY OBJECT_NAME(IX.OBJECT_ID) ,IX.name ,IX.type_desc ,IXUS.user_seeks ,IXUS.user_scans ,IXUS.user_lookups,IXUS.user_updates ,IXUS.last_user_seek ,IXUS.last_user_scan ,IXUS.last_user_lookup ,IXUS.last_user_update
ORDER BY IXUS.last_user_scan DESC



SELECT * FROM usuarios

GO

--SELECT * FROM testSinPK



SELECT * FROM personas WITH (INDEX(IX_Eada_Personas))

--Indice 

CREATE NONCLUSTERED INDEX IX_Edad_Personas ON [personas] (edad)

