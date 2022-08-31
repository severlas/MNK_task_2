from settings import HOME_URL

create_csv_file = f"""
-- CREATE ALL TABLE

CREATE TABLE data 
(
	part_number varchar(32),
	manufacturer varchar(32),
	main_part_number varchar(32),
	category varchar(128),
	origin varchar(10)                    
);  

CREATE TABLE price
(
	part_number varchar(32) PRIMARY KEY,
	price varchar(32)	
);

CREATE TABLE deposit
(
	part_number varchar(32) PRIMARY KEY,
	deposit varchar(32)	
);

CREATE TABLE quantity
(
	part_number varchar(32),
	quantity varchar(32),
	warehouse VARCHAR(10)
);

CREATE TABLE weight
(
	part_number varchar(32) PRIMARY KEY,
	weight_unpacked varchar(32),
	weight_packed varchar(32)
);

-- COPY DATA FROM FOLDER TASK_DATA

COPY data
FROM '{HOME_URL}/task_data/data.csv'
DELIMITER ';'
CSV HEADER;

COPY price
FROM '{HOME_URL}/task_data/price.csv'
DELIMITER ';'
CSV HEADER;

COPY deposit
FROM '{HOME_URL}/task_data/deposit.csv'
DELIMITER ';'
CSV HEADER;

COPY quantity
FROM '{HOME_URL}/task_data/quantity.csv'
DELIMITER ';'
CSV HEADER;

COPY weight
FROM '{HOME_URL}/task_data/weight.csv'
DELIMITER '\t'
CSV HEADER;

-- CORRECT ALL TABLE (ALTER PRIMARY KEY OR FOREIGN KEY), 
-- DECIDE PROBLEMS FOREIGN KEY
-- EDIT DATA TYPE COLUMN

DELETE FROM data AS d_a
USING data AS d_b
WHERE d_a.ctid < d_b.ctid
	AND d_a.part_number = d_b.part_number
	AND d_a.main_part_number = d_b.main_part_number
	AND d_a.category = d_b.category
	AND d_a.origin = d_b.origin;

ALTER TABLE data
ADD PRIMARY KEY (part_number);

UPDATE price SET
price = replace(price, ',', '.');

DELETE FROM price AS p
WHERE  NOT EXISTS (
   SELECT FROM data AS d
   WHERE  p.part_number = d.part_number
   );

ALTER TABLE price
ALTER COLUMN price TYPE decimal USING price::double precision;

ALTER TABLE price
ADD CONSTRAINT FK_part_number FOREIGN KEY(part_number) REFERENCES data(part_number);

UPDATE deposit SET
deposit = replace(deposit, ',', '.');

DELETE FROM deposit AS de
WHERE  NOT EXISTS (
   SELECT FROM data AS d
   WHERE  de.part_number = d.part_number
   );
   
ALTER TABLE deposit
ALTER COLUMN deposit TYPE numeric USING deposit::double precision;

ALTER TABLE deposit
ADD CONSTRAINT FK_part_number FOREIGN KEY(part_number) REFERENCES data(part_number);

DELETE FROM quantity AS q
WHERE  NOT EXISTS (
   SELECT FROM data AS d
   WHERE  q.part_number = d.part_number
   );

UPDATE quantity SET
quantity = replace(quantity, '>', '');

ALTER TABLE quantity
ALTER COLUMN quantity TYPE numeric USING quantity::double precision;
                    
ALTER TABLE quantity 
ADD CONSTRAINT FK_part_number FOREIGN KEY(part_number) REFERENCES data(part_number);

DELETE FROM weight AS w
WHERE  NOT EXISTS (
   SELECT FROM data AS d
   WHERE  w.part_number = d.part_number
   );
                    
ALTER TABLE weight
ADD CONSTRAINT FK_part_number FOREIGN KEY(part_number) REFERENCES data(part_number);


-- SELECT TASK

SELECT d.main_part_number, d.manufacturer, d.category, d.origin, p.price, 
coalesce(de.deposit, 0) AS deposit, p.price + coalesce(de.deposit, 0) AS total_price
FROM data AS d

INNER JOIN price AS p ON p.part_number = d.part_number
INNER JOIN quantity AS q ON q.part_number = d.part_number
LEFT JOIN deposit AS de ON de.part_number = d.part_number

WHERE q.warehouse IN('A', 'H', 'J', '3', '9')
    AND quantity != 0
    AND p.price + coalesce(de.deposit, 0) > 2.00

"""
