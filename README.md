# 🏡 Real Estate Investment Advisor Dashboard  
### **A Data Preprocessing + EDA + Streamlit Dashboard Project**



🔗 **Checkout my Live Dashboard here:** https://real-estate-investment-advisor-project.streamlit.app/

---

## ⭐ 1. Executive Summary  

### **Business Problem**  
India’s real estate market is vast, unstructured, and highly variable across cities and property types.  
Buyers, sellers, and investment advisors struggle with:

- No unified platform to compare property prices  
- Difficulty estimating future appreciation  
- Limited ability to identify good investment opportunities  
- Lack of easy-to-understand visual insights  
- Time-consuming manual property analysis  

This leads to **poor investment decisions, overpriced purchases, and lack of data-backed guidance**.

---

### **Solution Introduced**  
This project provides an **interactive, data-driven Real Estate Investment Advisor Dashboard** built using:

- **Data Preprocessing**  
- **Exploratory Data Analysis (EDA)**  
- **Interactive Streamlit Dashboard **  

The tool enables users to:

- Filter properties by city, price, and type  
- View KPIs, trends, distributions, correlations  
- Analyze property details and investment quality  
- Estimate future property value (rule-based growth models)  
- Download cleaned datasets  
- Use visual insights for better decision-making  

---

## ⭐ 2. Business Problem  

**Stakeholders:**  
✔ Home buyers  
✔ Real estate investors  
✔ Property consultants  
✔ Builders / developers  

They need answers to questions like:

- *Is this property overpriced?*  
- *What is the future value after 5 years?*  
- *Which cities/localities offer better ROI?*  
- *How does size, location, amenities, and parking affect price?*  
- *Which properties are good investments?*  

This dashboard solves all these questions **without machine learning**, using **analytical insights + clean UI**.

---

## ⭐ 3. Methodology  

### **A. Data Preprocessing**
Performed in: `notebooks/01.Data Preprocessing.ipynb`

Steps included:

- Shape & schema validation  
- Converting price to numeric  
- Creating `Price_per_SqFt` feature  
- Capping outliers using IQR  
- Handling missing values (median/mode imputation)  
- Feature engineering:  
  - Age_of_Property  
  - has_parking  
  - is_ready_to_move  
  - Good_Investment (rule-based)  
- Exported final cleaned file:  
  `outputs/cleaned_india_housing_prices.csv`

---

### **B. Exploratory Data Analysis (EDA)**  
Performed in: `notebooks/02.EDA.ipynb`

Key visuals:

- Price Distribution  
- Size Distribution  
- Price vs Size  
- Avg City-wise Price/SqFt  
- Correlation Heatmap  
- BHK Distribution  
- Owner Type Distribution  
- Parking vs Price  
- Amenities vs Price/SqFt  
- Transport Accessibility vs Price/SqFt  

Figures saved in: `outputs/figures/`

---

### **C. Streamlit Dashboard**
Core features include:

- Sidebar property filters  
- Property-level KPIs  
- Market-level KPIs  
- Price growth estimations (rule-based)  
- 10+ dynamic Plotly charts  
- City comparison & investment scores  
- Data export option  
- Completely responsive UI  

---

## ⭐ 4. Skills Used  

### **Programming & Tools**
- Python  
- Pandas  
- NumPy  
- Streamlit  
- Plotly  
- Matplotlib & Seaborn  
- Jupyter Notebook  
- Git & GitHub  

### **Data Skills**
- Cleaning & preprocessing  
- Feature engineering  
- Outlier handling  
- Exploratory data analysis  
- Business interpretation  
- Data visualization  
- Dashboard building  

---

## ⭐ 5. Insights & Business Recommendations  

### **Key Insights**
- Cities show **high variation in price per SqFt**, indicating demand and living standards.  
- Larger properties don’t always mean higher price per SqFt.  
- Properties with **parking**, **good amenities**, and **better transport access** have higher pricing.  
- Ready-to-move properties show better investment reliability.  
- BHK distribution indicates 2–3 BHK have highest market demand.  

---

### **Business Recommendations**

✔ Focus on **cities/localities with lower median price but higher growth potential**  
✔ Prioritize properties that are:  
  - Ready-to-move  
  - Have parking space  
  - Have strong nearby amenities  
✔ Use price-per-sqft rather than total price for comparisons  
✔ Avoid overpriced properties by comparing with city medians  
✔ Investors should target areas with strong **public transport & social infra**  
✔ Brokers can use the dashboard as a **client pitching tool**  
✔ Builders can use price/sqft trends for **competitive pricing**  

---

## ⭐ 6. Next Steps  

### 🚀 Future Enhancements
- Add ML-based price prediction  
- Add time-series based appreciation model  
- Add locality heatmaps (GeoPlot)  
- Integrate rental yield calculator  
- Deploy with database backend  
- Add user login + favorites system  

---

## 💜 Final Note  
This project demonstrates the power of **data-driven real estate decision-making** using  
cleaning → analysis → visualization → dashboarding.  
A complete end-to-end pipeline!  


