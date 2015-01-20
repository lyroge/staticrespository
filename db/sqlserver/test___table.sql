if object_id(N'testtable', 'U') is not null
	drop table testtable


create table testtable 
(
	id int identity(1,1) primary key,
	firstname varchar(20),
	lastname varchar(20),
	country varchar(20)
)

set identity_insert testtable on

declare @i int
set @i = 1
while @i<=20000
begin
	
	insert into testtable(id, firstname, lastname, country) values(@i, 'firstname_' + str(@i), 'lastname_' + str(@i), 'country_' + str(@i))
	set @i = @i + 1
end

set identity_insert testtable off