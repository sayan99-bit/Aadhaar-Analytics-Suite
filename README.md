Markdown

# 🛡️ Aadhaar-Analytics-Suite
**Unlocking Societal Trends in Biometric Data**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-FF4B4B?style=for-the-badge&logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-5.18-3F4F75?style=for-the-badge&logo=plotly)

A high-performance analytics platform designed to decode large-scale biometric datasets. This dashboard processes administrative logs to identify **migration corridors**, **demographic gaps**, and **service anomalies** without compromising user privacy.

Featuring a "Secure Data Gateway" UI, it offers real-time insights into enrolment saturation, mandatory biometric updates, and district-level risk assessment using statistical anomaly detection.

---

## 🚀 Key Features

### 🔐 Secure Data Gateway
* **Encrypted Environment Simulation:** A specialized "Lock Screen" UI that waits for a secure data handshake.
* **Auto-Schema Detection:** Intelligent file parsing that automatically identifies if an uploaded CSV is Enrolment, Demographic, or Biometric data based on column patterns.

### 📊 Smart Analytics Modules
* **Enrolment Trends:** Visualize age-bucketed saturation (0-5, 5-17, 18+) and child enrolment rates over time.
* **Demographic Insights:** Analyze population splits and update correction patterns to identify regional disparities.
* **Biometric Health:** Track mandatory update compliance (Age 5-17) and adult usage trends.

### ⚠️ Risk & Anomaly Detection
* **Automated Auditing:** Uses Z-Score statistical analysis to flag districts with suspicious spikes in biometric updates.
* **Risk Heatmaps:** Geospatial visualization of high-risk zones for immediate administrative intervention.

### 🎨 Modern UI/UX
* **Glassmorphism Design:** A premium, dark-mode interface with translucent cards and neon accents.
* **CSS Animations:** Smooth transitions, pulsing status indicators, and interactive elements.

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **Visualization:** [Plotly Express](https://plotly.com/python/) & Graph Objects
* **Data Processing:** [Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/)
* **Styling:** Custom CSS & HTML injection

---

## ⚙️ Installation & Setup

### Prerequisites
* Python 3.8 or higher

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/aadhaar-intel-suite.git](https://github.com/your-username/aadhaar-intel-suite.git)
cd aadhaar-intel-suite
2. Create a Virtual Environment (Optional but Recommended)
Bash

python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
3. Install Dependencies
Create a requirements.txt file with the contents below, then install:

Bash

pip install -r requirements.txt
requirements.txt content:

Plaintext

streamlit
pandas
numpy
plotly
4. Run the Application
Bash

streamlit run app.py
📖 How to Use
Option 1: The "Mock Data" Mode (Fastest Way to Test)
Launch the app.

In the Sidebar, check the box "Use Mock Data Generator".

The system will instantly generate synthetic records for Maharashtra, Karnataka, Delhi, UP, and Bihar.

Navigate through the tabs (Overview, Demographics, Biometrics) to see the charts in action.

Option 2: Upload Real Data
Ensure your CSV files have the correct column headers (case-insensitive):

Enrolment: date, state, district, age_0_5, age_5_17, age_18_greater

Demographic: date, state, district, demo_age_5_17, demo_age_17_

Biometric: date, state, district, bio_age_5_17, bio_age_17_

Drag and drop your CSV files into the "Data Ingestion" zone in the sidebar.

The system will auto-detect the file type and populate the dashboard.

📂 Project Structure
aadhaar-intel-suite/
│
├── app.py                # Main application logic
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── assets/               # Images and icons (optional)
🤝 Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

<div align="center"> <sub>Built with ❤️ for the 2026 Governance Hackathon</sub> </div>
