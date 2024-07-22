-- create the database if it does not exist
CREATE DATABASE IF NOT EXISTS mybank;
-- Select the 'mybank' database to use for subsequent operations
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

-- Create a table named 'transactions'
CREATE TABLE transactions (
  -- Define an 'id' column with an integer type, auto-increment, and set it as the primary key
  id INT AUTO_INCREMENT PRIMARY KEY,
  
  -- Define an 'account_id' column with an integer type
  account_id INT,
  
  -- Define a 'type' column with a variable character type of up to 50 characters
  type VARCHAR(50),
  
  -- Define an 'amount' column with a decimal type (up to 10 digits, 2 decimal places)
  amount DECIMAL(10, 2),
  
  -- Define a 'timestamp' column with a datetime type, defaulting to the current timestamp
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  
  -- Define a foreign key constraint referencing the 'accounts' table
  FOREIGN KEY (account_id) REFERENCES accounts(id)
);
