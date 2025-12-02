CREATE DATABASE habits;
CREATE USER habits_user WITH ENCRYPTED PASSWORD 'habits_password';
GRANT ALL PRIVILEGES ON DATABASE habits TO habits_user;
ALTER DATABASE habits OWNER TO habits_user;