-- Drop old functions first
DROP FUNCTION IF EXISTS search_contacts(text);
DROP FUNCTION IF EXISTS get_contacts_paginated(INT, INT);

-- Function 1: search by name or phone
CREATE OR REPLACE FUNCTION search_contacts(p text)
RETURNS TABLE(id INT, first_name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT pb.id, pb.first_name, pb.phone
    FROM phonebook pb
    WHERE pb.first_name ILIKE '%' || p || '%'
       OR pb.phone ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;

-- Function 2: pagination
CREATE OR REPLACE FUNCTION get_contacts_paginated(page_num INT, page_size INT)
RETURNS TABLE(id INT, first_name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT pb.id, pb.first_name, pb.phone
    FROM phonebook pb
    ORDER BY pb.id
    LIMIT page_size OFFSET (page_num - 1) * page_size;
END;
$$ LANGUAGE plpgsql;