-- Marketing Analytics Queries (SQLite)
-- ====================================

-- Overall response rate
CREATE VIEW v_response_rate AS
SELECT AVG(Response * 1.0) AS response_rate
FROM customers;

-- Campaign acceptance rates
CREATE VIEW v_campaign_rates AS
SELECT
  AVG(AcceptedCmp1 * 1.0) AS cmp1,
  AVG(AcceptedCmp2 * 1.0) AS cmp2,
  AVG(AcceptedCmp3 * 1.0) AS cmp3,
  AVG(AcceptedCmp4 * 1.0) AS cmp4,
  AVG(AcceptedCmp5 * 1.0) AS cmp5
FROM customers;

-- Segment-wise response
CREATE VIEW v_segment_response AS
SELECT 'Seg_High_Income' AS segment, AVG(Response * 1.0) AS rate
FROM customers WHERE Seg_High_Income = 1
UNION ALL
SELECT 'Seg_Young', AVG(Response * 1.0) FROM customers WHERE Seg_Young = 1
UNION ALL
SELECT 'Seg_Responder', AVG(Response * 1.0) FROM customers WHERE Seg_Responder = 1
UNION ALL
SELECT 'Seg_High_Web', AVG(Response * 1.0) FROM customers WHERE Seg_High_Web = 1
UNION ALL
SELECT 'Seg_Family', AVG(Response * 1.0) FROM customers WHERE Seg_Family = 1
UNION ALL
SELECT 'Seg_High_Spender', AVG(Response * 1.0) FROM customers WHERE Seg_High_Spender = 1;

-- Spend by demographics
CREATE VIEW v_spend_by_demo AS
SELECT Age_Band, Income_Band, Marital_Status, Country,
       AVG(Total_Spend) AS avg_spend,
       SUM(Total_Spend) AS sum_spend,
       COUNT(*) AS customers
FROM customers
GROUP BY Age_Band, Income_Band, Marital_Status, Country;

-- Channel usage by high-value customers
CREATE VIEW v_channels_high_value AS
SELECT
  AVG(NumWebPurchases) AS avg_web_purchases,
  AVG(NumStorePurchases) AS avg_store_purchases,
  AVG(NumCatalogPurchases) AS avg_catalog_purchases,
  AVG(NumDealsPurchases) AS avg_deals_purchases,
  AVG(NumWebVisitsMonth) AS avg_web_visits
FROM customers
WHERE Seg_High_Spender = 1;

-- Under-served segments (approximation: low spend < overall avg, high visits > overall avg, low response < overall avg)
CREATE VIEW v_underserved AS
SELECT Country, Age_Band, Income_Band,
       AVG(Total_Spend) AS avg_spend,
       AVG(NumWebVisitsMonth) AS avg_visits,
       AVG(Response * 1.0) AS response_rate
FROM customers
GROUP BY Country, Age_Band, Income_Band
HAVING AVG(Total_Spend) < (SELECT AVG(Total_Spend) FROM customers)
   AND AVG(NumWebVisitsMonth) > (SELECT AVG(NumWebVisitsMonth) FROM customers)
   AND AVG(Response * 1.0) < (SELECT AVG(Response * 1.0) FROM customers);