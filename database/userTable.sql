-- Query all data
SELECT * FROM public.users
ORDER BY id ASC LIMIT 100;

-- Truncate to delete all data in table (Recomment for table have relationship)
TRUNCATE TABLE users CASCADE;

-- Delete data in table
DELETE FROM orders;
DELETE FROM users;

-- Query all data with condition
SELECT * FROM public.users WHERE isDeleted='False'