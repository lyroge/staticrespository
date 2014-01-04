HOST="127.0.0.1"
USER="root"
PASSWD="abc"
DB="fbm"

START_URL_SQL = '''SELECT a.*,c.email FROM inquires a join company c on a.companyid=c.id 
WHERE issend = 0 AND c.email IS NOT NULL AND c.email <> '' AND c.email<>'error' AND c.email <> 'email not found from contact' '''

EMAIL_USERNAME = 'email'
EMAIL_PASSWORD = 'pwd'