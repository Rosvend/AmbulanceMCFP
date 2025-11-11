# Multi-Commodity Flow Optimization for Emergency Ambulance Routing

This project develops an **interactive application** that implements a **multi-commodity flow routing model** over a **real urban road network** obtained using **OSMnx**.
The study area corresponds approximately to a **1 km² urban region** (either a 1×1 km square or a circle of ≈560 meters radius), centered on a geographic point defined by each student.

---

## Context

In **prehospital emergency care systems**, every minute of response time can determine patient survival.
In dense urban areas, **traffic congestion**, **limited ambulance availability**, and **operational costs** represent major logistical challenges.

Traditional ambulance dispatch systems often rely on **manual or heuristic assignments**, lacking an optimization framework that simultaneously considers **travel time**, **clinical priority**, and **operational cost**.
This leads to **inefficient resource use**, **long response times**, and **excessive fuel and personnel costs**.

The challenge of this project is to **design a mathematical optimization model** that, using a **real road network extracted via OSMnx**, determines optimal routing for different emergency severities.
The model must assign each emergency to an appropriate ambulance type while considering the following conditions:

* Each urgency level (mild, moderate, critical) has a **different priority**.
* Each ambulance type has a **different operational cost**, which depends on medical staff, equipment, and supplies.

  * **Mild:** Basic transport ambulance
  * **Moderate:** Intermediate care ambulance
  * **Critical:** Advanced life support ambulance
* Roads have **limited capacities** that restrict simultaneous traffic flow.

  * Each road is assigned a **random speed capacity** between `[C_min, C_max]`, configurable by the user.
* Each flow (ambulance route) requires a **desired speed** randomly generated between `[R_min, R_max]`, also configurable in the user interface.

---

## Features

The interactive **Streamlit application** includes the following features:

* **“Recalculate Flows”** button:
  Runs the optimization model again with the current configuration.
* **“Recalculate Capacities”** button:
  Regenerates random capacity values for each road.
* **Configurable Parameters:**
  User can modify `R_min`, `R_max`, `C_min`, and `C_max`.
* **Visual Map Output:**
  Displays calculated routes for each flow, showing:

  * Origin (ambulance base)
  * Destinations (emergency points)
  * Routes for each ambulance type
  * Required speed per flow
  * Road capacity (maximum speed) per segment
* **Default Values:**
  Every configurable parameter must have a default setting.
* **Additional Controls (Optional):**
  Any extra features or UI controls considered useful by the student.

---

## Tech stack

* **Python 3.10+**
* **OSMnx** – Road network extraction and visualization
* **PuLP** – Linear optimization modeling
* **Streamlit** – Interactive web application framework
* **NetworkX** – Graph and routing algorithms
* **GeoPandas / Shapely** – Spatial data processing

---

## Repository Structure

```
.
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── data/                       # Cached network data (auto-generated)
├── docs/
│ └── informe_tecnico.pdf # Technical report
├── src/
│   ├── optimization/
│   │   ├── data_interface.py  # Data structure for optimization
│   │   └── model.py           # PuLP optimization model
│   └── visualization/
│       ├── __init__.py
│       ├── network.py         # NetworkManager for OSMnx
│       └── map_display.py     # MapVisualizer for Folium
└── tests/
    └── test_network.py        # Network module tests
```

---

## How to Run the Project

### Prerequisites
- Python 3.10+
- pip package manager
- Internet connection (for downloading OSM data)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/rosvend/AmbulanceMCFP.git
   cd AmbulanceMCFP
   ```

2. **Create virtual environment (recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Authors

Roy Sandoval — Network Routing & Streamlit Implementation

Alexandra Vasco — Mathematical Model & Documentation

