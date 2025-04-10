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
-- Name: calcular_importe(character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.calcular_importe(jotason character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	iMatricula character varying;
	hora_entrada timestamp;
	hora_salida timestamp;
	duracion_minutos integer;
BEGIN
	-- Extraemos la matr├¡cula del par├ímetro JSON
	iMatricula := (jotason::json ->> 'matricula');

	-- Verificamos si la matr├¡cula existe en la tabla
	IF EXISTS (
		SELECT 1
		FROM vehiculos
		WHERE vehi_matricula = iMatricula
	) THEN
		RAISE NOTICE 'El valor existe.';
	ELSE
		RAISE NOTICE 'El valor NO existe.';
		RETURN -1; -- Retornamos un valor negativo para indicar que no existe
	END IF;

	-- Obtenemos las fechas de entrada y salida
	SELECT vehi_fecha_entra, vehi_fecha_salida
	INTO hora_entrada, hora_salida
	FROM vehiculos
	WHERE vehi_matricula = iMatricula;

	-- Calculamos la duraci├│n en minutos
	duracion_minutos := EXTRACT(EPOCH FROM (hora_salida - hora_entrada)) / 60;

	-- Retornamos el valor
	RETURN duracion_minutos;
END;
$$;


ALTER FUNCTION public.calcular_importe(jotason character varying) OWNER TO postgres;

--
-- Name: eliminar_vehiculo(character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.eliminar_vehiculo(jotason character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
declare 
	iMatricula character varying;
	iCodigo integer;
BEGIN
	iMatricula := (jotason::json ->> 'matricula');

	 IF EXISTS (
        SELECT vehi_matricula
        FROM vehiculos
        WHERE vehi_matricula = iMatricula
    ) THEN
        RAISE NOTICE 'El valor existe.';
    ELSE
        RAISE NOTICE 'El valor NO existe.';
    END IF;

	SELECT vehi_fecha_entra, vehi_fecha_salida
	INTO iCodigo
	FROM vehiculos
	WHERE vehi_matricula = iMatricula;
	
	update vehiculos set vehi_fecha_salida=now() where 
	vehi_matricula=iMatricula;
	
    update vehiculos set vehi_esta_dentro=false where 
	vehi_matricula=iMatricula;
END;
$$;


ALTER FUNCTION public.eliminar_vehiculo(jotason character varying) OWNER TO postgres;

--
-- Name: insertar_vehiculo(character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.insertar_vehiculo(jotason character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
declare 
	iMatricula character varying;
BEGIN
	iMatricula := (jotason::json ->> 'matricula');

    INSERT INTO vehiculos(vehi_matricula) VALUES (iMatricula);
	update vehiculos set vehi_esta_dentro=true where vehi_matricula=iMatricula;
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
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (usu_cod);


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

