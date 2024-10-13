
-- For deleting the existing database and to recreate it everytime we run the scripts
DROP DATABASE IF EXISTS Market;

-- For creating and using the database called FLIPCART
CREATE DATABASE Market;
USE Market;

-- For deleting the existing tables and to have no conflicts of foreign keys while deleting tables
SET FOREIGN_KEY_CHECKSsys_config=0;
DROP TABLE IF EXISTS Stocks;
DROP TABLE IF EXISTS Mutual_Funds;
DROP TABLE IF EXISTS Commodity;
SET FOREIGN_KEY_CHECKS=1;


-- Table creation of each entity --
CREATE TABLE Stocks(
Stock_id int(10) PRIMARY KEY,
Symbol varchar(50) UNIQUE Not null,
Name varchar(50) UNIQUE Not null,
Date_time datetime(10) not null,
Price double not null,
Country varchar(50) Not null
);

CREATE TABLE Mutual_Funds(
MF_id int(10) PRIMARY KEY,
Symbol varchar(50) UNIQUE Not null,
Name varchar(50) UNIQUE Not null,
Date_time datetime(10) not null,
Price double not null,
Country varchar(50) Not null
);

CREATE TABLE Commodity(
commodity_id int(10) PRIMARY KEY,
Name varchar(50) UNIQUE Not null,
Date_time datetime(10) not null,
Price double not null,
Country varchar(50) Not null
);
