-- Create the curelink user if it doesn't exist
DO
$$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'curelink') THEN
    CREATE USER curelink WITH PASSWORD 'curelink_password';
  END IF;
END
$$;

-- Create the database if it doesn't exist
SELECT 'CREATE DATABASE curelink_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'curelink_db')\gexec

-- Grant privileges to the curelink user on the database
GRANT ALL PRIVILEGES ON DATABASE curelink_db TO curelink;

-- Connect to the curelink_db to grant schema privileges
\c curelink_db postgres;

-- Grant all privileges on the public schema
GRANT ALL PRIVILEGES ON SCHEMA public TO curelink;

-- Grant all privileges on all tables in the public schema
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO curelink;

-- Grant all privileges on all sequences in the public schema
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO curelink;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO curelink;

-- Set the owner of the public schema to curelink
ALTER SCHEMA public OWNER TO curelink;
