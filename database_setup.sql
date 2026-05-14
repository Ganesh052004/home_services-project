-- ============================================================
-- HomeFixr Database Setup
-- Run this in phpMyAdmin (XAMPP) or MySQL CLI
-- ============================================================

-- Step 1: Create Database
CREATE DATABASE IF NOT EXISTS homefixr;
USE homefixr;

-- Step 2: Workers Table
CREATE TABLE IF NOT EXISTS workers (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  name        VARCHAR(100) NOT NULL,
  phone       VARCHAR(15)  NOT NULL,
  email       VARCHAR(100),
  category    VARCHAR(50)  NOT NULL,
  city        VARCHAR(100) NOT NULL,
  experience  INT          DEFAULT 0,
  rate        INT          DEFAULT 0,
  about       TEXT,
  created_at  DATETIME     DEFAULT CURRENT_TIMESTAMP
);

-- Step 3: Bookings Table
CREATE TABLE IF NOT EXISTS bookings (
  id               INT AUTO_INCREMENT PRIMARY KEY,
  cust_name        VARCHAR(100) NOT NULL,
  cust_phone       VARCHAR(15)  NOT NULL,
  cust_address     TEXT         NOT NULL,
  service_category VARCHAR(50)  NOT NULL,
  worker_name      VARCHAR(100),
  booking_date     DATE         NOT NULL,
  booking_time     TIME         NOT NULL,
  description      TEXT         NOT NULL,
  status           VARCHAR(30)  DEFAULT 'Pending',
  created_at       DATETIME     DEFAULT CURRENT_TIMESTAMP
);

-- Step 4: Sample Worker Data (for testing)
INSERT INTO workers (name, phone, email, category, city, experience, rate, about) VALUES
('Rajesh Kumar',   '9876543210', 'rajesh@email.com',  'Plumber',       'Bengaluru', 8, 350, 'Expert in pipe fitting and bathroom work'),
('Sunil Mehta',    '9812345678', 'sunil@email.com',   'Electrician',   'Bengaluru', 6, 400, 'Wiring, switchboard repair, inverter installation'),
('Arun Sharma',    '9823456789', 'arun@email.com',    'Carpenter',     'Mumbai',    10, 500, 'Furniture repair, door fitting, custom woodwork'),
('Ramesh Nair',    '9834567890', 'ramesh@email.com',  'Painter',       'Chennai',   5, 300, 'Interior and exterior painting, waterproofing'),
('Vikram Singh',   '9845678901', 'vikram@email.com',  'AC Technician', 'Bengaluru', 7, 450, 'AC service, gas refilling, installation'),
('Mohan Das',      '9856789012', 'mohan@email.com',   'Cleaner',       'Hyderabad', 3, 250, 'Deep cleaning, sofa cleaning, kitchen cleaning');

-- Done!
SELECT 'Database setup complete!' AS Status;
