-- Overall response rate
SELECT AVG(Response) AS response_rate FROM customers;

-- Response rate by income band
SELECT Income_Band, AVG(Response) AS response_rate
FROM customers
GROUP BY Income_Band;

-- Spend patterns by demographics
SELECT Age_Band, Marital_Status, Country,
       AVG(MntWines) AS avg_wines,
       AVG(MntMeatProducts) AS avg_meat,
       AVG(Total_Spend) AS avg_total_spend
FROM customers
GROUP BY Age_Band, Marital_Status, Country;

-- Channel usage by high spenders
SELECT CASE WHEN Seg_High_Spender=1 THEN 'High Spender' ELSE 'Others' END AS segment,
       AVG(NumWebPurchases) AS avg_web,
       AVG(NumStorePurchases) AS avg_store,
       AVG(NumCatalogPurchases) AS avg_catalog,
       AVG(NumDealsPurchases) AS avg_deals
FROM customers
GROUP BY segment;
