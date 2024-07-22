-- Create a database named 'mybank' if it does not already exist
CREATE DATABASE IF NOT EXISTS mybank;

-- Select the 'mybank' database touse for subsequent operations
USE mybank;

-- Create a table named 'accounts' if it does not already exist
CREATE TABLE IF NOT EXISTS accounts (
    -- Define an 'id' column with an integer type, auto-increment, and set it as the primary key
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Define a 'name' column with a variable character type of up to 255 characters
    name VARCHAR(255),
    
    -- Define a 'username' column with a variable character type of up to 255 characters
    username VARCHAR(255),
    
    -- Define a 'password' column with a variable character type of up to 255 characters
    password VARCHAR(255),
    
    -- Define a 'balance' column with a floating-point number type
    balance FLOAT
);
