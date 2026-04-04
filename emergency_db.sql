--
-- PostgreSQL database dump
--

\restrict KngVOoTJebZlhaCwJefyQ1RKy3h8wkAE0UGkF6BedMaxV9zIqQCBShNUQWFBXu6

-- Dumped from database version 18.3 (Debian 18.3-1.pgdg13+1)
-- Dumped by pg_dump version 18.3 (Debian 18.3-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: records; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.records (
    id integer NOT NULL,
    amount integer,
    type text,
    category text,
    date text,
    note text
);


ALTER TABLE public.records OWNER TO admin;

--
-- Name: records_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.records_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.records_id_seq OWNER TO admin;

--
-- Name: records_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.records_id_seq OWNED BY public.records.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name text,
    role text,
    active boolean DEFAULT true
);


ALTER TABLE public.users OWNER TO admin;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO admin;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: records id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.records ALTER COLUMN id SET DEFAULT nextval('public.records_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: records; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.records (id, amount, type, category, date, note) FROM stdin;
1	5000	income	salary	2026-04-02	salary
2	5000	income	salary	2026-04-02	salary
3	5000	income	salary	2026-04-02	salary
4	5000	income	salary	2026-04-02	salary
5	5000	income	salary	2026-04-02	salary
6	5000	income	salary	2026-04-02	salary
7	5000	income	salary	2026-04-02	salary
8	5000	income	salary	2026-04-02	salary
9	5000	income	salary	2026-04-02	salary
10	5000	income	salary	2026-04-02	salary
11	5000	income	salary	2026-04-02	salary
12	5000	income	salary	2026-04-02	salary
13	5000	income	salary	2026-04-02	salary
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.users (id, name, role, active) FROM stdin;
1	Aviral	admin	t
2	Yash	viewer	t
3	Yana	analyst	t
\.


--
-- Name: records_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.records_id_seq', 13, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.users_id_seq', 6, true);


--
-- Name: records records_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.records
    ADD CONSTRAINT records_pkey PRIMARY KEY (id);


--
-- Name: users users_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_name_key UNIQUE (name);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

\unrestrict KngVOoTJebZlhaCwJefyQ1RKy3h8wkAE0UGkF6BedMaxV9zIqQCBShNUQWFBXu6

