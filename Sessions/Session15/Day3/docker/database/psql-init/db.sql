\set DB_NAME `echo "$DB_NAME"`
\set DB_USER `echo "$DB_USER"`
\set DB_PASSWORD `echo "$DB_PASSWORD"`
CREATE USER :DB_USER WITH PASSWORD :'DB_PASSWORD';
CREATE DATABASE :DB_NAME;
GRANT ALL PRIVILEGES ON DATABASE :DB_NAME TO :DB_USER;
ALTER ROLE :DB_USER CREATEDB;
\connect :DB_NAME;
CREATE TABLE public.imbd_directors
(
    director_id bigint,
    first_name text,
    last_name text
);
COPY public.imbd_directors FROM '/docker-entrypoint-initdb.d/IMDB-directors.csv' DELIMITER ',' CSV HEADER;
CREATE TABLE public.imbd_movies_directors
(   
    director_id bigint,
    movie_id bigint
);
COPY public.imbd_movies_directors FROM '/docker-entrypoint-initdb.d/IMDB-movies_directors.csv' DELIMITER ',' CSV HEADER;
CREATE TABLE public.imbd_movies_genres
(   
    movie_id bigint,
    genre text
);
COPY public.imbd_movies_genres FROM '/docker-entrypoint-initdb.d/IMDB-movies_genres.csv' DELIMITER ',' CSV HEADER;
