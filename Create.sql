-- Database: kp5

-- DROP DATABASE IF EXISTS kp5;

CREATE DATABASE kp5
    WITH
    OWNER = postgresa
    ENCODING = 'UTF8'
    LC_COLLATE = 'ru_RU.UTF-8'
    LC_CTYPE = 'ru_RU.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

CREATE TABLE public.employers
(
    id integer,
    name character varying(250),
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public.employers
    OWNER to postgres;


CREATE TABLE public.vacancies
(
    id integer,
    employer_id integer,
    name character varying(250),
    alternate_url character varying(250),
    published_at date,
    area character varying(250),
    salary_from numeric(12, 2),
    salary_to numeric(12, 2),0
    salary_currency character varying(50),
    salary numeric(12, 2),
    PRIMARY KEY (if)
);

ALTER TABLE IF EXISTS public.vacancies
    OWNER to postgres;