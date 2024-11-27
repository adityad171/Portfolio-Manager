
-- For deleting the existing database and to recreate it everytime we run the scripts
DROP DATABASE IF EXISTS Market;

-- For creating and using the database called FLIPCART
CREATE DATABASE Market;
USE Market;

-- For deleting the existing tables and to have no conflicts of foreign keys while deleting tables
DROP TABLE IF EXISTS Stocks;
DROP TABLE IF EXISTS Mutual_Funds;
DROP TABLE IF EXISTS Commodity;

-- Table creation of each entity --
CREATE TABLE Stocks(
Stock_id int(10) not Null,
Symbol varchar(50) Not null,
Name varchar(50) Not null,
Date long not null,
Price double not null
);

CREATE TABLE Mutual_Funds(
MF_id int(10) not Null,
Name varchar(500) Not null,
Date date not null,
nav double not null
);

CREATE TABLE Commodity(
commodity_id int(10) not null,
Symbol varchar(50) Not null,
Name varchar(50) Not null,
Date date not null,
rate double not null
);

insert into Stocks (stock_id, Symbol, name, date, price) values ('3','exp', 'example_asset', '2023-10-24', '10.0');
insert into Stocks (stock_id, Symbol, name, date, price) values ('3','exp', 'example_asset', '2024-04-24', '20.0');
insert into Stocks (stock_id, Symbol, name, date, price) values ('3','exp', 'example_asset', '2024-09-24', '25.0');
insert into Stocks (stock_id, Symbol, name, date, price) values ('3','exp', 'example_asset', '2024-10-24', '30.0');

insert into Stocks (stock_id, Symbol, name, date, price) values ('4','exp2', 'example_asset_2', '2023-10-24', '10.0');
insert into Stocks (stock_id, Symbol, name, date, price) values ('4','exp2', 'example_asset_2', '2024-04-24', '20.0');
insert into Stocks (stock_id, Symbol, name, date, price) values ('4','exp2', 'example_asset_2', '2024-09-24', '25.0');
insert into Stocks (stock_id, Symbol, name, date, price) values ('4','exp2', 'example_asset_2', '2024-10-24', '30.0');

insert into Stocks (stock_id, Symbol, name, date, price) values ('3','exp', 'example_asset', '2024-10-25', '10.5');
