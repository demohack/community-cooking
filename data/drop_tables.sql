DROP TABLE IF EXISTS t3;

-- Purpose: reads the schema to drop constraints and tables so that the database objects can be rebuilt
-- 2022-04-16 Yu

CREATE TABLE t3 (
tablename varchar(200),
conname varchar(200)	
);

DO $$DECLARE r record;
BEGIN
    FOR r IN SELECT table_schema, table_name FROM information_schema.tables
             WHERE table_schema = 'public'
    LOOP
        EXECUTE 'insert into t3 (tablename, conname) SELECT rel.relname tablename, con.conname conname from pg_catalog.pg_constraint con INNER JOIN pg_catalog.pg_class rel ON rel.oid = con.conrelid INNER JOIN pg_catalog.pg_namespace nsp ON nsp.oid = connamespace WHERE nsp.nspname = ''' || quote_ident(r.table_schema) || ''' and rel.relname = ''' || quote_ident(r.table_name) || '''';
    END LOOP;
END$$;

DO $$DECLARE r record;
BEGIN
    FOR r IN SELECT tablename, conname FROM t3
    LOOP
        EXECUTE 'alter table ' || quote_ident(r.tablename) || ' drop constraint if exists ' || quote_ident(r.conname) || ' cascade';
    END LOOP;
END$$;

DO $$DECLARE r record;
BEGIN
    FOR r IN SELECT table_name FROM information_schema.tables
             WHERE table_schema = 'public' and table_name not like 't_'
    LOOP
        EXECUTE 'drop table if exists ' || quote_ident(r.table_name);
    END LOOP;
END$$;

