-- Task 2: MySQL Schema for Ecommerce Sales Time-Series Data
-- Database: ecommerce_sales
-- Tables: categories, products, regions, orders (4 tables, normalized)

-- Create database
CREATE DATABASE IF NOT EXISTS ecommerce_sales;
USE ecommerce_sales;

-- Dimension table: product categories (Office, Accessories, Electronics)
CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE
);

-- Dimension table: regions (North, East, South, West)
CREATE TABLE regions (
    region_id INT AUTO_INCREMENT PRIMARY KEY,
    region_name VARCHAR(50) NOT NULL UNIQUE
);

-- Dimension table: products (linked to category)
CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE RESTRICT,
    UNIQUE KEY uk_product_category (product_name, category_id)
);

-- Fact table: orders (time-series records)
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    order_date DATE NOT NULL,
    product_id INT NOT NULL,
    region_id INT NOT NULL,
    quantity INT NOT NULL,
    sales DECIMAL(12, 2) NOT NULL,
    profit DECIMAL(12, 2) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT,
    FOREIGN KEY (region_id) REFERENCES regions(region_id) ON DELETE RESTRICT,
    INDEX idx_order_date (order_date),
    INDEX idx_product_region (product_id, region_id)
);
