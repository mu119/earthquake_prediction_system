# 🌍 Earthquake & Tsunami Risk Prediction System

Welcome to the **Earthquake & Tsunami Risk Prediction System** — a Streamlit-based web app designed to assess the risk of earthquakes and tsunamis for any given location using historical global seismic data.

---

## 🚀 Features

* 🌍 **Location-based Earthquake Risk Prediction** (0-100%)
* 🌊 **Tsunami Risk Estimation**
* 📍 Accepts input as location name or latitude-longitude
* 📈 **EDA Dashboard** with:

  * Zone-wise Earthquake Frequency
  * Year-wise Trends
  * Magnitude Distribution
  * Top 10 Most Affected States
* 🗺️ **Interactive Global Earthquake Map**
* 📂 Works with large historical dataset (via Google Drive)

---

## 🛠️ Tech Stack

* **Frontend**: Streamlit
* **Backend**: Python
* **Geospatial Analysis**: `geopy`, `plotly`, `pandas`
* **Visualization**: Plotly, Streamlit charts

---

## 🔧 Setup Instructions

1. **Clone this Repository**

```bash
git clone https://github.com/mu119/earthquake_prediction_system.git
cd earthquake_prediction_system
```

2. **Create Virtual Environment & Install Requirements**

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

3. **Download Dataset (if not inclulded)**

   [https://drive.google.com/file/d/1oBP0v961OlczIYU5NwOF2L4Y3dE3Pjht/view?usp=sharing](https://drive.google.com/file/d/1oBP0v961OlczIYU5NwOF2L4Y3dE3Pjht/view?usp=sharing)

    `data/earthquake_data.csv`

4) **Run the App**

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
earthquake_prediction_system/
├── app.py                  # Streamlit app main file
├── data/
│   └── earthquake_data.csv # Earthquake dataset (download separately)
├── requirements.txt        # Python dependencies
├── README.md               # Project readme
└── ...
```

---

## 📸 Screenshot

> Add a screenshot here of your Streamlit app with map and charts.

---

## 📜 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📬 Contact

For any query, contact: [mu119](https://github.com/mu119)

---
