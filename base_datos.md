-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.acquisition_requests (
  id_request uuid NOT NULL DEFAULT gen_random_uuid(),
  request_number character varying NOT NULL UNIQUE,
  id_supplier uuid,
  description text NOT NULL,
  estimated_amount numeric,
  status USER-DEFINED,
  priority USER-DEFINED,
  request_date timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  approval_date timestamp with time zone,
  completion_date timestamp with time zone,
  id_requesting_user uuid NOT NULL,
  id_approving_user uuid,
  notes text,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT acquisition_requests_pkey PRIMARY KEY (id_request),
  CONSTRAINT acquisition_requests_id_approving_user_fkey FOREIGN KEY (id_approving_user) REFERENCES public.users(id_user),
  CONSTRAINT acquisition_requests_id_requesting_user_fkey FOREIGN KEY (id_requesting_user) REFERENCES public.users(id_user),
  CONSTRAINT acquisition_requests_id_supplier_fkey FOREIGN KEY (id_supplier) REFERENCES public.suppliers(id_supplier)
);
CREATE TABLE public.brands (
  id_brand uuid NOT NULL DEFAULT gen_random_uuid(),
  name character varying NOT NULL UNIQUE,
  country_origin character varying,
  active boolean DEFAULT true,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  type_brand USER-DEFINED DEFAULT 'product'::type_brand,
  CONSTRAINT brands_pkey PRIMARY KEY (id_brand)
);
CREATE TABLE public.cashbox (
  id_cashbox uuid NOT NULL DEFAULT gen_random_uuid(),
  movement_date timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  id_transaction uuid,
  id_user uuid NOT NULL,
  type USER-DEFINED NOT NULL,
  concept text NOT NULL,
  amount numeric NOT NULL CHECK (amount >= 0::numeric),
  balance numeric NOT NULL DEFAULT 0,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  id_session uuid,
  CONSTRAINT cashbox_pkey PRIMARY KEY (id_cashbox),
  CONSTRAINT cashbox_id_session_fkey FOREIGN KEY (id_session) REFERENCES public.cashbox_sessions(id_session),
  CONSTRAINT cashbox_id_user_fkey FOREIGN KEY (id_user) REFERENCES public.users(id_user)
);
CREATE TABLE public.cashbox_sessions (
  id_session uuid NOT NULL DEFAULT gen_random_uuid(),
  session_date date NOT NULL,
  opened_by uuid NOT NULL,
  closed_by uuid,
  opening_amount numeric NOT NULL DEFAULT 0,
  expected_closing numeric,
  actual_closing numeric,
  difference numeric,
  status USER-DEFINED NOT NULL DEFAULT 'OPEN'::cashbox_session_status,
  opened_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  closed_at timestamp with time zone,
  notes text,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT cashbox_sessions_pkey PRIMARY KEY (id_session),
  CONSTRAINT cashbox_sessions_closed_by_fkey FOREIGN KEY (closed_by) REFERENCES public.users(id_user),
  CONSTRAINT cashbox_sessions_opened_by_fkey FOREIGN KEY (opened_by) REFERENCES public.users(id_user)
);
CREATE TABLE public.categories (
  id_category uuid NOT NULL DEFAULT gen_random_uuid(),
  name character varying NOT NULL UNIQUE,
  description text,
  active boolean DEFAULT true,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT categories_pkey PRIMARY KEY (id_category)
);
CREATE TABLE public.change_history (
  id_change uuid NOT NULL DEFAULT gen_random_uuid(),
  table_name character varying NOT NULL,
  record_id uuid NOT NULL,
  field character varying NOT NULL,
  previous_value text,
  new_value text,
  id_user uuid,
  change_date timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT change_history_pkey PRIMARY KEY (id_change),
  CONSTRAINT change_history_id_user_fkey FOREIGN KEY (id_user) REFERENCES public.users(id_user)
);
CREATE TABLE public.client_roles (
  client_id character varying NOT NULL,
  id_role uuid NOT NULL,
  CONSTRAINT client_roles_pkey PRIMARY KEY (client_id, id_role),
  CONSTRAINT client_roles_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(client_id),
  CONSTRAINT client_roles_id_role_fkey FOREIGN KEY (id_role) REFERENCES public.roles(id_role)
);
CREATE TABLE public.clients (
  client_id character varying NOT NULL,
  client_secret character varying,
  CONSTRAINT clients_pkey PRIMARY KEY (client_id)
);
CREATE TABLE public.customers (
  id_customer uuid NOT NULL DEFAULT gen_random_uuid(),
  id_number character varying NOT NULL UNIQUE,
  name character varying NOT NULL,
  surname character varying NOT NULL,
  address text,
  phone character varying,
  email character varying,
  identification_type USER-DEFINED,
  birth_date date,
  gender USER-DEFINED,
  active boolean DEFAULT true,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT customers_pkey PRIMARY KEY (id_customer)
);
CREATE TABLE public.evidence_photos (
  id_photo uuid NOT NULL DEFAULT gen_random_uuid(),
  id_repair uuid NOT NULL,
  type USER-DEFINED NOT NULL,
  file_name character varying NOT NULL,
  file_path character varying NOT NULL,
  description text,
  capture_date timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  id_captured_by uuid,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT evidence_photos_pkey PRIMARY KEY (id_photo),
  CONSTRAINT evidence_photos_id_captured_by_fkey FOREIGN KEY (id_captured_by) REFERENCES public.users(id_user),
  CONSTRAINT evidence_photos_id_repair_fkey FOREIGN KEY (id_repair) REFERENCES public.repairs(id_repair)
);
CREATE TABLE public.inventory_movements (
  id_movement uuid NOT NULL DEFAULT gen_random_uuid(),
  id_product uuid NOT NULL,
  movement_type USER-DEFINED NOT NULL,
  quantity integer NOT NULL,
  previous_quantity integer NOT NULL,
  new_quantity integer NOT NULL,
  reason text,
  reference character varying,
  id_user uuid,
  movement_date timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT inventory_movements_pkey PRIMARY KEY (id_movement),
  CONSTRAINT inventory_movements_id_product_fkey FOREIGN KEY (id_product) REFERENCES public.products(id_product),
  CONSTRAINT inventory_movements_id_user_fkey FOREIGN KEY (id_user) REFERENCES public.users(id_user)
);
CREATE TABLE public.mechanics (
  id_mechanic uuid NOT NULL DEFAULT gen_random_uuid(),
  id_number character varying NOT NULL UNIQUE,
  name character varying NOT NULL,
  surname character varying,
  phone character varying,
  email character varying,
  address text,
  hire_date date,
  salary numeric,
  active boolean DEFAULT true,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT mechanics_pkey PRIMARY KEY (id_mechanic)
);
CREATE TABLE public.mechanics_specialties (
  id_mechanic_specialty uuid NOT NULL DEFAULT gen_random_uuid(),
  id_mechanic uuid NOT NULL,
  id_specialty uuid NOT NULL,
  certification_date date,
  level USER-DEFINED,
  active boolean DEFAULT true,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT mechanics_specialties_pkey PRIMARY KEY (id_mechanic_specialty),
  CONSTRAINT mechanics_specialties_id_mechanic_fkey FOREIGN KEY (id_mechanic) REFERENCES public.mechanics(id_mechanic),
  CONSTRAINT mechanics_specialties_id_specialty_fkey FOREIGN KEY (id_specialty) REFERENCES public.specialties(id_specialty)
);
CREATE TABLE public.notifications (
  id_notification uuid NOT NULL DEFAULT gen_random_uuid(),
  title character varying NOT NULL,
  message text NOT NULL,
  type USER-DEFINED,
  id_user uuid,
  read boolean DEFAULT false,
  creation_date timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  read_date timestamp with time zone,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT notifications_pkey PRIMARY KEY (id_notification),
  CONSTRAINT notifications_id_user_fkey FOREIGN KEY (id_user) REFERENCES public.users(id_user)
);
CREATE TABLE public.payments (
  id_payment uuid NOT NULL DEFAULT gen_random_uuid(),
  id_sale uuid NOT NULL,
  payment_method USER-DEFINED NOT NULL,
  amount numeric NOT NULL,
  payment_date timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  reference character varying,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT payments_pkey PRIMARY KEY (id_payment),
  CONSTRAINT payments_id_sale_fkey FOREIGN KEY (id_sale) REFERENCES public.sales(id_sale)
);
CREATE TABLE public.products (
  id_product uuid NOT NULL DEFAULT gen_random_uuid(),
  code character varying NOT NULL UNIQUE,
  name character varying NOT NULL,
  description text,
  price numeric NOT NULL CHECK (price >= 0::numeric),
  discount numeric DEFAULT 0.0 CHECK (discount >= 0::numeric),
  stock integer DEFAULT 0 CHECK (stock >= 0),
  min_stock integer DEFAULT 0 CHECK (min_stock >= 0),
  max_stock integer DEFAULT 0 CHECK (max_stock >= 0),
  id_supplier uuid,
  id_category uuid,
  id_brand uuid,
  model character varying,
  qr_url text UNIQUE,
  active boolean DEFAULT true,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT products_pkey PRIMARY KEY (id_product),
  CONSTRAINT products_id_brand_fkey FOREIGN KEY (id_brand) REFERENCES public.brands(id_brand),
  CONSTRAINT products_id_category_fkey FOREIGN KEY (id_category) REFERENCES public.categories(id_category),
  CONSTRAINT products_id_supplier_fkey FOREIGN KEY (id_supplier) REFERENCES public.suppliers(id_supplier)
);
CREATE TABLE public.repair_materials (
  id_repair_material uuid NOT NULL DEFAULT gen_random_uuid(),
  id_repair uuid NOT NULL,
  id_product uuid NOT NULL,
  quantity integer NOT NULL,
  unit_price numeric NOT NULL,
  discount numeric DEFAULT 0,
  subtotal numeric NOT NULL,
  usage_date timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  id_vehicle uuid,
  type character varying,
  reference character varying,
  CONSTRAINT repair_materials_pkey PRIMARY KEY (id_repair_material),
  CONSTRAINT repair_materials_id_product_fkey FOREIGN KEY (id_product) REFERENCES public.products(id_product),
  CONSTRAINT repair_materials_id_repair_fkey FOREIGN KEY (id_repair) REFERENCES public.repairs(id_repair),
  CONSTRAINT repair_materials_id_vehicle_fkey FOREIGN KEY (id_vehicle) REFERENCES public.vehicles(id_vehicle)
);
CREATE TABLE public.repair_services (
  id_repair_service uuid NOT NULL DEFAULT gen_random_uuid(),
  id_repair uuid NOT NULL,
  id_service_type uuid NOT NULL,
  agreed_price numeric,
  actual_hours numeric,
  completed boolean DEFAULT false,
  start_date timestamp with time zone,
  completion_date timestamp with time zone,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT repair_services_pkey PRIMARY KEY (id_repair_service),
  CONSTRAINT repair_services_id_repair_fkey FOREIGN KEY (id_repair) REFERENCES public.repairs(id_repair),
  CONSTRAINT repair_services_id_service_type_fkey FOREIGN KEY (id_service_type) REFERENCES public.service_types(id_service_type)
);
CREATE TABLE public.repairs (
  id_repair uuid NOT NULL DEFAULT gen_random_uuid(),
  order_number character varying NOT NULL UNIQUE,
  id_vehicle uuid NOT NULL,
  id_mechanic uuid,
  fault_description text NOT NULL,
  diagnosis text,
  status USER-DEFINED,
  priority USER-DEFINED,
  entry_date timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  start_date timestamp with time zone,
  completion_date timestamp with time zone,
  delivery_date timestamp with time zone,
  notes text,
  estimated_cost numeric,
  final_cost numeric,
  id_created_by uuid,
  id_updated_by uuid,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT repairs_pkey PRIMARY KEY (id_repair),
  CONSTRAINT repairs_id_created_by_fkey FOREIGN KEY (id_created_by) REFERENCES public.users(id_user),
  CONSTRAINT repairs_id_mechanic_fkey FOREIGN KEY (id_mechanic) REFERENCES public.mechanics(id_mechanic),
  CONSTRAINT repairs_id_updated_by_fkey FOREIGN KEY (id_updated_by) REFERENCES public.users(id_user),
  CONSTRAINT repairs_id_vehicle_fkey FOREIGN KEY (id_vehicle) REFERENCES public.vehicles(id_vehicle)
);
CREATE TABLE public.request_products (
  id_request_product uuid NOT NULL DEFAULT gen_random_uuid(),
  id_request uuid NOT NULL,
  id_product uuid,
  product_description character varying NOT NULL,
  requested_quantity integer NOT NULL,
  estimated_price numeric,
  urgent boolean DEFAULT false,
  approved boolean DEFAULT false,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT request_products_pkey PRIMARY KEY (id_request_product),
  CONSTRAINT request_products_id_product_fkey FOREIGN KEY (id_product) REFERENCES public.products(id_product),
  CONSTRAINT request_products_id_request_fkey FOREIGN KEY (id_request) REFERENCES public.acquisition_requests(id_request)
);
CREATE TABLE public.roles (
  id_role uuid NOT NULL DEFAULT gen_random_uuid(),
  name character varying NOT NULL UNIQUE,
  description text,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT roles_pkey PRIMARY KEY (id_role)
);
CREATE TABLE public.sale_details (
  id_sale_detail uuid NOT NULL DEFAULT gen_random_uuid(),
  id_sale uuid NOT NULL,
  id_product uuid NOT NULL,
  quantity integer NOT NULL,
  unit_price numeric NOT NULL,
  discount numeric DEFAULT 0,
  subtotal numeric NOT NULL,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT sale_details_pkey PRIMARY KEY (id_sale_detail),
  CONSTRAINT sale_details_id_product_fkey FOREIGN KEY (id_product) REFERENCES public.products(id_product),
  CONSTRAINT sale_details_id_sale_fkey FOREIGN KEY (id_sale) REFERENCES public.sales(id_sale)
);
CREATE TABLE public.sales (
  id_sale uuid NOT NULL DEFAULT gen_random_uuid(),
  invoice_number character varying NOT NULL UNIQUE,
  id_customer uuid NOT NULL,
  id_seller uuid NOT NULL,
  subtotal numeric NOT NULL,
  tax numeric NOT NULL,
  total_discount numeric DEFAULT 0,
  total numeric NOT NULL,
  status USER-DEFINED,
  sale_date timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  notes text,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  payment_method USER-DEFINED NOT NULL DEFAULT 'cash'::payment_method,
  CONSTRAINT sales_pkey PRIMARY KEY (id_sale),
  CONSTRAINT sales_id_customer_fkey FOREIGN KEY (id_customer) REFERENCES public.customers(id_customer),
  CONSTRAINT sales_id_seller_fkey FOREIGN KEY (id_seller) REFERENCES public.users(id_user)
);
CREATE TABLE public.service_types (
  id_service_type uuid NOT NULL DEFAULT gen_random_uuid(),
  name character varying NOT NULL,
  description text,
  base_price numeric,
  estimated_hours integer,
  id_required_specialty uuid,
  active boolean DEFAULT true,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT service_types_pkey PRIMARY KEY (id_service_type),
  CONSTRAINT service_types_id_required_specialty_fkey FOREIGN KEY (id_required_specialty) REFERENCES public.specialties(id_specialty)
);
CREATE TABLE public.specialties (
  id_specialty uuid NOT NULL DEFAULT gen_random_uuid(),
  name character varying NOT NULL UNIQUE,
  description text,
  active boolean DEFAULT true,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT specialties_pkey PRIMARY KEY (id_specialty)
);
CREATE TABLE public.suppliers (
  id_supplier uuid NOT NULL DEFAULT gen_random_uuid(),
  ruc character varying NOT NULL UNIQUE,
  name character varying NOT NULL,
  surname character varying NOT NULL,
  address text,
  phone character varying,
  email character varying,
  main_contact character varying,
  active boolean DEFAULT true,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT suppliers_pkey PRIMARY KEY (id_supplier)
);
CREATE TABLE public.system_configuration (
  id_config uuid NOT NULL DEFAULT gen_random_uuid(),
  key character varying NOT NULL UNIQUE,
  value text,
  description text,
  type USER-DEFINED DEFAULT 'string'::configuration_type,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT system_configuration_pkey PRIMARY KEY (id_config)
);
CREATE TABLE public.users (
  id_user uuid NOT NULL DEFAULT gen_random_uuid(),
  id_role uuid NOT NULL,
  username character varying NOT NULL UNIQUE,
  password character varying,
  name character varying NOT NULL,
  surname character varying NOT NULL,
  email character varying UNIQUE,
  active boolean DEFAULT true,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  cognito_sub text UNIQUE,
  CONSTRAINT users_pkey PRIMARY KEY (id_user),
  CONSTRAINT users_id_role_fkey FOREIGN KEY (id_role) REFERENCES public.roles(id_role)
);
CREATE TABLE public.vehicles (
  id_vehicle uuid NOT NULL DEFAULT gen_random_uuid(),
  id_customer uuid NOT NULL,
  license_plate character varying UNIQUE,
  brand character varying,
  model character varying,
  year integer,
  color character varying,
  mileage integer,
  active boolean DEFAULT true,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT vehicles_pkey PRIMARY KEY (id_vehicle),
  CONSTRAINT vehicles_id_customer_fkey FOREIGN KEY (id_customer) REFERENCES public.customers(id_customer)
);