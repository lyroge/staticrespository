

CREATE TABLE url_history
	(
	url    VARCHAR (100) NOT NULL,
	urlmd5 CHAR (32) NOT NULL
	);


ALTER TABLE url_history ADD INDEX IDX_URL_History_urlmd5(urlmd5);