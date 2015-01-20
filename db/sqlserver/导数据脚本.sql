

declare @i INT
declare @j INT
declare @suffixi varchar(2)
declare @suffixj varchar(2)
DECLARE @sql VARCHAR(1000)

SET @i = 0
SET @j = 21
WHILE @j < 100
BEGIN 
	SET @suffixj = Rtrim(Ltrim(str(@j)))
	SET @sql = 'delete from tbNovelComment_' + @suffixj + ' '	
	--execute(@sql)
	SET @sql = 'delete from tbNovelReply_' + @suffixj + ' '	
	--execute(@sql)	
	SET @j = @j + 1
END 		


while @i < 21
BEGIN
   	SET @suffixi = Rtrim(Ltrim(str(@i)))
	IF (@i < 10)
	BEGIN 
		SET @suffixi = '0' + Rtrim(Ltrim(str(@i)))
	END
	
	SET @j = 21
	
	WHILE @j < 100
	BEGIN 
	SET @suffixj = Rtrim(Ltrim(str(@j)))
	SET @sql = '
	SET IDENTITY_INSERT tbNovelComment_'+@suffixj +' ON ;
	INSERT INTO tbNovelComment_' +@suffixj + '(SonId, CmtId, CreatDatetime, LastUpdateDatetime, CreatUserID, CreatUserName, CreatUserIP, AuthorUserID, AuthorUserName, MainID, MainTitle, Subid, SubTitle, CmtTitle, CmtContent, IsPrivate, EliteIndex, TopIndex, ReplyCount, AgreeCount, CombatCount, IsPass, IsOnLine, Source, FontCount, CommentImages, CommentVideo ) 
	SELECT SonId, CmtId, CreatDatetime, LastUpdateDatetime, CreatUserID, CreatUserName, CreatUserIP, AuthorUserID, AuthorUserName, MainID, MainTitle, Subid, SubTitle, CmtTitle, CmtContent, IsPrivate, EliteIndex, TopIndex, ReplyCount, AgreeCount, CombatCount, IsPass, IsOnLine, Source, FontCount, CommentImages, CommentVideo 
	FROM tbNovelComment_'+@suffixi+' WHERE MainID % 100 = '+@suffixj +'
	SET IDENTITY_Insert tbNovelComment_'+@suffixj +' OFF '
	execute(@sql)
	--PRINT @sql		
	SET @j = @j + 1
	END 		
	set @i = @i + 1  
END


SET @i = 0
SET @j = 21
while @i < 21
BEGIN
   	SET @suffixi = Rtrim(Ltrim(str(@i)))
	IF (@i < 10)
	BEGIN 
		SET @suffixi = '0' + Rtrim(Ltrim(str(@i)))
	END
	SET @j = 21
	WHILE @j < 100
	BEGIN 
	SET @suffixj = Rtrim(Ltrim(str(@j)))
	SET @sql = '
	SET IDENTITY_INSERT tbNovelReply_'+@suffixj +' ON ;
	INSERT INTO tbNovelReply_' +@suffixj + '(ReplyId, CmtID, SonID, MainID, SubID, CreatReplyDatetime, CreatReplyUserID, CreatReplyUserName, CreatReplyUserIP, ReplyTitle, ReplyContent, IsOnLine) 
	SELECT ReplyId, CmtID, SonID, MainID, SubID, CreatReplyDatetime, CreatReplyUserID, CreatReplyUserName, CreatReplyUserIP, ReplyTitle, ReplyContent, IsOnLine
	FROM tbNovelReply_'+@suffixi+' WHERE MainID % 100 = '+@suffixj +'
	SET IDENTITY_Insert tbNovelReply_'+@suffixj +' OFF '
	execute(@sql)
	--PRINT @sql		
	SET @j = @j + 1
	END 		
	set @i = @i + 1  
END