
-- For deleting the existing database and to recreate it everytime we run the scripts
DROP DATABASE IF EXISTS PORTFOLIOS;

-- For creating and using the database called FLIPCART
CREATE DATABASE PORTFOLIOS;
USE PORTFOLIOS;

-- For deleting the existing tables and to have no conflicts of foreign keys while deleting tables
SET FOREIGN_KEY_CHECKSsys_config=0;
DROP TABLE IF EXISTS Portfolio;
DROP TABLE IF EXISTS Asset;
DROP TABLE IF EXISTS Transactions;
SET FOREIGN_KEY_CHECKS=1;


-- Table creation of each entity --
CREATE TABLE Portfolio(
portfolio_id int(10) PRIMARY KEY,
user_id int(10) Not null
);

CREATE TABLE Asset(
asset_id int(10) PRIMARY KEY,
portfolio_id int(10) Not null,
asset_name varchar(50) unique not null,
asset_type varchar(20) NOT NULL,
quantity int(10) NOT NULL,
purchase_price double NOT NULL,
current_price double NOT NULL
);

CREATE TABLE Transactions(
transaction_id int(10) PRIMARY KEY,
portfolio_id int(10) NOT NULL,
asset_id int(10) NOT NULL,
transaction_type varchar(50) UNIQUE NOT NULL,
quantity int(10) NOT NULL,
price double NOT NULL,
exec_date datetime(10) NOT NULL
);
