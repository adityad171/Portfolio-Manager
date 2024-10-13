
-- For deleting the existing database and to recreate it everytime we run the scripts
DROP DATABASE IF EXISTS REPORTS;

-- For creating and using the database called FLIPCART
CREATE DATABASE REPORTS;
USE REPORTS;

-- For deleting the existing tables and to have no conflicts of foreign keys while deleting tables
SET FOREIGN_KEY_CHECKSsys_config=0;
DROP TABLE IF EXISTS Performance;
DROP TABLE IF EXISTS Risk;
SET FOREIGN_KEY_CHECKS=1;


-- Table creation of each entity --
CREATE TABLE Performance(
report_id int(10) PRIMARY KEY,
portfolio_id int(10) not null,
time_period time,
sharpe double,
alpha double,
beta double
);

CREATE TABLE Risk(
portfolio_id int(10) PRIMARY KEY,
time_period time,
risk_score double,
std_dev double,
volatility double
);