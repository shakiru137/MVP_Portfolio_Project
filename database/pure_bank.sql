-- Create the database if it does not exist
CREATE DATABASE IF NOT EXISTS PURE_BANK;

-- Select the 'PURE_BANK' database to use for subsequent operations
USE PURE_BANK;

-- Create the 'accounts' table with the appropriate columns
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
  balance FLOAT,

  -- Define an 'account_number' column with a fixed length of 10 characters
  account_number CHAR(10) UNIQUE,

  -- Define a 'pin' column with a a fixed length of 4 characters
  pin CHAR(4)
);

-- Create the 'transactions' table with the appropriate columns
CREATE TABLE IF NOT EXISTS transactions (
  -- Define a 'transaction_number' column with a character type of 18 characters and set it as the primary key
  transaction_number CHAR(18) PRIMARY KEY,
  
  -- Define an 'account_number' column with a fixed length of 10 characters
  account_number CHAR(10),
  
  -- Define a 'type' column with a variable character type of up to 50 characters
  type VARCHAR(50),
  
  -- Define an 'amount' column with a decimal type (up to 10 digits, 2 decimal places)
  amount DECIMAL(10, 2),
  
  -- Define a 'timestamp' column with a datetime type, defaulting to the current timestamp
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  
  -- Define a 'description' column for transaction description
  description VARCHAR(255),
  
  -- Define a foreign key constraint referencing the 'accounts' table
  FOREIGN KEY (account_number) REFERENCES accounts(account_number)
);