-- ================================================================
-- 05_extract_raw_data.sql — Ecommerce Production Data Extraction
-- ================================================================

SELECT
    o.order_id,
    o.order_date,
    c.first_name AS customer_first_name,
    c.last_name AS customer_last_name,
    p.product_name,
    p.category AS product_category,
    s.store_name,
    o.quantity,
    o.total_amount,
    o.status,
    o.is_returned,
    r.rating AS review_rating
FROM ecommerce.orders o
LEFT JOIN ecommerce.customers c ON o.customer_id = c.customer_id
LEFT JOIN ecommerce.products p ON o.product_id = p.product_id
LEFT JOIN ecommerce.sellers s ON o.seller_id = s.seller_id
LEFT JOIN ecommerce.reviews r ON o.order_id = r.order_id
LIMIT 50;