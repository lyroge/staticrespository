 
SELECT * FROM pre_forum_thread;
SELECT * FROM pre_forum_post_tableid;
SELECT * FROM pre_forum_post;
SELECT * FROM pre_forum_forum WHERE fid =39 ;
SELECT * FROM pre_forum_threadclass;
SELECT * FROM url_history;

DELETE FROM pre_forum_thread;
DELETE FROM pre_forum_post_tableid;
DELETE FROM pre_forum_post;
DELETE FROM url_history;
UPDATE pre_forum_forum SET threads=0, posts=0, todayposts=0, lastpost='' WHERE fid=39

