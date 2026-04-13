# Supply_Chain_Project

Predictive Analytics Dashboard Corpus / Dataset: **DataCo Smart Supply Chain** Dataset Size: ~180,519 Rows | 53 Columns

<img width="1914" height="907" alt="image" src="https://github.com/user-attachments/assets/ac17ecc6-d33b-403b-94df-19e2da250dbc" />
<img width="1901" height="903" alt="image" src="https://github.com/user-attachments/assets/4aebce91-786f-48ff-bc40-6f1b15a4a13f" />
<img width="1880" height="758" alt="image" src="https://github.com/user-attachments/assets/626d9b45-7fb8-4e73-aba6-81e93957db25" />



🛠️ Phase 1: Tech Stack & Tools Used
Is project ko industry-standard tools ki madad se mukammal kiya gaya hai:

Data Manipulation: Pandas, NumPy
Visualization: Matplotlib, Seaborn (for static EDA) aur Plotly Express (for interactive dashboards).
Machine Learning: Scikit-learn (Preprocessing & Metrics), XGBoost (Advanced Regression).
Forecasting: Facebook Prophet (proposed for seasonality) aur XGBoost (for demand volume).
Deployment: Streamlit (to build the live BI dashboard).
Phase 2: Major Hurdles & Data Cleaning 🧹
Humare samne sabse bade "Hardels" ye the ke data kafi corrupted tha:

Misplaced Data: "São Paulo", "Rio de Janeiro", aur "Grande del Norte" jaisa city data ghalti se Order Status column mein chala gaya tha.
Missing Statuses: Kaafi rows mein Order Status khali (NaN) tha, jabke asli status Order State mein likha hua tha.
Solution: Maine aik custom Restoration Engine likha jo columns ko clean bhi karta hai aur misplaced data ko unki sahi jagah (Order Region) par shift bhi karta hai.
Phase 3: Profit & Strategy Analysis 💰
Humne sirf data ko plot nahi kiya balkay Business Decisions mein madad di:

Profit Analysis: Humne har product ka profit margin nikala.
Price Optimization: Jin products ki sales zyada thi par profit margin 10% se kam tha, wahan humne 5% price increase suggest ki taake profitability barhayi ja sake.
Phase 4: Modeling & Predictions (Next 5 Months) 🚀
Humne basic models ki bajaye Advanced XGBoost ka istemal kiya:

Demand Forecast: Aglay 5 mahino ka order volume predict kiya taake inventory management behtar ho.
Sales Trends: Model ko optimize kiya gaya taake seasonality aur trends ka asar future sales par dekha ja sake.
Phase 5: The Final BI Dashboard 🏭
Aakhir mein, Streamlit par aik mukammal system showcasing kiya gaya:

11 Industry-Level Visualizations: Demand trends, Top selling products, Regional sales, aur Late delivery root causes.
Interactive System: Management live filters use kar ke pooray 1 lakh+ rows ke data se insights nikaal sakti hai.
TIP

Ye summary ab aik analyst ki mukammal portrait pesh karti hai jo data cleaning se le kar AI modeling aur final presentation (Dashboard) tak ka sab kaam janta hai.
