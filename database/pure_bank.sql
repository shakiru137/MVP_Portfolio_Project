CREATE DATABASE IF NOT EXISTS mybank;
USE mybank;
CREATE TABLE IF NOT EXISTS accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    username VARCHAR(255),
    password VARCHAR(255),
    balance FLOAT
);

