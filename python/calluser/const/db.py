HOST="127.0.0.1"
USER="root"
PASSWD="abc"
DB="db"

START_URL_SQL = "SELECT id,name,url_slug,email,contactperpon FROM company WHERE email IS NOT NULL AND email <> '' limit 50"