-- 1. Product
CREATE TABLE Product (
  product_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  category VARCHAR(50) NOT NULL,
  warranty_years INT NOT NULL,
  image_url VARCHAR(255),
  PRIMARY KEY (product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Supplier
CREATE TABLE Supplier (
  supplier_id INT NOT NULL AUTO_INCREMENT,
  supplier_name VARCHAR(100) NOT NULL,
  contact VARCHAR(100),
  PRIMARY KEY (supplier_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2.1 Supplier_Product (Many-to-Many)
CREATE TABLE Supplier_Product (
  supplier_id INT NOT NULL,
  product_id INT NOT NULL,
  PRIMARY KEY (supplier_id, product_id),
  INDEX idx_sp_supplier (supplier_id),
  INDEX idx_sp_product (product_id),
  CONSTRAINT fk_sp_supplier
    FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_sp_product
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Customer
CREATE TABLE Customer (
  customer_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  contact VARCHAR(100),
  address VARCHAR(255),
  PRIMARY KEY (customer_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. User
CREATE TABLE `User` (
  user_id INT NOT NULL AUTO_INCREMENT,
  account VARCHAR(50) NOT NULL UNIQUE,
  pwd_hash VARCHAR(255) NOT NULL,
  role_id INT NOT NULL,
  PRIMARY KEY (user_id),
  CONSTRAINT fk_user_role
    FOREIGN KEY (role_id) REFERENCES Role(role_id)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Role
CREATE TABLE Role (
  role_id INT NOT NULL AUTO_INCREMENT,
  role_name VARCHAR(50) NOT NULL UNIQUE,
  PRIMARY KEY (role_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5.1 User_Role (Many-to-Many)
CREATE TABLE User_Role (
  user_id INT NOT NULL,
  role_id INT NOT NULL,
  PRIMARY KEY (user_id, role_id),
  INDEX idx_ur_user (user_id),
  INDEX idx_ur_role (role_id),
  CONSTRAINT fk_ur_user
    FOREIGN KEY (user_id) REFERENCES `User`(user_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_ur_role
    FOREIGN KEY (role_id) REFERENCES Role(role_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. Shipping_Vendor
CREATE TABLE Shipping_Vendor (
  user_id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  mode VARCHAR(50) NOT NULL,
  PRIMARY KEY (user_id),
  INDEX idx_sv_user (user_id),
  CONSTRAINT fk_sv_user
    FOREIGN KEY (user_id) REFERENCES `User`(user_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. Order
CREATE TABLE `Order` (
  order_id INT NOT NULL AUTO_INCREMENT,
  order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  status VARCHAR(50) NOT NULL,
  ship_to VARCHAR(255) NOT NULL,
  customer_id INT NOT NULL,
  user_id INT NOT NULL,
  PRIMARY KEY (order_id),
  INDEX idx_ord_customer (customer_id),
  INDEX idx_ord_user (user_id),
  CONSTRAINT fk_ord_customer
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_ord_user
    FOREIGN KEY (user_id) REFERENCES `User`(user_id)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7.1 Order_Item
CREATE TABLE Order_Item (
  order_item_id INT NOT NULL AUTO_INCREMENT,
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL,
  PRIMARY KEY (order_item_id),
  INDEX idx_oi_order (order_id),
  INDEX idx_oi_product (product_id),
  CONSTRAINT fk_oi_order
    FOREIGN KEY (order_id) REFERENCES `Order`(order_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_oi_product
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. Shipment
CREATE TABLE Shipment (
  shipment_id INT NOT NULL AUTO_INCREMENT,
  ship_date DATETIME NOT NULL,
  tracking_no VARCHAR(100) NOT NULL,
  status VARCHAR(50) NOT NULL,
  order_id INT NOT NULL,
  shipping_vendor_id INT NOT NULL,
  PRIMARY KEY (shipment_id),
  INDEX idx_ship_order (order_id),
  INDEX idx_ship_vendor (shipping_vendor_id),
  CONSTRAINT fk_ship_order
    FOREIGN KEY (order_id) REFERENCES `Order`(order_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_ship_vendor
    FOREIGN KEY (shipping_vendor_id) REFERENCES Shipping_Vendor(user_id)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 9. Location
CREATE TABLE Location (
  location_id INT NOT NULL AUTO_INCREMENT,
  location_code VARCHAR(50) NOT NULL UNIQUE,
  location_name VARCHAR(100) NOT NULL,
  zone VARCHAR(50) NOT NULL,
  shelf VARCHAR(50) NOT NULL,
  location_type VARCHAR(50) NOT NULL DEFAULT 'storage',
  capacity INT NOT NULL DEFAULT 0,
  status VARCHAR(20) NOT NULL DEFAULT 'active',
  notes TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (location_id),
  INDEX idx_location_code (location_code),
  INDEX idx_location_zone (zone),
  INDEX idx_location_type (location_type),
  INDEX idx_location_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 9.1 Inventory_Lot
CREATE TABLE Inventory_Lot (
  product_id INT NOT NULL,
  location_id INT NOT NULL,
  quantity INT NOT NULL DEFAULT 0,
  expiry_date DATE,
  PRIMARY KEY (product_id, location_id),
  INDEX idx_il_product (product_id),
  INDEX idx_il_location (location_id),
  CONSTRAINT fk_il_product
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_il_location
    FOREIGN KEY (location_id) REFERENCES Location(location_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 10. Scrap
CREATE TABLE Scrap (
  scrap_id INT NOT NULL AUTO_INCREMENT,
  product_id INT NOT NULL,
  location_id INT NOT NULL,
  quantity INT NOT NULL,
  scrap_date DATE NOT NULL,
  reason VARCHAR(255) NOT NULL,
  PRIMARY KEY (scrap_id),
  INDEX idx_scrap_product (product_id),
  INDEX idx_scrap_location (location_id),
  CONSTRAINT fk_scrap_product
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_scrap_location
    FOREIGN KEY (location_id) REFERENCES Location(location_id)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;