--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.20
-- Dumped by pg_dump version 9.6.20

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public.account DROP CONSTRAINT account_status_fkey;
ALTER TABLE ONLY public.account DROP CONSTRAINT account_role_fkey;
ALTER TABLE ONLY public.account DROP CONSTRAINT account_phone_uuid_fkey;
ALTER TABLE ONLY public.account DROP CONSTRAINT account_avatar_uuid_fkey;
ALTER TABLE ONLY public.account DROP CONSTRAINT account_address_uuid_fkey;
ALTER TABLE ONLY public.status DROP CONSTRAINT status_pkey;
ALTER TABLE ONLY public.role DROP CONSTRAINT role_pkey;
ALTER TABLE ONLY public.phone DROP CONSTRAINT phone_pkey;
ALTER TABLE ONLY public.avatar DROP CONSTRAINT avatar_pkey;
ALTER TABLE ONLY public.address DROP CONSTRAINT address_pkey;
ALTER TABLE ONLY public.account DROP CONSTRAINT account_uuid_key;
ALTER TABLE ONLY public.account DROP CONSTRAINT account_username_key;
ALTER TABLE ONLY public.account DROP CONSTRAINT account_pkey;
ALTER TABLE ONLY public.account DROP CONSTRAINT account_email_key;
DROP TABLE public.status;
DROP TABLE public.role;
DROP TABLE public.phone;
DROP TABLE public.avatar;
DROP TABLE public.address;
DROP TABLE public.account;
DROP TYPE public.statusenum;
DROP TYPE public.roleenum;
DROP EXTENSION plpgsql;
DROP SCHEMA public;
--
-- Name: public; Type: SCHEMA; Schema: -; Owner: account
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO account;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: account
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: roleenum; Type: TYPE; Schema: public; Owner: account
--

CREATE TYPE public.roleenum AS ENUM (
    'member',
    'admin',
    'root'
);


ALTER TYPE public.roleenum OWNER TO account;

--
-- Name: statusenum; Type: TYPE; Schema: public; Owner: account
--

CREATE TYPE public.statusenum AS ENUM (
    'pending',
    'active',
    'inactive'
);


ALTER TYPE public.statusenum OWNER TO account;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: account; Type: TABLE; Schema: public; Owner: account
--

CREATE TABLE public.account (
    uuid uuid NOT NULL,
    ctime bigint,
    mtime bigint,
    membership_uuid uuid NOT NULL,
    email character varying(255) NOT NULL,
    username character varying(255) NOT NULL,
    first_name character varying,
    last_name character varying,
    status public.statusenum NOT NULL,
    role public.roleenum NOT NULL,
    address_uuid uuid,
    phone_uuid uuid,
    avatar_uuid uuid
);


ALTER TABLE public.account OWNER TO account;

--
-- Name: address; Type: TABLE; Schema: public; Owner: account
--

CREATE TABLE public.address (
    uuid uuid NOT NULL,
    ctime bigint,
    mtime bigint,
    line_1 character varying NOT NULL,
    line_2 character varying,
    city character varying NOT NULL,
    province character varying NOT NULL,
    country character varying(2) NOT NULL,
    postal_code character varying NOT NULL
);


ALTER TABLE public.address OWNER TO account;

--
-- Name: avatar; Type: TABLE; Schema: public; Owner: account
--

CREATE TABLE public.avatar (
    uuid uuid NOT NULL,
    ctime bigint,
    mtime bigint,
    s3_filename character varying NOT NULL,
    filename character varying NOT NULL
);


ALTER TABLE public.avatar OWNER TO account;

--
-- Name: phone; Type: TABLE; Schema: public; Owner: account
--

CREATE TABLE public.phone (
    uuid uuid NOT NULL,
    ctime bigint,
    mtime bigint,
    _number character varying(20) NOT NULL,
    country_code character varying(8) NOT NULL,
    extension character varying(20)
);


ALTER TABLE public.phone OWNER TO account;

--
-- Name: role; Type: TABLE; Schema: public; Owner: account
--

CREATE TABLE public.role (
    ctime bigint,
    mtime bigint,
    name public.roleenum NOT NULL
);


ALTER TABLE public.role OWNER TO account;

--
-- Name: status; Type: TABLE; Schema: public; Owner: account
--

CREATE TABLE public.status (
    ctime bigint,
    mtime bigint,
    name public.statusenum NOT NULL
);


ALTER TABLE public.status OWNER TO account;

--
-- Data for Name: account; Type: TABLE DATA; Schema: public; Owner: account
--

COPY public.account (uuid, ctime, mtime, membership_uuid, email, username, first_name, last_name, status, role, address_uuid, phone_uuid, avatar_uuid) FROM stdin;
3e8ad9ff-ee52-442e-b50d-47488294c535	1604092401657	1604092564079	060db114-e23f-429d-80b7-36a14b2b3de7	dallan.bhatti@techtapir.com	dallan	Dallan	Bhatti	active	member	95d5ef02-b8de-4ccf-aa43-1287330ddc0f	30d68893-6502-4614-83a9-2bc741d44556	5f81f0ed-6e23-45e2-aed2-d46c8537f21f
646601b4-9805-4d0c-92f0-f76168221de2	1604092638934	1604092665858	532089b9-f28f-40c4-83d3-aef1df1d2d48	ross@sfu.ca	ross	Ross	Stevenson	active	member	bec78118-7ea6-4cd9-825d-c37fc7a1910c	de2aea54-7990-4ded-b3b4-7c3376fe8011	e4a57b6f-641e-411a-bd68-ff82f344838f
afe7213a-cbcc-4aa6-bf5c-f8b458fbffeb	1604092703571	1604092775463	542a8447-e2e8-4b6d-8a2a-97a9f04d4ce6	david@sfu.ca	david	David	Yeager	active	member	d1c4fd8a-6017-409e-9610-ad1eb4fe2eaa	eee20b5f-de48-4281-a1ad-eac88286600d	6ce8dd7c-a2e5-4fa8-bbad-b968af597247
4ffe400a-2ab3-494b-a0d4-9fe0bc92a584	1606244664355	1606244747475	bf759ec2-afd2-45a9-915e-7d43cab4acd8	kai@sfu.ca	kai	Kai	Somers	active	member	b7d8bcf7-3a42-4b7c-adc2-debca7d24deb	f2727107-9273-4f46-a8ae-ec2f6b67414c	1764db97-32e6-4c21-8d2b-46bf43a00435
62cfcfc0-1e12-4f62-aeac-ff9cf30bddbc	1606244784056	1606244853924	5f2ec7c6-7152-4272-a805-5c52eaf52eb6	liam@sfu.ca	liam	Liam	O'Shaugnessy	active	member	4f67865d-5b3c-40d3-9444-1abd38984dc2	bbe3804d-bbfd-4f5d-8516-aab8b8c247b8	426bd9a1-0649-4518-8e83-7093865cd4ce
90fac9af-4eca-4dae-9cc4-01f7e8d39ed7	1606244890430	1606244977957	02f40727-bbcf-4edf-937f-0d5fd9c27d05	kurt@sfu.ca	kurt	Kurt	Bell	active	member	525c72d6-b4cb-431b-ac67-a2bab5341663	ab537ecb-e70f-49e4-b619-80d20c9304ac	86f8ce40-3048-4679-9709-4ed7ca09530a
\.


--
-- Data for Name: address; Type: TABLE DATA; Schema: public; Owner: account
--

COPY public.address (uuid, ctime, mtime, line_1, line_2, city, province, country, postal_code) FROM stdin;
95d5ef02-b8de-4ccf-aa43-1287330ddc0f	1604092562595	\N	1838 Riverside Drive	\N	North Vancouver	British Columbia	CA	V7H 1V7
bec78118-7ea6-4cd9-825d-c37fc7a1910c	1604092665759	\N	1837 Riverside Drive	\N	North Vancouver	British Columbia	CA	V7H1V6
d1c4fd8a-6017-409e-9610-ad1eb4fe2eaa	1604092772906	\N	1836 Riverside Drive	\N	North Vancouver	British Columbia	CA	V7H1V5
b7d8bcf7-3a42-4b7c-adc2-debca7d24deb	1606244745054	\N	1835 Riverside Drive	\N	North Vancouver	British Columbia	CA	V7A 1V7
4f67865d-5b3c-40d3-9444-1abd38984dc2	1606244851125	\N	1834 Riverside Drive	\N	North Vancouver	British Columbia	CA	V7A 1V6
525c72d6-b4cb-431b-ac67-a2bab5341663	1606244977100	\N	1833 Riverside Drive	\N	North Vancouver	British Columbia	CA	V7A 1V5
\.


--
-- Data for Name: avatar; Type: TABLE DATA; Schema: public; Owner: account
--

COPY public.avatar (uuid, ctime, mtime, s3_filename, filename) FROM stdin;
5f81f0ed-6e23-45e2-aed2-d46c8537f21f	1604092564057	\N	060db114-e23f-429d-80b7-36a14b2b3de7.jpeg	techtapir_avatar.jpeg
e4a57b6f-641e-411a-bd68-ff82f344838f	1604092665693	\N	532089b9-f28f-40c4-83d3-aef1df1d2d48.jpg	Rick-Ross-e1439528528453.jpg
6ce8dd7c-a2e5-4fa8-bbad-b968af597247	1604092775412	\N	542a8447-e2e8-4b6d-8a2a-97a9f04d4ce6.jpg	2009_Nissan_Xterra_--_08-29-2009.jpg
1764db97-32e6-4c21-8d2b-46bf43a00435	1606244747439	\N	bf759ec2-afd2-45a9-915e-7d43cab4acd8.png	kingkai.png
426bd9a1-0649-4518-8e83-7093865cd4ce	1606244853896	\N	5f2ec7c6-7152-4272-a805-5c52eaf52eb6.png	shaggy.png
86f8ce40-3048-4679-9709-4ed7ca09530a	1606244977933	\N	02f40727-bbcf-4edf-937f-0d5fd9c27d05.png	ham.png
\.


--
-- Data for Name: phone; Type: TABLE DATA; Schema: public; Owner: account
--

COPY public.phone (uuid, ctime, mtime, _number, country_code, extension) FROM stdin;
30d68893-6502-4614-83a9-2bc741d44556	1604092562702	\N	(778) 871-4225	CA	\N
de2aea54-7990-4ded-b3b4-7c3376fe8011	1604092665806	\N	(778) 871-4226	CA	\N
eee20b5f-de48-4281-a1ad-eac88286600d	1604092772922	\N	(778) 871-4227	CA	\N
f2727107-9273-4f46-a8ae-ec2f6b67414c	1606244745207	\N	(778) 871-4223	CA	\N
bbe3804d-bbfd-4f5d-8516-aab8b8c247b8	1606244851149	\N	(778) 871-4222	CA	\N
ab537ecb-e70f-49e4-b619-80d20c9304ac	1606244977122	\N	(778) 871-4221	CA	\N
\.


--
-- Data for Name: role; Type: TABLE DATA; Schema: public; Owner: account
--

COPY public.role (ctime, mtime, name) FROM stdin;
1604091744077	\N	member
1604091744077	\N	admin
1604091744077	\N	root
\.


--
-- Data for Name: status; Type: TABLE DATA; Schema: public; Owner: account
--

COPY public.status (ctime, mtime, name) FROM stdin;
1604091744033	\N	pending
1604091744033	\N	active
1604091744033	\N	inactive
\.


--
-- Name: account account_email_key; Type: CONSTRAINT; Schema: public; Owner: account
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_email_key UNIQUE (email);


--
-- Name: account account_pkey; Type: CONSTRAINT; Schema: public; Owner: account
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_pkey PRIMARY KEY (uuid, membership_uuid);


--
-- Name: account account_username_key; Type: CONSTRAINT; Schema: public; Owner: account
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_username_key UNIQUE (username);


--
-- Name: account account_uuid_key; Type: CONSTRAINT; Schema: public; Owner: account
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_uuid_key UNIQUE (uuid);


--
-- Name: address address_pkey; Type: CONSTRAINT; Schema: public; Owner: account
--

ALTER TABLE ONLY public.address
    ADD CONSTRAINT address_pkey PRIMARY KEY (uuid);


--
-- Name: avatar avatar_pkey; Type: CONSTRAINT; Schema: public; Owner: account
--

ALTER TABLE ONLY public.avatar
    ADD CONSTRAINT avatar_pkey PRIMARY KEY (uuid);


--
-- Name: phone phone_pkey; Type: CONSTRAINT; Schema: public; Owner: account
--

ALTER TABLE ONLY public.phone
    ADD CONSTRAINT phone_pkey PRIMARY KEY (uuid);


--
-- Name: role role_pkey; Type: CONSTRAINT; Schema: public; Owner: account
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_pkey PRIMARY KEY (name);


--
-- Name: status status_pkey; Type: CONSTRAINT; Schema: public; Owner: account
--

ALTER TABLE ONLY public.status
    ADD CONSTRAINT status_pkey PRIMARY KEY (name);


--
-- Name: account account_address_uuid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: account
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_address_uuid_fkey FOREIGN KEY (address_uuid) REFERENCES public.address(uuid);


--
-- Name: account account_avatar_uuid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: account
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_avatar_uuid_fkey FOREIGN KEY (avatar_uuid) REFERENCES public.avatar(uuid);


--
-- Name: account account_phone_uuid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: account
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_phone_uuid_fkey FOREIGN KEY (phone_uuid) REFERENCES public.phone(uuid);


--
-- Name: account account_role_fkey; Type: FK CONSTRAINT; Schema: public; Owner: account
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_role_fkey FOREIGN KEY (role) REFERENCES public.role(name);


--
-- Name: account account_status_fkey; Type: FK CONSTRAINT; Schema: public; Owner: account
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_status_fkey FOREIGN KEY (status) REFERENCES public.status(name);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: account
--

GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

