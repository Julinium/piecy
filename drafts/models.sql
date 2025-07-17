-- ** Database generated with pgModeler (PostgreSQL Database Modeler).
-- ** pgModeler version: 1.2.0
-- ** PostgreSQL version: 16.0
-- ** Project Site: pgmodeler.io
-- ** Model Author: ---

-- ** Database creation must be performed outside a multi lined SQL file. 
-- ** These commands were put in this file only as a convenience.

-- object: dbieces | type: DATABASE --
-- DROP DATABASE IF EXISTS dbieces;
CREATE DATABASE dbieces
	TABLESPACE = pg_default
	OWNER = postgres;
-- ddl-end --


-- object: test | type: SCHEMA --
-- DROP SCHEMA IF EXISTS test CASCADE;
CREATE SCHEMA test;
-- ddl-end --
ALTER SCHEMA test OWNER TO postgres;
-- ddl-end --

SET search_path TO pg_catalog,public,test;
-- ddl-end --

-- object: public.product | type: TABLE --
-- DROP TABLE IF EXISTS public.product CASCADE;
CREATE TABLE public.product (
	id uuid NOT NULL DEFAULT uuid.uuid4(),
	active boolean DEFAULT 1,
	name character varying(128) NOT NULL,
	label character varying(64),
	um character varying(16),
	reference character varying(64),
	sku character varying(128),
	id_fabricant uuid,
	id_group uuid,
	origin character varying(32),
	barcode character varying(256),
	tva_percent smallint DEFAULT 20,
	prix_vente_public smallint,
	prix_vente_online smallint,
	list_online boolean DEFAULT 1,
	max_discount smallint DEFAULT 30,
	expires boolean DEFAULT 0,
	dimension_l_cm smallint DEFAULT 50,
	dimension_w_cm smallint DEFAULT 20,
	dimension_h_cm smallint DEFAULT 30,
	weight_kg decimal(6,2) DEFAULT 30,
	fragile boolean DEFAULT 0,
	description character varying(256),
	created_by uuid NOT NULL,
	created_on date,
	edited_by uuid NOT NULL,
	edited_on date,
	CONSTRAINT product_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.product OWNER TO postgres;
-- ddl-end --

-- object: public.fabricant | type: TABLE --
-- DROP TABLE IF EXISTS public.fabricant CASCADE;
CREATE TABLE public.fabricant (
	id uuid NOT NULL DEFAULT uuid.uuid4(),
	active boolean DEFAULT 1,
	name character varying(64),
	country character varying(16),
	website character varying(128),
	contact character varying(16),
	created_by uuid NOT NULL,
	created_on date,
	edited_by uuid NOT NULL,
	edited_on date,
	CONSTRAINT fabricant_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.fabricant OWNER TO postgres;
-- ddl-end --

-- object: fabricant_fk | type: CONSTRAINT --
-- ALTER TABLE public.product DROP CONSTRAINT IF EXISTS fabricant_fk CASCADE;
ALTER TABLE public.product ADD CONSTRAINT fabricant_fk FOREIGN KEY (id_fabricant)
REFERENCES public.fabricant (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public.client | type: TABLE --
-- DROP TABLE IF EXISTS public.client CASCADE;
CREATE TABLE public.client (
	id uuid NOT NULL DEFAULT uuid.uuid4(),
	active boolean DEFAULT 1,
	name character varying(128) NOT NULL,
	address_l1 character varying(64),
	address_l2 character varying(64),
	address_city character varying(32),
	address_state character varying(32),
	address_country character varying(32),
	address_zip character varying(8),
	tel character varying(16),
	mobile character varying(16),
	whatsapp character varying(16),
	fax character varying(16),
	email character varying(64),
	website character varying(64),
	description character varying(256),
	source character varying(32),
	id_societe uuid,
	created_by uuid NOT NULL,
	created_on date,
	edited_by uuid NOT NULL,
	edited_on date,
	CONSTRAINT client_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.client OWNER TO postgres;
-- ddl-end --

-- object: public.societe | type: TABLE --
-- DROP TABLE IF EXISTS public.societe CASCADE;
CREATE TABLE public.societe (
	id uuid NOT NULL DEFAULT uuid.uuid4(),
	active boolean DEFAULT 1,
	raison_social character varying(128),
	forme character varying(16),
	ice character varying(64),
	city character varying(64),
	state character varying(64),
	country character varying(64) DEFAULT MA,
	manager character varying(64),
	date_est date,
	sector character varying(128),
	phone character varying(16),
	fax character varying(16),
	email character varying(64),
	website character varying(64),
	created_by uuid NOT NULL,
	created_on date,
	edited_by uuid NOT NULL,
	edited_on date,
	CONSTRAINT societe_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.societe OWNER TO postgres;
-- ddl-end --

-- object: societe_fk | type: CONSTRAINT --
-- ALTER TABLE public.client DROP CONSTRAINT IF EXISTS societe_fk CASCADE;
ALTER TABLE public.client ADD CONSTRAINT societe_fk FOREIGN KEY (id_societe)
REFERENCES public.societe (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public.ensemble | type: TABLE --
-- DROP TABLE IF EXISTS public.ensemble CASCADE;
CREATE TABLE public.ensemble (
	id uuid NOT NULL DEFAULT uuid.uuid4(),
	active boolean DEFAULT 1,
	name character varying(64),
	description character varying(256),
	created_by uuid NOT NULL,
	created_on date,
	edited_by uuid NOT NULL,
	edited_on date,
	CONSTRAINT ensemble_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.ensemble OWNER TO postgres;
-- ddl-end --

-- object: public.many_ensemble_has_many_product | type: TABLE --
-- DROP TABLE IF EXISTS public.many_ensemble_has_many_product CASCADE;
CREATE TABLE public.many_ensemble_has_many_product (
	id_ensemble uuid NOT NULL,
	id_product uuid NOT NULL,
	CONSTRAINT many_ensemble_has_many_product_pk PRIMARY KEY (id_ensemble,id_product)
);
-- ddl-end --

-- object: ensemble_fk | type: CONSTRAINT --
-- ALTER TABLE public.many_ensemble_has_many_product DROP CONSTRAINT IF EXISTS ensemble_fk CASCADE;
ALTER TABLE public.many_ensemble_has_many_product ADD CONSTRAINT ensemble_fk FOREIGN KEY (id_ensemble)
REFERENCES public.ensemble (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: product_fk | type: CONSTRAINT --
-- ALTER TABLE public.many_ensemble_has_many_product DROP CONSTRAINT IF EXISTS product_fk CASCADE;
ALTER TABLE public.many_ensemble_has_many_product ADD CONSTRAINT product_fk FOREIGN KEY (id_product)
REFERENCES public.product (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public.category | type: TABLE --
-- DROP TABLE IF EXISTS public.category CASCADE;
CREATE TABLE public.category (
	id uuid NOT NULL DEFAULT uuid.uuid4(),
	active boolean DEFAULT 1,
	name character varying(64),
	description character varying(256),
	created_by uuid NOT NULL,
	created_on date,
	edited_by uuid NOT NULL,
	edited_on date,
	CONSTRAINT category_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.category OWNER TO postgres;
-- ddl-end --

-- object: public.many_category_has_many_product | type: TABLE --
-- DROP TABLE IF EXISTS public.many_category_has_many_product CASCADE;
CREATE TABLE public.many_category_has_many_product (
	id_category uuid NOT NULL,
	id_product uuid NOT NULL,
	CONSTRAINT many_category_has_many_product_pk PRIMARY KEY (id_category,id_product)
);
-- ddl-end --

-- object: category_fk | type: CONSTRAINT --
-- ALTER TABLE public.many_category_has_many_product DROP CONSTRAINT IF EXISTS category_fk CASCADE;
ALTER TABLE public.many_category_has_many_product ADD CONSTRAINT category_fk FOREIGN KEY (id_category)
REFERENCES public.category (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: product_fk | type: CONSTRAINT --
-- ALTER TABLE public.many_category_has_many_product DROP CONSTRAINT IF EXISTS product_fk CASCADE;
ALTER TABLE public.many_category_has_many_product ADD CONSTRAINT product_fk FOREIGN KEY (id_product)
REFERENCES public.product (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public.vehicule_model | type: TABLE --
-- DROP TABLE IF EXISTS public.vehicule_model CASCADE;
CREATE TABLE public.vehicule_model (
	id uuid NOT NULL DEFAULT uuid.uuid4(),
	active boolean DEFAULT 1,
	marque character varying(16),
	model_nom character varying(16),
	model_code character varying(16),
	year_start date,
	year_end date,
	category character varying(16),
	created_by uuid NOT NULL,
	created_on date,
	edited_by uuid NOT NULL,
	edited_on date,
	CONSTRAINT vehicule_model_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.vehicule_model OWNER TO postgres;
-- ddl-end --

-- object: public.many_vehicule_model_has_many_product | type: TABLE --
-- DROP TABLE IF EXISTS public.many_vehicule_model_has_many_product CASCADE;
CREATE TABLE public.many_vehicule_model_has_many_product (
	id_vehicule_model uuid NOT NULL,
	id_product uuid NOT NULL,
	CONSTRAINT many_vehicule_model_has_many_product_pk PRIMARY KEY (id_vehicule_model,id_product)
);
-- ddl-end --

-- object: vehicule_model_fk | type: CONSTRAINT --
-- ALTER TABLE public.many_vehicule_model_has_many_product DROP CONSTRAINT IF EXISTS vehicule_model_fk CASCADE;
ALTER TABLE public.many_vehicule_model_has_many_product ADD CONSTRAINT vehicule_model_fk FOREIGN KEY (id_vehicule_model)
REFERENCES public.vehicule_model (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: product_fk | type: CONSTRAINT --
-- ALTER TABLE public.many_vehicule_model_has_many_product DROP CONSTRAINT IF EXISTS product_fk CASCADE;
ALTER TABLE public.many_vehicule_model_has_many_product ADD CONSTRAINT product_fk FOREIGN KEY (id_product)
REFERENCES public.product (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public.magasin | type: TABLE --
-- DROP TABLE IF EXISTS public.magasin CASCADE;
CREATE TABLE public.magasin (
	id uuid NOT NULL DEFAULT uuid.uuid4(),
	active boolean,
	name character varying(64),
	address character varying(64),
	city character varying(16),
	state character varying(16),
	country character varying(16),
	website character varying(128),
	manager character varying(128),
	contact character varying(128),
	description character varying(256),
	created_by uuid NOT NULL,
	created_on date,
	edited_by uuid NOT NULL,
	edited_on date,
	CONSTRAINT magasin_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.magasin OWNER TO postgres;
-- ddl-end --

-- object: public.floor | type: TABLE --
-- DROP TABLE IF EXISTS public.floor CASCADE;
CREATE TABLE public.floor (
	id uuid NOT NULL DEFAULT uuid.uuid4(),
	active boolean DEFAULT 1,
	name character varying(64) DEFAULT RDC,
	elevation smallint DEFAULT 0,
	description character varying,
	id_magasin uuid,
	created_by uuid NOT NULL,
	created_on date,
	edited_by uuid NOT NULL,
	edited_on date,
	CONSTRAINT aile_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.floor OWNER TO postgres;
-- ddl-end --

-- object: public.rayon | type: TABLE --
-- DROP TABLE IF EXISTS public.rayon CASCADE;
CREATE TABLE public.rayon (
	id uuid NOT NULL DEFAULT uuid.uuid4(),
	active boolean DEFAULT 1,
	name character varying(64) DEFAULT R1,
	number smallint DEFAULT 1,
	description character varying,
	id_floor uuid,
	created_by uuid NOT NULL,
	created_on date,
	edited_by uuid NOT NULL,
	edited_on date,
	CONSTRAINT rayon_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.rayon OWNER TO postgres;
-- ddl-end --

-- object: magasin_fk | type: CONSTRAINT --
-- ALTER TABLE public.floor DROP CONSTRAINT IF EXISTS magasin_fk CASCADE;
ALTER TABLE public.floor ADD CONSTRAINT magasin_fk FOREIGN KEY (id_magasin)
REFERENCES public.magasin (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: floor_fk | type: CONSTRAINT --
-- ALTER TABLE public.rayon DROP CONSTRAINT IF EXISTS floor_fk CASCADE;
ALTER TABLE public.rayon ADD CONSTRAINT floor_fk FOREIGN KEY (id_floor)
REFERENCES public.floor (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public.reception | type: TABLE --
-- DROP TABLE IF EXISTS public.reception CASCADE;
CREATE TABLE public.reception (
	id uuid NOT NULL DEFAULT uuid.uuid4(),
	date_commande date,
	date_livraison date NOT NULL,
	activee boolean NOT NULL DEFAULT 1,
	payee boolean NOT NULL DEFAULT 0,
	id_fournisseur uuid,
	created_by uuid NOT NULL,
	created_on date,
	edited_by uuid NOT NULL,
	edited_on date,
	CONSTRAINT reception_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.reception OWNER TO postgres;
-- ddl-end --

-- object: public.fournisseur | type: TABLE --
-- DROP TABLE IF EXISTS public.fournisseur CASCADE;
CREATE TABLE public.fournisseur (
	id uuid NOT NULL DEFAULT uuid.uuid4(),
	active boolean DEFAULT 1,
	name character varying(128) NOT NULL,
	address_l1 character varying(64),
	address_l2 character varying(64),
	address_city character varying(32),
	address_state character varying(32),
	address_country character varying(32),
	address_zip character varying(8),
	tel character varying(16),
	mobile character varying(16),
	whatsapp character varying(16),
	fax character varying(16),
	email character varying(64),
	website character varying(64),
	description character varying(256),
	source character varying(32),
	id_societe uuid,
	created_by uuid NOT NULL,
	created_on date,
	edited_by uuid NOT NULL,
	edited_on date,
	CONSTRAINT fournisseur_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.fournisseur OWNER TO postgres;
-- ddl-end --

-- object: fournisseur_fk | type: CONSTRAINT --
-- ALTER TABLE public.reception DROP CONSTRAINT IF EXISTS fournisseur_fk CASCADE;
ALTER TABLE public.reception ADD CONSTRAINT fournisseur_fk FOREIGN KEY (id_fournisseur)
REFERENCES public.fournisseur (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public.entree | type: TABLE --
-- DROP TABLE IF EXISTS public.entree CASCADE;
CREATE TABLE public.entree (
	id uuid NOT NULL DEFAULT uuid.uuid4(),
	id_product uuid,
	id_reception uuid,
	qtte_cmd smallint NOT NULL DEFAULT 1,
	qtte_recv smallint NOT NULL DEFAULT 1,
	id_rayon uuid,
	created_by uuid NOT NULL,
	created_on date,
	edited_by uuid NOT NULL,
	edited_on date,
	CONSTRAINT entree_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.entree OWNER TO postgres;
-- ddl-end --

-- object: product_fk | type: CONSTRAINT --
-- ALTER TABLE public.entree DROP CONSTRAINT IF EXISTS product_fk CASCADE;
ALTER TABLE public.entree ADD CONSTRAINT product_fk FOREIGN KEY (id_product)
REFERENCES public.product (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: rayon_fk | type: CONSTRAINT --
-- ALTER TABLE public.entree DROP CONSTRAINT IF EXISTS rayon_fk CASCADE;
ALTER TABLE public.entree ADD CONSTRAINT rayon_fk FOREIGN KEY (id_rayon)
REFERENCES public.rayon (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: reception_fk | type: CONSTRAINT --
-- ALTER TABLE public.entree DROP CONSTRAINT IF EXISTS reception_fk CASCADE;
ALTER TABLE public.entree ADD CONSTRAINT reception_fk FOREIGN KEY (id_reception)
REFERENCES public.reception (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public.file | type: TABLE --
-- DROP TABLE IF EXISTS public.file CASCADE;
CREATE TABLE public.file (
	id uuid NOT NULL DEFAULT uuid.uuid4(),
	active boolean DEFAULT 1,
	name character varying(64),
	path character varying(256),
	type character varying(32) DEFAULT image,
	id_product uuid,
	description character varying(256),
	created_by uuid NOT NULL,
	created_on date,
	edited_by uuid NOT NULL,
	edited_on date,
	CONSTRAINT file_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.file OWNER TO postgres;
-- ddl-end --

-- object: product_fk | type: CONSTRAINT --
-- ALTER TABLE public.file DROP CONSTRAINT IF EXISTS product_fk CASCADE;
ALTER TABLE public.file ADD CONSTRAINT product_fk FOREIGN KEY (id_product)
REFERENCES public.product (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public.tenant | type: TABLE --
-- DROP TABLE IF EXISTS public.tenant CASCADE;
CREATE TABLE public.tenant (
	id uuid NOT NULL DEFAULT uuid.uuid4(),
	active boolean DEFAULT 1,
	name character varying(128),
	tel character varying(16),
	email character varying(16),
	phone character varying(16),
	whatsapp character varying(16),
	domain character varying(32),
	slug character varying(32),
	owner character varying(64),
	channel character varying(32) DEFAULT M2E,
	description character varying(256),
	created_by uuid NOT NULL,
	created_on date,
	edited_by uuid NOT NULL,
	edited_on date,
	CONSTRAINT tenant_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.tenant OWNER TO postgres;
-- ddl-end --

-- object: public.plan | type: TABLE --
-- DROP TABLE IF EXISTS public.plan CASCADE;
CREATE TABLE public.plan (
	id uuid NOT NULL DEFAULT uuid.uuid4(),
	active boolean DEFAULT 1,
	name character varying(16),
	label character varying(64),
	year_free_mth smallint DEFAULT 2,
	first_time_disc smallint DEFAULT 50,
	monthy_price decimal(12,2) NOT NULL DEFAULT 0.0,
	custom_domain boolean DEFAULT 0,
	mailbox boolean DEFAULT 0,
	ecommerce boolean DEFAULT 0,
	vitrine boolean DEFAULT 0,
	max_users smallint DEFAULT 2,
	max_clients smallint DEFAULT 10,
	max_products smallint DEFAULT 50,
	max_pdfs smallint DEFAULT 20,
	max_excels smallint DEFAULT 20,
	created_by uuid NOT NULL,
	created_on date,
	edited_by uuid NOT NULL,
	edited_on date,
	CONSTRAINT plan_pk PRIMARY KEY (id)
);
-- ddl-end --
COMMENT ON COLUMN public.plan.max_users IS E'Max number of users, including admins. 0 is unlimited';
-- ddl-end --
COMMENT ON COLUMN public.plan.max_clients IS E'Max number of clients. 0 is unlimited';
-- ddl-end --
COMMENT ON COLUMN public.plan.max_products IS E'Max number of products. 0 is unlimited';
-- ddl-end --
ALTER TABLE public.plan OWNER TO postgres;
-- ddl-end --

-- object: test.xxxx | type: TABLE --
-- DROP TABLE IF EXISTS test.xxxx CASCADE;
CREATE TABLE test.xxxx (
	id uuid NOT NULL DEFAULT uuid.uuid4(),
	active boolean DEFAULT 1,
	name character varying(16),
	created_by uuid NOT NULL,
	created_on date,
	edited_by uuid NOT NULL,
	edited_on date,
	CONSTRAINT xtemp_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE test.xxxx OWNER TO postgres;
-- ddl-end --

-- object: public."user" | type: TABLE --
-- DROP TABLE IF EXISTS public."user" CASCADE;
CREATE TABLE public."user" (
	id uuid NOT NULL DEFAULT uuid.uuid4(),
	active boolean DEFAULT 1,
	id_tenant uuid,
	verified boolean DEFAULT 0,
	username character varying(16),
	email character varying(64),
	phone character varying(64),
	first_name character varying(64),
	last_name character varying(64),
	is_superuser boolean DEFAULT 0,
	is_admin boolean DEFAULT 0,
	created_by uuid NOT NULL,
	created_on date,
	edited_by uuid NOT NULL,
	edited_on date,
	CONSTRAINT user_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public."user" OWNER TO postgres;
-- ddl-end --

-- object: public.payment | type: TABLE --
-- DROP TABLE IF EXISTS public.payment CASCADE;
CREATE TABLE public.payment (
	id uuid NOT NULL DEFAULT uuid.uuid4(),
	active boolean DEFAULT 1,
	verified boolean DEFAULT 0,
	reference character varying(32),
	mode character varying(32),
	date_made date,
	amount decimal(12,2),
	currency character varying DEFAULT MAD,
	maker character varying(64),
	description character varying(64),
	created_by uuid NOT NULL,
	created_on date,
	edited_by uuid NOT NULL,
	edited_on date,
	CONSTRAINT payment_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.payment OWNER TO postgres;
-- ddl-end --

-- object: public.subscription | type: TABLE --
-- DROP TABLE IF EXISTS public.subscription CASCADE;
CREATE TABLE public.subscription (
	id uuid NOT NULL DEFAULT uuid.uuid4(),
	active boolean DEFAULT 1,
	name character varying(16),
	date_fm date,
	date_to date,
	id_tenant uuid,
	id_plan uuid,
	id_payment uuid,
	created_by uuid NOT NULL,
	created_on date,
	edited_by uuid NOT NULL,
	edited_on date,
	CONSTRAINT subscription_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.subscription OWNER TO postgres;
-- ddl-end --

-- object: tenant_fk | type: CONSTRAINT --
-- ALTER TABLE public.subscription DROP CONSTRAINT IF EXISTS tenant_fk CASCADE;
ALTER TABLE public.subscription ADD CONSTRAINT tenant_fk FOREIGN KEY (id_tenant)
REFERENCES public.tenant (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: plan_fk | type: CONSTRAINT --
-- ALTER TABLE public.subscription DROP CONSTRAINT IF EXISTS plan_fk CASCADE;
ALTER TABLE public.subscription ADD CONSTRAINT plan_fk FOREIGN KEY (id_plan)
REFERENCES public.plan (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: payment_fk | type: CONSTRAINT --
-- ALTER TABLE public.subscription DROP CONSTRAINT IF EXISTS payment_fk CASCADE;
ALTER TABLE public.subscription ADD CONSTRAINT payment_fk FOREIGN KEY (id_payment)
REFERENCES public.payment (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: tenant_fk | type: CONSTRAINT --
-- ALTER TABLE public."user" DROP CONSTRAINT IF EXISTS tenant_fk CASCADE;
ALTER TABLE public."user" ADD CONSTRAINT tenant_fk FOREIGN KEY (id_tenant)
REFERENCES public.tenant (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public.commande | type: TABLE --
-- DROP TABLE IF EXISTS public.commande CASCADE;
CREATE TABLE public.commande (
	id uuid NOT NULL DEFAULT uuid.uuid4(),
	activee boolean NOT NULL DEFAULT 1,
	id_client uuid,
	date_commande date,
	date_livraison date NOT NULL,
	payee boolean NOT NULL DEFAULT 0,
	report character varying(256),
	public_note character varying(256),
	internal_note character varying(256),
	created_by uuid NOT NULL,
	created_on date,
	edited_by uuid NOT NULL,
	edited_on date,
	CONSTRAINT commande_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.commande OWNER TO postgres;
-- ddl-end --

-- object: client_fk | type: CONSTRAINT --
-- ALTER TABLE public.commande DROP CONSTRAINT IF EXISTS client_fk CASCADE;
ALTER TABLE public.commande ADD CONSTRAINT client_fk FOREIGN KEY (id_client)
REFERENCES public.client (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public.sortie | type: TABLE --
-- DROP TABLE IF EXISTS public.sortie CASCADE;
CREATE TABLE public.sortie (
	id uuid NOT NULL DEFAULT uuid.uuid4(),
	id_product uuid,
	id_commande uuid,
	qtte_cmde smallint NOT NULL DEFAULT 1,
	qtte_recv smallint NOT NULL DEFAULT 1,
	id_rayon uuid,
	created_by uuid NOT NULL,
	created_on date,
	edited_by uuid NOT NULL,
	edited_on date,
	CONSTRAINT sortee_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.sortie OWNER TO postgres;
-- ddl-end --

-- object: commande_fk | type: CONSTRAINT --
-- ALTER TABLE public.sortie DROP CONSTRAINT IF EXISTS commande_fk CASCADE;
ALTER TABLE public.sortie ADD CONSTRAINT commande_fk FOREIGN KEY (id_commande)
REFERENCES public.commande (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: product_fk | type: CONSTRAINT --
-- ALTER TABLE public.sortie DROP CONSTRAINT IF EXISTS product_fk CASCADE;
ALTER TABLE public.sortie ADD CONSTRAINT product_fk FOREIGN KEY (id_product)
REFERENCES public.product (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public.count | type: TABLE --
-- DROP TABLE IF EXISTS public.count CASCADE;
CREATE TABLE public.count (
	id uuid NOT NULL DEFAULT uuid.uuid4(),
	qtte_cmde smallint NOT NULL DEFAULT 1,
	qtte_recv smallint NOT NULL DEFAULT 1,
	id_rayon uuid,
	created_by uuid NOT NULL,
	created_on date,
	edited_by uuid NOT NULL,
	edited_on date,
	CONSTRAINT count_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.count OWNER TO postgres;
-- ddl-end --

-- object: public.checkup | type: TABLE --
-- DROP TABLE IF EXISTS public.checkup CASCADE;
CREATE TABLE public.checkup (
	id uuid DEFAULT uuid.uuid4(),
	activee boolean NOT NULL DEFAULT 1,
	date date NOT NULL,
	counter character varying(64),
	reason character varying(64),
	reference character varying(128),
	description character varying(256),
	created_by uuid NOT NULL,
	created_on date,
	edited_by uuid NOT NULL,
	edited_on date,
	id_magasin uuid,
	id_count uuid,
	report character varying(256)

);
-- ddl-end --
ALTER TABLE public.checkup OWNER TO postgres;
-- ddl-end --

-- object: magasin_fk | type: CONSTRAINT --
-- ALTER TABLE public.checkup DROP CONSTRAINT IF EXISTS magasin_fk CASCADE;
ALTER TABLE public.checkup ADD CONSTRAINT magasin_fk FOREIGN KEY (id_magasin)
REFERENCES public.magasin (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: count_fk | type: CONSTRAINT --
-- ALTER TABLE public.checkup DROP CONSTRAINT IF EXISTS count_fk CASCADE;
ALTER TABLE public.checkup ADD CONSTRAINT count_fk FOREIGN KEY (id_count)
REFERENCES public.count (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public."group" | type: TABLE --
-- DROP TABLE IF EXISTS public."group" CASCADE;
CREATE TABLE public."group" (
	id uuid NOT NULL DEFAULT uuid.uuid4(),
	active boolean DEFAULT 1,
	name character varying(64),
	description character varying(256),
	created_by uuid NOT NULL,
	created_on date,
	edited_by uuid NOT NULL,
	edited_on date,
	CONSTRAINT group_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public."group" OWNER TO postgres;
-- ddl-end --

-- object: group_fk | type: CONSTRAINT --
-- ALTER TABLE public.product DROP CONSTRAINT IF EXISTS group_fk CASCADE;
ALTER TABLE public.product ADD CONSTRAINT group_fk FOREIGN KEY (id_group)
REFERENCES public."group" (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public.registre | type: TABLE --
-- DROP TABLE IF EXISTS public.registre CASCADE;
CREATE TABLE public.registre (
	id uuid NOT NULL DEFAULT uuid.uuid4(),
	active boolean DEFAULT 1,
	date date,
	model character varying(32),
	operation character varying(1),
	record uuid,
	created_by uuid NOT NULL,
	created_on date,
	edited_by uuid NOT NULL,
	edited_on date,
	CONSTRAINT registre_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.registre OWNER TO postgres;
-- ddl-end --

-- object: societe_fk | type: CONSTRAINT --
-- ALTER TABLE public.fournisseur DROP CONSTRAINT IF EXISTS societe_fk CASCADE;
ALTER TABLE public.fournisseur ADD CONSTRAINT societe_fk FOREIGN KEY (id_societe)
REFERENCES public.societe (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: rayon_fk | type: CONSTRAINT --
-- ALTER TABLE public.sortie DROP CONSTRAINT IF EXISTS rayon_fk CASCADE;
ALTER TABLE public.sortie ADD CONSTRAINT rayon_fk FOREIGN KEY (id_rayon)
REFERENCES public.rayon (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --


