DROP TABLE IF EXISTS test_schema.bank_markerting;

CREATE SCHEMA IF NOT EXISTS test_schema;

CREATE TABLE IF NOT EXISTS test_schema.bank_markerting (
    age                    INT
  , job                    VARCHAR(50)   
  , marital                VARCHAR(50)   
  , education              VARCHAR(50)   
  , `default`              VARCHAR(50)   
  , housing                VARCHAR(50)   
  , loan                   VARCHAR(50)   
  , contact                VARCHAR(50)   
  , month                  VARCHAR(50)   
  , day_of_week            INT  
  , duration               INT   
  , campaign               INT   
  , pdays                  INT   
  , previous               INT   
  , poutcome               VARCHAR(50)   
  , `emp.var.rate`           DECIMAL(18,8)   
  , `cons.price.idx`         DECIMAL(18,8)   
  , `cons.conf.idx`          DECIMAL(18,8)   
  , euribor3m              DECIMAL(18,8)   
  , nr_employed            INT   
  , y                      VARCHAR(50)
)

ALTER TABLE test_schema.bank_markerting COMMENT = '은행_마켓팅';

ALTER TABLE test_schema.bank_markerting MODIFY age INT COMMENT '나이';
ALTER TABLE test_schema.bank_markerting MODIFY job VARCHAR(50) COMMENT '직업';
ALTER TABLE test_schema.bank_markerting MODIFY marital VARCHAR(50) COMMENT '컬럼1';
ALTER TABLE test_schema.bank_markerting MODIFY education VARCHAR(50) COMMENT '컬럼2';
ALTER TABLE test_schema.bank_markerting MODIFY `default` VARCHAR(50) COMMENT '컬럼3';
ALTER TABLE test_schema.bank_markerting MODIFY housing VARCHAR(50) COMMENT '컬럼4';
ALTER TABLE test_schema.bank_markerting MODIFY loan VARCHAR(50) COMMENT '컬럼5';
ALTER TABLE test_schema.bank_markerting MODIFY contact VARCHAR(50) COMMENT '컬럼6';
ALTER TABLE test_schema.bank_markerting MODIFY month VARCHAR(50) COMMENT '컬럼7';
ALTER TABLE test_schema.bank_markerting MODIFY day_of_week VARCHAR(50) COMMENT '컬럼8';
ALTER TABLE test_schema.bank_markerting MODIFY duration INT COMMENT '컬럼9';
ALTER TABLE test_schema.bank_markerting MODIFY campaign INT COMMENT '컬럼10';
ALTER TABLE test_schema.bank_markerting MODIFY pdays INT COMMENT '컬럼11';
ALTER TABLE test_schema.bank_markerting MODIFY previous INT COMMENT '컬럼12';
ALTER TABLE test_schema.bank_markerting MODIFY poutcome VARCHAR(50) COMMENT '컬럼13';
ALTER TABLE test_schema.bank_markerting MODIFY `emp.var.rate` DECIMAL(18,8) COMMENT '컬럼14';
ALTER TABLE test_schema.bank_markerting MODIFY `cons.price.idx` DECIMAL(18,8) COMMENT '컬럼15';
ALTER TABLE test_schema.bank_markerting MODIFY `cons.conf.idx` DECIMAL(18,8) COMMENT '컬럼16';
ALTER TABLE test_schema.bank_markerting MODIFY euribor3m DECIMAL(18,8) COMMENT '컬럼17';
ALTER TABLE test_schema.bank_markerting MODIFY nr_employed INT COMMENT '컬럼18';
ALTER TABLE test_schema.bank_markerting MODIFY y VARCHAR(50) COMMENT '컬럼19';

ANALYZE TABLE test_schema.bank_markerting;


ALTER TABLE test_schema.bank_markerting DROP COLUMN IF EXISTS cust_id;
ALTER TABLE test_schema.bank_markerting ADD COLUMN cust_id INT AUTO_INCREMENT, ADD CONSTRAINT cust_pkey PRIMARY KEY (cust_id);
ALTER TABLE test_schema.bank_markerting MODIFY COLUMN cust_id INT AUTO_INCREMENT AFTER age;
ALTER TABLE test_schema.bank_markerting MODIFY COLUMN age INT NOT NULL AFTER cust_id;