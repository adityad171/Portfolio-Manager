
-- For deleting the existing database and to recreate it everytime we run the scripts
DROP DATABASE IF EXISTS PORTFOLIOS;

-- For creating and using the database called FLIPCART
CREATE DATABASE PORTFOLIOS;
USE PORTFOLIOS;

-- For deleting the existing tables and to have no conflicts of foreign keys while deleting tables
DROP TABLE IF EXISTS Portfolio;
DROP TABLE IF EXISTS Asset;

-- Table creation of each entity --
CREATE TABLE Portfolio(
portfolio_id int(10) PRIMARY KEY,
user_id int(10) Not null
);

CREATE TABLE Asset(
asset_id int(10) not null,
portfolio_id int(10) Not null,
asset_name varchar(50) not null,
asset_type varchar(20) NOT NULL,
quantity int(10) NOT NULL,
purchase_price double NOT NULL,
current_price double
);

insert into portfolio (portfolio_id, user_id) values ('1','0275817784');
insert into asset (asset_id, portfolio_id, asset_name, asset_type,quantity, purchase_price, current_price) values ('3','1', 'example_asset', 'stock', '2', '10.0', '12.2');
insert into asset (asset_id, portfolio_id, asset_name, asset_type,quantity, purchase_price, current_price) values ('5','1', 'example_asset_2', 'MF', '5', '25.0', '9.1');
