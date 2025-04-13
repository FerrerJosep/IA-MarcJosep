--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

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

--
-- Name: calcular_minutos(character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.calcular_minutos(jotason character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
    iMatricula character varying := jotason::json ->> 'matricula';
    hora_entrada timestamp;
    hora_salida timestamp;
BEGIN
    SELECT vehi_fecha_entra, vehi_fecha_salida
    INTO hora_entrada, hora_salida
    FROM vehiculos
    WHERE vehi_matricula = iMatricula;

    IF hora_entrada IS NULL OR hora_salida IS NULL THEN
        RETURN -1; -- No hay datos suficientes
    END IF;

    RETURN FLOOR(EXTRACT(EPOCH FROM (hora_salida - hora_entrada)) / 60)::int;
END;
$$;


ALTER FUNCTION public.calcular_minutos(jotason character varying) OWNER TO postgres;

--
-- Name: eliminar_vehiculo(character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.eliminar_vehiculo(jotason character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE 
    iMatricula character varying;
BEGIN
    iMatricula := (jotason::json ->> 'matricula');

    -- Verificamos si existe el vehículo
    IF EXISTS (
        SELECT 1 FROM vehiculos WHERE vehi_matricula = iMatricula
    ) THEN
        RAISE NOTICE 'El valor existe.';

      

        -- Actualizamos estado de salida y hora
        UPDATE vehiculos 
        SET vehi_fecha_salida = NOW(), 
            vehi_esta_dentro = FALSE
        WHERE vehi_matricula = iMatricula;

    ELSE
        RAISE NOTICE 'El valor NO existe.';
    END IF;

END;
$$;


ALTER FUNCTION public.eliminar_vehiculo(jotason character varying) OWNER TO postgres;

--
-- Name: insertar_vehiculo(character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.insertar_vehiculo(jotason character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
    iMatricula character varying;
BEGIN
    iMatricula := (jotason::json ->> 'matricula');

    IF EXISTS (SELECT 1 FROM vehiculos WHERE vehi_matricula = iMatricula) THEN
        -- Ya existe: actualizamos vehi_fecha_entra y estado
        UPDATE vehiculos
        SET vehi_esta_dentro = true,
            vehi_fecha_entra = CURRENT_TIMESTAMP
        WHERE vehi_matricula = iMatricula;
    ELSE
        -- No existe: insertamos nuevo registro
        INSERT INTO vehiculos(vehi_matricula, vehi_esta_dentro, vehi_fecha_entra)
        VALUES (iMatricula, true, CURRENT_TIMESTAMP);

		
		UPDATE vehiculos
        SET vehi_esta_dentro = true,
            vehi_fecha_entra = CURRENT_TIMESTAMP
        WHERE vehi_matricula = iMatricula;
		
    END IF;
END;
$$;


ALTER FUNCTION public.insertar_vehiculo(jotason character varying) OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    usu_cod integer NOT NULL,
    usu_vehiculo integer,
    usu_nombre character varying
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- Name: usuarios_usu_cod_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_usu_cod_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuarios_usu_cod_seq OWNER TO postgres;

--
-- Name: usuarios_usu_cod_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_usu_cod_seq OWNED BY public.usuarios.usu_cod;


--
-- Name: vehiculos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vehiculos (
    vehi_cod integer NOT NULL,
    vehi_matricula character varying,
    vehi_fecha_entra timestamp without time zone DEFAULT now(),
    vehi_fecha_salida timestamp without time zone,
    vehi_esta_dentro boolean DEFAULT false
);


ALTER TABLE public.vehiculos OWNER TO postgres;

--
-- Name: vehiculos_vehi_cod_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.vehiculos_vehi_cod_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.vehiculos_vehi_cod_seq OWNER TO postgres;

--
-- Name: vehiculos_vehi_cod_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.vehiculos_vehi_cod_seq OWNED BY public.vehiculos.vehi_cod;


--
-- Name: usuarios usu_cod; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN usu_cod SET DEFAULT nextval('public.usuarios_usu_cod_seq'::regclass);


--
-- Name: vehiculos vehi_cod; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vehiculos ALTER COLUMN vehi_cod SET DEFAULT nextval('public.vehiculos_vehi_cod_seq'::regclass);


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios (usu_cod, usu_vehiculo, usu_nombre) FROM stdin;
\.


--
-- Data for Name: vehiculos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vehiculos (vehi_cod, vehi_matricula, vehi_fecha_entra, vehi_fecha_salida, vehi_esta_dentro) FROM stdin;
72	josepppp	2025-04-10 20:20:02.565416	2025-04-10 20:21:19.986005	f
78	1336FLG	2025-04-13 19:00:15.045446	2025-04-13 19:00:23.121905	f
66	MatriculaProva	2025-04-10 20:25:09.915589	2025-04-10 20:26:12.016611	f
73	chiariibb	2025-04-10 21:29:43.148172	2025-04-10 21:31:12.607842	f
67	Marc	2025-04-10 19:36:32.483225	2025-04-10 19:37:02.372514	f
84	5879FYR	2025-04-13 19:07:46.222682	2025-04-13 19:08:51.663714	f
81	2000GYG	2025-04-13 19:12:19.372215	2025-04-13 19:13:08.343845	f
68	Josep	2025-04-12 20:13:10.679177	2025-04-10 20:22:04.8541	t
69	josep	2025-04-12 20:13:25.42303	2025-04-12 20:06:31.904858	t
85	37960PX	2025-04-13 19:14:47.611097	2025-04-13 19:17:42.855208	f
65	ABCD	2025-04-12 20:13:33.261101	2025-04-12 20:15:23.779502	f
74	JOSEP	2025-04-13 15:11:18.334808	2025-04-13 15:13:12.133178	f
75	PROVA	2025-04-13 15:18:59.31336	2025-04-13 15:25:08.729076	f
77	3760CGF	2025-04-13 16:52:04.178895	\N	t
80	4702CYP	2025-04-13 18:01:15.068521	2025-04-13 18:01:25.668857	f
79	8884KHF	2025-04-13 17:13:44.773512	2025-04-13 18:09:05.561335	f
70	Josep1234	2025-04-10 20:12:24.529334	2025-04-10 20:13:26.295195	f
82	8884KNL	2025-04-13 18:28:55.644882	\N	t
71	marc123	2025-04-10 20:18:34.964727	2025-04-10 20:18:48.546728	f
76	8704GCA	2025-04-13 18:32:32.611807	2025-04-13 18:36:56.230661	f
83	FJXFJX	2025-04-13 18:38:03.556349	2025-04-13 18:37:49.699955	t
\.


--
-- Name: usuarios_usu_cod_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuarios_usu_cod_seq', 7, true);


--
-- Name: vehiculos_vehi_cod_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.vehiculos_vehi_cod_seq', 85, true);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (usu_cod);


--
-- Name: vehiculos vehi_matricula_unica; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vehiculos
    ADD CONSTRAINT vehi_matricula_unica UNIQUE (vehi_matricula);


--
-- Name: vehiculos vehiculos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vehiculos
    ADD CONSTRAINT vehiculos_pkey PRIMARY KEY (vehi_cod);


--
-- Name: usuarios fk_usu_vehiculo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT fk_usu_vehiculo FOREIGN KEY (usu_vehiculo) REFERENCES public.vehiculos(vehi_cod);


--
-- PostgreSQL database dump complete
--

