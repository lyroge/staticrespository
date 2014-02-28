
declare @sql varchar(1000)  
declare @suffix VARCHAR(2)
DECLARE @tablename1 VARCHAR(20)
DECLARE @tablename2 VARCHAR(20)

declare @i int
set @i = 0  

while @i < 100  
begin  
	SET @suffix = Rtrim(Ltrim(str(@i)))
	IF (@i < 10)
	BEGIN 
		SET @suffix = '0' + Rtrim(Ltrim(str(@i)))
	END 
	
	SET @tablename1 = 'tbUserComment_' + @suffix
	SET @tablename2 = 'tbUserReply_' + @suffix
	
	execute('if object_id('''+@tablename1+''') is not null  drop table ' + @tablename1)
	execute('if object_id('''+@tablename2+''') is not null  drop table ' + @tablename2)

	set @sql = '
CREATE TABLE tbUserComment_' + @suffix + '
(
CmtId INT,
SonId INT,
CreatDatetime DATETIME,
CreatUserID INT,
AuthorUserID INT,
AuthorUserName VARCHAR(64),
MainID INT ,
MainTitle VARCHAR(255),
CmtTitle VARCHAR(255)
)'  
	--PRINT @sql
	execute(@sql)
	
	set @sql = '
CREATE TABLE tbUserReply_'+ @suffix +'
(
ReplyId int,
CmtId INT,
SonId INT,
CreatReplyDatetime DATETIME,
CreatUserID INT,
AuthorUserID INT,
AuthorUserName VARCHAR(64),
MainID INT,
MainTitle VARCHAR(255),
ReplyTitle VARCHAR(255)
)
'  
	--PRINT @sql
	execute(@sql)	
	
	set @i = @i + 1  
end  


--set @SQL = ' select @Count=count(1) from tbCommentEditorTemp '  + @op ;
--declare @c int
--exec sp_executesql @SQL, N'@Count int out', @c out