# 📊 Marketing Campaign Analysis – Summary Report

## 1. Objective
The project aimed to analyze customer data from marketing campaigns to:
- Measure overall response and acceptance rates.
- Profile customer segments.
- Understand spending patterns by demographics.
- Identify under‑served groups for future targeting.

---

## 2. Data Preparation
- Raw customer CSV was cleaned and enriched with derived fields:
  - **Children** = Kidhome + Teenhome  
  - **Total_Spend** = Sum of all product category spends  
  - **Total_Purchases** = Sum of purchases across channels  
  - **Segmentation flags** (High Income, Young, Responder, High Web, Family, High Spender)  
- Demographic bands were created (Age_Band, Income_Band).  
- Final dataset stored in **SQLite (`marketing.db`)** with a `customers` table.

---

## 3. Analytical Views
We created reusable SQL views for key insights:

| View | Purpose |
|------|---------|
| **v_response_rate** | Overall campaign response rate |
| **v_campaign_rates** | Acceptance rates across campaigns 1–5 |
| **v_segment_response** | Response rates by customer segments |
| **v_spend_by_demo** | Average & total spend by demographics |
| **v_channels_high_value** | Channel usage patterns of high spenders |
| **v_underserved** | Segments with low spend, high visits, low response |

---

## 4. Key Insights
- **Overall response rate**: ~14.7% of customers responded.  
- **Campaign acceptance**: Campaign 1 had the highest acceptance (~13%), while others were much lower.  
- **Segment response**: High‑income and high‑spender groups did not necessarily show higher response rates, highlighting a gap.  
- **Spending patterns**: Older, high‑income customers contributed the largest share of spend.  
- **Channel usage**: High‑value customers favored **store purchases** and **web purchases**.  
- **Under‑served segments**: Certain age/income bands showed **high engagement (visits)** but **low spend and low response**, indicating untapped potential.

---

## 5. Business Understanding
- Campaigns need **better targeting**: acceptance rates are uneven.  
- **Young and family segments** show moderate engagement but low conversion.  
- **High spenders** are loyal but not always responsive to campaigns.  
- **Under‑served groups** represent opportunities for tailored offers.  

---

## 6. Next Steps
- Refine segmentation with behavioral + demographic features.  
- Personalize campaigns for under‑served but engaged groups.  
- Optimize channel strategy (web vs. store vs. catalog).  
- Monitor response rates over time to measure improvement.  