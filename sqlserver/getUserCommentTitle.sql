
create  FUNCTION [dbo].[getUserCommentTitle] 
(	
	@Source INT,
	@CmtTitle VARCHAR(255),
	@CmtContent TEXT,
	@MainTitle VARCHAR(255),
	@CommentImages varchar(255),
	@CommentVideo varchar(512)
)
RETURNS varchar(255)
AS
BEGIN
	DECLARE @title VARCHAR(255)
	SET @title = @CmtTitle 
	IF (@Source >= 1 AND @source <=7)
	begin
		IF @Source = 1 
	   	SET @title = '‘˘ÀÕœ ª®£°'
		IF @Source = 2 
	   	SET @title = '»”∏ˆº¶µ∞£°'
	   	IF @Source = 3 
	   	SET @title = '‘˘√∂◊Í Ø£°'
	   	IF @Source = 4 
	   	SET @title = '”˛Œ™…Ò± £°'
	   	IF @Source = 5 
	   	SET @title = '±… ”ÀŸ∂»£°'
	   	IF @Source = 6
	   	SET @title = '≥Â±≠øß∑»£°'
	   	IF @Source = 7 
	   	SET @title = 'ÀÕ∫…∞¸¿≤£°'	   	
	   	SET @title = 'Œ™' + @MainTitle + @title
	   	RETURN @title
   	END 
   	
   	IF @CommentImages IS NOT NULL OR @CommentImages <> ''
   	BEGIN
   		IF @CmtTitle IS NULL OR @CmtTitle = ''
   		BEGIN
   			SET @title = ltrim(rtrim(substring(@CmtContent, 1, 46)))  + '(Õº∆¨)'
   		END 
   		ELSE
   		BEGIN
   			SET @title = @CmtTitle + '(Õº∆¨)'
   		END
   	END 
   	
   	
   	IF @CommentVideo IS NOT NULL OR @CommentVideo <> ''
   	BEGIN
   		IF @CmtTitle IS NULL OR @CmtTitle = ''
   		BEGIN
   			SET @title = ltrim(rtrim(substring(@CmtContent, 1, 46)))  + '( ”∆µ)'
   		END 
   		ELSE
   		BEGIN
   			SET @title = @CmtTitle + '( ”∆µ)'
   		END
   	END 
   	
   	IF @title IS NULL OR @title = ''
   		SET @title = ltrim(rtrim(substring(@CmtContent, 1, 50)))
   	
   	RETURN @title
END

