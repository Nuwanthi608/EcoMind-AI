CREATE DATABASE IF NOT EXISTS ecomind_ai
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE ecomind_ai;

CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    confidence FLOAT NOT NULL,
    disposal_advice VARCHAR(1000) NOT NULL,
    impact_estimate VARCHAR(1000) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
