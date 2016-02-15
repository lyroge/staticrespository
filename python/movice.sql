create table video(
    `id` int(11) NOT NULL AUTO_INCREMENT primary key, 
    name varchar(50),
    cover varchar(200),
    lasttime varchar(50),
    tag varchar(20),
    url varchar(300)
)



create table video_child(
    `id` int(11) NOT NULL AUTO_INCREMENT primary key, 
    name varchar(50),
    url varchar(200),
    video_url varchar(200),
    video_id int(11)
)