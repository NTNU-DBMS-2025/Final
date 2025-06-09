/* ========== 今日出貨清單 ========== */
CREATE OR REPLACE VIEW v_shipments_today AS
SELECT s.*
FROM Shipment s
WHERE DATE(s.ship_date) = CURDATE();

/* ========== 已過期仍有庫存 ========== */
CREATE OR REPLACE VIEW v_inventory_expired AS
SELECT il.*, p.name AS product_name, l.location_name AS location_name
FROM Inventory_Lot il
JOIN Product  p ON p.product_id  = il.product_id
JOIN Location l ON l.location_id = il.location_id
WHERE il.expiry_date < CURDATE()
  AND il.quantity > 0;

/* ========== 低庫存（低於 reorder_point）========== */
CREATE OR REPLACE VIEW v_low_stock AS
SELECT il.*, p.name AS product_name, l.zone
FROM Inventory_Lot il
JOIN Product  p ON p.product_id  = il.product_id
JOIN Location l ON l.location_id = il.location_id
WHERE il.quantity < p.reorder_point;

/* ========== 尚未處理的 ========== */
CREATE OR REPLACE VIEW v_orders_pending AS
SELECT   order_id, order_number, expected_delivery_date, priority, ship_to, total_amount, customer_id, status
FROM `order`
WHERE status = 'pending';

/* ========== 今天應到貨但尚未到 ========== */
CREATE OR REPLACE VIEW v_orders_arrived_today AS
SELECT *
FROM `Order`
WHERE expected_delivery_date = CURDATE()
  AND status != 'delivered';

/* ========== 今天預計出貨但尚未出貨 ========== */
CREATE OR REPLACE VIEW v_orders_unshipped_today AS
SELECT o.*
FROM `Order` o
LEFT JOIN Shipment s ON s.order_id = o.order_id
WHERE DATE(o.expected_delivery_date) = CURDATE()
  AND o.status = 'pending'
  AND s.shipment_id IS NULL;

/* ========== 近 30 天銷售彙總（每日） ========== */
CREATE OR REPLACE VIEW v_sales_30d AS
SELECT
  DATE(o.order_date)           AS sales_day,
  COUNT(DISTINCT o.order_id)   AS orders_cnt,
  SUM(oi.quantity)             AS units_sold,
  SUM(oi.quantity*oi.unit_price) AS total_amount
FROM `Order`     o
JOIN Order_Item  oi USING(order_id)
WHERE o.order_date >= CURDATE() - INTERVAL 30 DAY
GROUP BY DATE(o.order_date)
ORDER BY sales_day DESC;


/* ========== 最近 7 天各訂單狀態統計 ========== */
CREATE OR REPLACE VIEW v_orders_status_7d AS
SELECT
  DATE(o.order_date)               AS stats_day,
  o.status,
  COUNT(*)                         AS orders_cnt,
  SUM(o.total_amount)              AS total_amount
FROM `Order` o
WHERE o.order_date >= CURDATE() - INTERVAL 7 DAY
GROUP BY DATE(o.order_date), o.status;

/* ========== 不同客戶類型平均訂單金額 ========== */
CREATE OR REPLACE VIEW v_avg_order_value_by_cust_type AS
SELECT
  c.customer_type,
  AVG(o.total_amount) AS avg_order_value,
  COUNT(*)            AS orders_cnt
FROM `Order` o
JOIN Customer c ON c.customer_id = o.customer_id
GROUP BY c.customer_type;

/* ========== 零庫存產品清單 ========== */
CREATE OR REPLACE VIEW v_products_out_of_stock AS
SELECT p.*
FROM Product p
LEFT JOIN Inventory_Lot il ON il.product_id = p.product_id
GROUP BY p.product_id
HAVING COALESCE(SUM(il.quantity), 0) = 0;

/* ========== 已滿載或超載 ========== */
CREATE OR REPLACE VIEW v_locations_over_capacity AS
SELECT
  l.location_id,
  l.location_code,
  l.capacity,
  COALESCE(SUM(il.quantity),0) AS occupied
FROM Location l
LEFT JOIN Inventory_Lot il ON il.location_id = l.location_id
GROUP BY l.location_id, l.capacity
HAVING occupied >= l.capacity;

/* ========== 產品「天數供應量」(Days of Supply) ========== */
CREATE OR REPLACE VIEW v_product_days_of_supply AS
WITH shipped_30d AS (
  SELECT
    oi.product_id,
    SUM(oi.quantity) AS sold_qty_30d
  FROM `Order` o
  JOIN Order_Item oi USING(order_id)
  WHERE o.order_date >= CURDATE() - INTERVAL 30 DAY
  GROUP BY oi.product_id
)
SELECT
  p.product_id,
  p.name,
  COALESCE(SUM(il.quantity),0)                 AS on_hand,
  COALESCE(s.sold_qty_30d,0)                   AS sold_30d,
  CASE
    WHEN COALESCE(s.sold_qty_30d,0) = 0 THEN NULL
    ELSE ROUND( (SUM(il.quantity) / s.sold_qty_30d) * 30 , 1 )
  END AS days_of_supply
FROM Product p
LEFT JOIN Inventory_Lot il ON il.product_id = p.product_id
LEFT JOIN shipped_30d s     ON s.product_id = p.product_id
GROUP BY p.product_id;

/* ========== 產品報廢率 (%) ========== */
CREATE OR REPLACE VIEW v_product_scrap_rate AS
WITH shipped AS (
  SELECT
    oi.product_id,
    SUM(oi.quantity) AS shipped_qty
  FROM `Order` o
  JOIN Order_Item oi USING(order_id)
  GROUP BY oi.product_id
), scrapped AS (
  SELECT
    product_id,
    SUM(quantity) AS scrap_qty
  FROM Scrap
  GROUP BY product_id
)
SELECT
  p.product_id,
  p.name,
  s.shipped_qty,
  sc.scrap_qty,
  ROUND( sc.scrap_qty / NULLIF(s.shipped_qty,0) * 100 , 2) AS scrap_rate_pct
FROM Product p
LEFT JOIN shipped  s  ON s.product_id  = p.product_id
LEFT JOIN scrapped sc ON sc.product_id = p.product_id;



/* ========== 物流商延遲出貨件數 ========== */
CREATE OR REPLACE VIEW v_vendor_delay_cnt AS
SELECT
  sv.name AS shipping_vendor,
  COUNT(*) AS delayed_shipments
FROM Shipment s
JOIN Shipping_Vendor sv ON sv.user_id = s.shipping_vendor_id
WHERE s.status IN ('pending','in_transit')
  AND s.estimated_delivery_date < CURDATE()
GROUP BY sv.name;

/* ========== 本月報廢成本彙總 ========== */
CREATE OR REPLACE VIEW v_scrap_cost_month AS
SELECT
  DATE_FORMAT(scrap_date,'%Y-%m') AS month,
  SUM(estimated_value)             AS total_scrap_cost,
  COUNT(*)                         AS scrap_records
FROM Scrap
WHERE DATE_FORMAT(scrap_date,'%Y-%m') = DATE_FORMAT(CURDATE(),'%Y-%m')
GROUP BY DATE_FORMAT(scrap_date,'%Y-%m');

/* ==========30 天內銷售最快前 10 名產品 ========== */
CREATE OR REPLACE VIEW v_fast_moving_top10 AS
SELECT
  p.product_id,
  p.name,
  SUM(oi.quantity) AS sold_qty_30d
FROM `Order` o
JOIN Order_Item oi USING(order_id)
JOIN Product p ON p.product_id = oi.product_id
WHERE o.order_date >= CURDATE() - INTERVAL 30 DAY
GROUP BY p.product_id
ORDER BY sold_qty_30d DESC
LIMIT 10;

/* ==========60 天未動撥庫存 (Idle Inventory) ========== */
CREATE OR REPLACE VIEW v_idle_inventory_60d AS
SELECT
  il.product_id,
  il.location_id,
  il.quantity,
  il.expiry_date,
  p.name AS product_name,
  MAX(o.order_date) AS last_movement
FROM Inventory_Lot il
JOIN Product p ON p.product_id = il.product_id
LEFT JOIN Order_Item oi ON oi.product_id = p.product_id
LEFT JOIN `Order`    o  ON o.order_id = oi.order_id
GROUP BY il.product_id, il.location_id
HAVING COALESCE(MAX(o.order_date), '1900-01-01') < CURDATE() - INTERVAL 60 DAY;

/* ==========產品分類庫存結構 ========== */
CREATE OR REPLACE VIEW v_inventory_by_category AS
SELECT
  p.category,
  SUM(il.quantity) AS total_qty
FROM Product p
LEFT JOIN Inventory_Lot il ON il.product_id = p.product_id
GROUP BY p.category;

/* ==========每日平均訂單處理時間 ========== */
CREATE OR REPLACE VIEW v_avg_order_processing_time AS
SELECT
  DATE(o.order_date) AS process_day,
  AVG(DATEDIFF(s.estimated_shipping_date , o.order_date)) AS avg_days
FROM `Order` o
JOIN Shipment s ON s.order_id = o.order_id
GROUP BY DATE(o.order_date);

/* ==========客戶最後一次下單日期 ========== */
CREATE OR REPLACE VIEW v_customer_last_order AS
SELECT
  c.customer_id,
  c.name           AS customer_name,
  MAX(o.order_date) AS last_order_date
FROM Customer c
LEFT JOIN `Order` o ON o.customer_id = c.customer_id
GROUP BY c.customer_id;

/* ==========庫存批號即將到期 (30 天內) ========== */
CREATE OR REPLACE VIEW v_lot_expiry_alert AS
SELECT
  il.product_id,
  il.location_id,
  p.name           AS product_name,
  il.quantity,
  il.expiry_date,
  DATEDIFF(il.expiry_date, CURDATE()) AS days_left
FROM Inventory_Lot il
JOIN Product p ON p.product_id = il.product_id
WHERE il.expiry_date BETWEEN CURDATE() AND CURDATE() + INTERVAL 30 DAY
ORDER BY il.expiry_date;

/* ==========供應商產品種類數量排行榜 ========== */
CREATE OR REPLACE VIEW v_supplier_product_variants AS
SELECT
  s.supplier_id,
  s.supplier_name,
  COUNT(DISTINCT sp.product_id) AS product_variants
FROM Supplier s
JOIN Supplier_Product sp ON sp.supplier_id = s.supplier_id
GROUP BY s.supplier_id
ORDER BY product_variants DESC;


/* ==========未出貨訂單超過三天 ========== */
CREATE OR REPLACE VIEW v_orders_delayed_shipping AS
SELECT o.*
FROM `Order` o
LEFT JOIN Shipment s ON s.order_id = o.order_id
WHERE o.status = 'pending'
  AND DATEDIFF(CURDATE(), o.order_date) > 3;


/* ==========本週即將出貨訂單預覽 ========== */
CREATE OR REPLACE VIEW v_orders_to_ship_this_week AS
SELECT *
FROM `Order`
WHERE expected_delivery_date BETWEEN CURDATE() AND CURDATE() + INTERVAL 7 DAY;