/********************************************************************
  Bacchus Winery – Milestone 2
  final_schema_with_sample_data.sql
  (schema name = winery)
********************************************************************/

DROP DATABASE IF EXISTS winery;
CREATE DATABASE winery DEFAULT CHARACTER SET utf8;
USE winery;

/* ─────────────────────────────────────
   TABLE DEFINITIONS
   ───────────────────────────────────── */

CREATE TABLE employees (
  employee_id INT NOT NULL AUTO_INCREMENT,
  first_name  VARCHAR(45),
  last_name   VARCHAR(45),
  job_title   VARCHAR(45),
  PRIMARY KEY (employee_id)
) ENGINE=InnoDB;

CREATE TABLE hours (
  time_id     INT NOT NULL AUTO_INCREMENT,
  employee_id INT NOT NULL,
  quarter     TINYINT,
  hours       DECIMAL(7,2),
  PRIMARY KEY (time_id),
  INDEX employee_id_idx (employee_id),
  CONSTRAINT fk_employee_id
    FOREIGN KEY (employee_id)
    REFERENCES employees (employee_id)
) ENGINE=InnoDB;

CREATE TABLE suppliers (
  supplier_id   INT NOT NULL AUTO_INCREMENT,
  supplier_name VARCHAR(45) NOT NULL,
  PRIMARY KEY (supplier_id),
  UNIQUE (supplier_name)
) ENGINE=InnoDB;

CREATE TABLE distributors (
  distributor_id   INT NOT NULL AUTO_INCREMENT,
  distributor_name VARCHAR(45) NOT NULL,
  PRIMARY KEY (distributor_id),
  UNIQUE (distributor_name)
) ENGINE=InnoDB;

CREATE TABLE supply_orders (
  order_id      INT NOT NULL AUTO_INCREMENT,
  supplier_id   INT NOT NULL,
  date_expected DATE,
  date_received DATE,
  PRIMARY KEY (order_id),
  INDEX supplier_id_idx (supplier_id),
  CONSTRAINT fk_supplier_id
    FOREIGN KEY (supplier_id)
    REFERENCES suppliers (supplier_id)
) ENGINE=InnoDB;

CREATE TABLE supplies (
  supply_id   INT NOT NULL AUTO_INCREMENT,
  supply_name VARCHAR(255) NOT NULL,
  on_hand     INT,
  PRIMARY KEY (supply_id),
  UNIQUE (supply_name)
) ENGINE=InnoDB;

CREATE TABLE supply_order_details (
  order_id  INT NOT NULL,
  supply_id INT NOT NULL,
  quantity  INT,
  PRIMARY KEY (order_id,supply_id),
  INDEX supply_id_idx (supply_id),
  CONSTRAINT fk_sod_order
    FOREIGN KEY (order_id)  REFERENCES supply_orders (order_id),
  CONSTRAINT fk_supply_id
    FOREIGN KEY (supply_id) REFERENCES supplies (supply_id)
) ENGINE=InnoDB;

CREATE TABLE wines (
  wine_id   INT NOT NULL AUTO_INCREMENT,
  wine_name VARCHAR(255) NOT NULL,
  in_stock  INT,
  PRIMARY KEY (wine_id),
  UNIQUE (wine_name)
) ENGINE=InnoDB;

CREATE TABLE distributor_orders (
  wine_order_id  INT NOT NULL AUTO_INCREMENT,
  distributor_id INT NOT NULL,
  order_placed   DATE,
  track_num      VARCHAR(30),
  PRIMARY KEY (wine_order_id),
  CONSTRAINT fk_distributor_id
    FOREIGN KEY (distributor_id)
    REFERENCES distributors (distributor_id)
) ENGINE=InnoDB;

CREATE TABLE wine_order_details (
  wine_order_id INT NOT NULL,
  wine_id       INT NOT NULL,
  quantity      INT,
  PRIMARY KEY (wine_order_id,wine_id),
  INDEX wine_id_idx (wine_id),
  CONSTRAINT fk_wine_order_id
    FOREIGN KEY (wine_order_id) REFERENCES distributor_orders (wine_order_id),
  CONSTRAINT fk_wine_id
    FOREIGN KEY (wine_id)       REFERENCES wines (wine_id)
) ENGINE=InnoDB;

/* ─────────────────────────────────────
   SAMPLE DATA
   ───────────────────────────────────── */

/* 1.  Employees (case-study names plus the two owners) */
INSERT INTO employees (first_name,last_name,job_title) VALUES
('Stan',     'Bacchus',    'Owner'),
('Davis',    'Bacchus',    'Owner'),
('Janet',    'Collins',    'Finance & Payroll Mgr'),
('Roz',      'Murphy',     'Marketing Director'),
('Bob',      'Ulrich',     'Marketing Assistant'),
('Henry',    'Doyle',      'Production Manager'),
('Maria',    'Costanza',   'Distribution Manager');

/* 2.  Hours (6 demo rows) */
INSERT INTO hours (employee_id,quarter,hours) VALUES
(3,1,410.0),
(4,1,395.5),
(5,1,380.0),
(6,1,420.0),
(7,1,415.5),
(3,2,405.0);

/* 3.  Suppliers (exactly the three in the narrative) */
INSERT INTO suppliers (supplier_name) VALUES
('Bottle & Cork Co.'),
('Label & Box Ltd.'),
('Vat & Tubing Inc.');

/* 4.  Distributors (≥6 demo rows) */
INSERT INTO distributors (distributor_name) VALUES
('FineWine USA'),
('Grapevine Wholesale'),
('Select Cellars'),
('Pacific Vintners'),
('Elite Beverage'),
('Sunset Imports');

/* 5.  Supplies (≥6 demo rows) */
INSERT INTO supplies (supply_name,on_hand) VALUES
('750 ml Bottles', 12000),
('Natural Corks',  15000),
('Wine Labels',     8000),
('Cardboard Boxes', 2000),
('Stainless Vats',     4),
('Transfer Tubing',  250);

/* 6.  Supply orders + details */
INSERT INTO supply_orders (supplier_id,date_expected,date_received) VALUES
(1,'2023-03-15','2023-03-16'),
(2,'2023-04-10','2023-04-15'),
(3,'2023-05-05',NULL),
(1,'2023-06-20','2023-06-20'),
(2,'2023-07-01',NULL),
(3,'2023-07-25',NULL);

INSERT INTO supply_order_details VALUES
(1,1,5000),(1,2,6000),
(2,3,4000),(2,4,1000),
(3,5,2),
(4,6,100);

/* 7.  Wines (four varieties in case study) */
INSERT INTO wines (wine_name,in_stock) VALUES
('Merlot',        500),
('Cabernet',      450),
('Chablis',       300),
('Chardonnay',    550);

/* 8.  Distributor orders + details */
INSERT INTO distributor_orders (distributor_id,order_placed,track_num) VALUES
(1,'2023-03-10','TRK1001'),
(2,'2023-03-15','TRK1002'),
(3,'2023-04-02','TRK1003'),
(4,'2023-04-18','TRK1004'),
(5,'2023-05-05','TRK1005'),
(6,'2023-05-20','TRK1006');

INSERT INTO wine_order_details VALUES
(1,1,120),(1,3,60),
(2,2,80),
(3,4,75),
(4,1,90),
(5,2,110);