CREATE USER admin WITH PASSWORD 'devpass';

CREATE DATABASE django_parser_db;
GRANT ALL PRIVILEGES ON DATABASE django_parser_db TO admin;