 
SELECT * FROM pre_forum_thread;
SELECT * FROM pre_forum_post_tableid;
SELECT * FROM pre_forum_post;
SELECT * FROM pre_forum_forum WHERE fid =2 ;
 
DELETE FROM pre_forum_thread;
DELETE FROM pre_forum_post_tableid;
DELETE FROM pre_forum_post;
UPDATE pre_forum_forum SET threads=0, posts=0, todayposts=0, lastpost='' WHERE fid=2

