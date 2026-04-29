-- Procedure 1: upsert
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE first_name = p_name;
    ELSE
        INSERT INTO phonebook(first_name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;

-- Procedure 2: bulk insert with validation
CREATE OR REPLACE PROCEDURE insert_many_contacts(names VARCHAR[], phones VARCHAR[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
    bad_data TEXT := '';
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP
        IF phones[i] ~ '^[+8][0-9]{10,14}$' THEN
            CALL upsert_contact(names[i], phones[i]);
        ELSE
            bad_data := bad_data || names[i] || ': ' || phones[i] || E'\n';
        END IF;
    END LOOP;
    IF bad_data != '' THEN
        RAISE NOTICE 'Invalid data: %', bad_data;
    END IF;
END;
$$;

-- Procedure 3: delete by name or phone
CREATE OR REPLACE PROCEDURE delete_contact(p_name VARCHAR DEFAULT NULL, p_phone VARCHAR DEFAULT NULL)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_name IS NOT NULL THEN
        DELETE FROM phonebook WHERE first_name = p_name;
    ELSIF p_phone IS NOT NULL THEN
        DELETE FROM phonebook WHERE phone = p_phone;
    END IF;
END;
$$;