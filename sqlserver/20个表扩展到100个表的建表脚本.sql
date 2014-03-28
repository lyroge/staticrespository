

declare @sql varchar(2000)  
declare @suffix VARCHAR(2)
DECLARE @tablename1 VARCHAR(20)
DECLARE @tablename2 VARCHAR(20)

declare @i int
set @i = 21  

while @i < 100  
begin  
	SET @suffix = Rtrim(Ltrim(str(@i)))
	IF (@i < 10)
	BEGIN 
		SET @suffix = '0' + Rtrim(Ltrim(str(@i)))
	END 
	
	SET @tablename1 = 'tbNovelComment_' + @suffix
	SET @tablename2 = 'tbNovelReply_' + @suffix
	
	execute('if object_id('''+@tablename1+''') is not null  drop table ' + @tablename1)
    execute('if object_id('''+@tablename2+''') is not null  drop table ' + @tablename2)

	set @sql = '
CREATE TABLE tbNovelComment_' + @suffix + ' 
	(
	SonId              INT IDENTITY,
	CmtId              INT,
	CreatDatetime      DATETIME,
	LastUpdateDatetime DATETIME,
	CreatUserID        INT,
	CreatUserName      VARCHAR (64),
	CreatUserIP        VARCHAR (16),
	AuthorUserID       INT,
	AuthorUserName     VARCHAR (64),
	MainID             INT,
	MainTitle          VARCHAR (255),
	Subid              INT,
	SubTitle           VARCHAR (255),
	CmtTitle           VARCHAR (255),
	CmtContent         TEXT,
	IsPrivate          BIT,
	EliteIndex         TINYINT,
	TopIndex           TINYINT,
	ReplyCount         INT,
	AgreeCount         INT,
	CombatCount        INT,
	IsPass             BIT,
	IsOnLine           BIT,
	Source             INT,
	FontCount          INT,
	CommentImages      VARCHAR (256),
	CommentVideo       VARCHAR (512),
	CONSTRAINT PK_tbNovelComment_' + @suffix + ' PRIMARY KEY (SonId)
	);

CREATE INDEX tbNovelComment_' + @suffix + '_Cmt 
	ON tbNovelComment_' + @suffix + ' (CmtId);

CREATE INDEX tbNovelComment_' + @suffix + '_MainID
	ON tbNovelComment_' + @suffix + ' (MainID);
'  
	--PRINT @sql
	execute(@sql)
	
	set @sql = '
CREATE TABLE dbo.tbNovelReply_'+ @suffix +' 
	(
	ReplyId            INT IDENTITY,
	CmtID              INT,
	SonID              INT,
	MainID             INT,
	SubID              INT,
	CreatReplyDatetime DATETIME,
	CreatReplyUserID   INT,
	CreatReplyUserName VARCHAR (64),
	CreatReplyUserIP   VARCHAR (16),
	ReplyTitle         VARCHAR (256),
	ReplyContent       TEXT,
	IsOnLine           BIT,
	CONSTRAINT PK_tbNovelReply_'+ @suffix +' PRIMARY KEY (ReplyId)
	);
'  
	--PRINT @sql
	execute(@sql)	
	
	set @i = @i + 1  
end  