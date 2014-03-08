 
declare @sql varchar(5000)  
declare @suffix VARCHAR(2)
DECLARE @tablename1 VARCHAR(20)
DECLARE @tablename2 VARCHAR(20)
DECLARE @tablename3 VARCHAR(20)
DECLARE @tablename4 VARCHAR(20)

declare @i int
set @i = 0  

while @i < 21
begin  
	SET @suffix = Rtrim(Ltrim(str(@i)))
	IF (@i < 10)
	BEGIN 
		SET @suffix = '0' + Rtrim(Ltrim(str(@i)))
	END 
	
	SET @tablename3 = 'tbNovelComment_' + @suffix
	SET @tablename4 = 'tbNovelReply_' + @suffix
	
	set @sql = 'declare mycursor cursor for select CmtId,SonId,CreatDatetime,CreatUserID,AuthorUserID,AuthorUserName,MainID,MainTitle,CmtTitle,CmtContent,Source,CommentImages,CommentVideo from ' + @tablename3 + ' 
	open mycursor 	
	declare @sql varchar(1000), @tablesuffix varchar(2), @cmtid int, @sonid int, @CreatDatetime datetime, @CreatUserID varchar(20), @AuthorUserID varchar(20), 
	@AuthorUserName varchar(64), @MainID varchar(20), @MainTitle varchar(255), @CmtTitle varchar(255),@Source int, @CommentImages varchar(255), @CommentVideo varchar(512), @CmtContent varchar(8000)
   
	fetch next from mycursor into @cmtid,@sonid,@CreatDatetime,@CreatUserID,@AuthorUserID,@AuthorUserName,@MainID,@MainTitle,@CmtTitle,@CmtContent,@Source,@CommentImages,@CommentVideo
	while @@fetch_status=0 
	begin 
	set @tablesuffix = @CreatUserID % 100	   
	IF (@tablesuffix < 10)
	BEGIN 
		SET @tablesuffix = ''0'' + Rtrim(Ltrim(str(@tablesuffix)))
	END 		  
	
	set @CmtTitle = dbo.getUserCommentTitle(@Source, @CmtTitle, @CmtContent,@MainTitle,@CommentImages,@CommentVideo)
	
	set @sql = ''INSERT INTO tbUserComment_'' + @tablesuffix + ''(CmtId,SonId,CreatDatetime,CreatUserID, AuthorUserID, AuthorUserName, MainID, MainTitle, CmtTitle) 
	VALUES('' + Rtrim(Ltrim(str(@cmtid)))+ '','' + Rtrim(Ltrim(str(@sonid))) +  '','''''' + Rtrim(Ltrim(@CreatDatetime)) + '''''','' + 
	Rtrim(Ltrim(str(@CreatUserID))) +  '','' + Rtrim(Ltrim(str(@AuthorUserID))) + '','''''' + Rtrim(Ltrim(@AuthorUserName)) + '''''',''''''+ Rtrim(Ltrim(str(@MainID))) + 
	'''''','''''' + Rtrim(Ltrim(@MainTitle)) + '''''','''''' + Rtrim(Ltrim(@CmtTitle)) + '''''')''
	print @sql
    execute(@sql) 
	fetch next from mycursor into @cmtid,@sonid,@CreatDatetime,@CreatUserID,@AuthorUserID,@AuthorUserName,@MainID,@MainTitle,@CmtTitle,@CmtContent,@Source,@CommentImages,@CommentVideo
	END 
	close mycursor 
	deallocate mycursor 
	'	   
    execute(@sql)
    
    -- dbo.tbUserReply_xx
    set @sql = 'declare mycursor cursor for select ReplyId,a.CmtId,a.SonId,CreatReplyDatetime,CreatReplyUserID,ReplyTitle,b.MainID,b.MainTitle, b.AuthorUserID,b.AuthorUserName from ' + @tablename4 + ' a join '+@tablename3 +' b on a.sonid=b.sonid
	open mycursor 	
	declare @sql varchar(1000), @tablesuffix varchar(2),@ReplyId int, @cmtid int, @sonid int, @CreatReplyDatetime datetime, @CreatReplyUserID varchar(20), @ReplyTitle varchar(255),
	@MainID int, @MainTitle varchar(255), @AuthorUserID int, @AuthorUserName varchar(64)
   
	fetch next from mycursor into @ReplyId,@cmtid,@sonid,@CreatReplyDatetime,@CreatReplyUserID,@ReplyTitle,@MainID,@MainTitle,@AuthorUserID,@AuthorUserName
	while @@fetch_status=0 
	begin 
	set @tablesuffix = @CreatReplyUserID % 100	   
	IF (@tablesuffix < 10)
	BEGIN 
		SET @tablesuffix = ''0'' + Rtrim(Ltrim(str(@tablesuffix)))
	END 		 		
			
	set @sql = ''INSERT INTO tbUserReply_'' + @tablesuffix + ''(ReplyId,CmtId,SonId,CreatReplyDatetime,CreatUserID, AuthorUserID, AuthorUserName, MainID, MainTitle, ReplyTitle) 
	VALUES('' + Rtrim(Ltrim(str(@ReplyId)))+ '','' + Rtrim(Ltrim(str(@cmtid)))+ '','' + Rtrim(Ltrim(str(@sonid))) +  '','''''' + Rtrim(Ltrim(@CreatReplyDatetime)) + '''''','' + 
	Rtrim(Ltrim(str(@CreatReplyUserID))) +  '','' + Rtrim(Ltrim(str(@AuthorUserID))) + '','''''' + Rtrim(Ltrim(@AuthorUserName)) + '''''',''''''+ Rtrim(Ltrim(str(@MainID))) + 
	'''''','''''' + Rtrim(Ltrim(@MainTitle)) + '''''','''''' + Rtrim(Ltrim(isnull(@ReplyTitle,''''))) + '''''')''
	print @sql
    execute(@sql) 
	fetch next from mycursor into @ReplyId,@cmtid,@sonid,@CreatReplyDatetime,@CreatReplyUserID,@ReplyTitle,@MainID,@MainTitle,@AuthorUserID,@AuthorUserName
	END 
	close mycursor 
	deallocate mycursor 
	'	   
    execute(@sql)
  
	set @i = @i + 1  
end  