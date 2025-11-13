# Project Requirements 

## 1. 🎯 Project Overview

[cite_start]**Title:** Optimization Final Course Project [cite: 1, 2]
[cite_start]**Goal:** To develop an interactive application that implements a **multi-commodity flow (MCF) optimization model**[cite: 7].
[cite_start]**Domain:** The application will model optimal ambulance routing for simultaneous emergency scenarios in a dense urban area[cite: 11, 12].
[cite_start]**Core Task:** The model must determine the optimal routes for ambulances departing from a single base to multiple incident locations, minimizing the total response cost (based on travel time and operational costs)[cite: 13, 14, 40].

---

## 2. 🛠️ Technical Stack

* [cite_start]**Network Data:** OSMnx (to obtain a real-world road network) [cite: 7, 42]
* [cite_start]**Optimization Model:** PuLP [cite: 42]
* [cite_start]**Interactive Application:** Streamlit [cite: 43]
* [cite_start]**Deployment:** streamlit.io [cite: 53]

---

## 3. 🧠 Problem Definition & Modeling Requirements

### Objective Function

[cite_start]The primary goal is to **minimize the total response cost**[cite: 40]. This cost must be a function of:
1.  [cite_start]**Travel Time:** Calculated based on route distance and allowed speeds[cite: 40].
2.  [cite_start]**Operational Costs:** Each ambulance type has a different, configurable operational cost (personnel, equipment, etc.)[cite: 20].

### Network & Nodes

* [cite_start]**Study Area:** A ~1 km² area (e.g., $1 \times 1$ km square or ~560m radius circle) [cite: 8] [cite_start]extracted from OpenStreetMap using **OSMnx**[cite: 7].
* [cite_start]**Origin (Source):** A single node representing the "ambulance base"[cite: 13].
* [cite_start]**Destinations (Sinks):** Multiple random points representing incident locations[cite: 13].

### Commodities (Flows)

[cite_start]The "multi-commodity" aspect refers to the three types of emergency severity[cite: 7, 12]:
1.  **Critical**
2.  **Medium**
3.  **Mild**

### Constraints & Parameters

* [cite_start]**Ambulance Assignment:** The model *must* assign a specific ambulance type based on the emergency's severity[cite: 21]:
    * **Critical Emergency** $\rightarrow$ Critical Care Ambulance
    * **Medium Emergency** $\rightarrow$ Intermediate Care Ambulance
    * **Mild Emergency** $\rightarrow$ Simple Transport Ambulance
* **Road Capacity (Speed):** Each street (edge) in the network has a limited capacity. [cite_start]This must be modeled as a **maximum speed**[cite: 22].
    * [cite_start]This speed ($C_i$) must be randomly generated for each street within a user-configurable range: $[C_{min}, C_{max}]$[cite: 22].
* [cite_start]**Flow Requirement (Speed):** Each *flow* (i.e., each ambulance route) has a **required speed** ($R_i$) to complete its journey[cite: 23].
    * [cite_start]This required speed ($R_i$) must also be randomly generated within a user-configurable range: $[R_{min}, R_{max}]$[cite: 23].
* [cite_start]**Configurability:** All parameters ($C_{min}$, $C_{max}$, $R_{min}$, $R_{max}$, and operational costs) must be configurable by the user in the application's UI[cite: 20, 23, 28].
* [cite_start]**Default Values:** All configurable parameters must have a default value set in the application[cite: 38].

---

## 4. 🖥️ Application (Streamlit) Requirements

[cite_start]The application must be interactive and include the following[cite: 24, 43]:

### Visualization

[cite_start]A map must be displayed showing[cite: 29]:
* [cite_start]The **origin** (ambulance base)[cite: 30].
* [cite_start]All **destination** (incident) nodes[cite: 32].
* [cite_start]The calculated **optimal route** for each flow (Mild, Medium, Critical)[cite: 34].
* [cite_start]The **required speed ($R_i$)** for each flow[cite: 36].
* [cite_start]The **maximum speed ($C_i$)** of each road segment used by a flow[cite: 37].

### Interactive Controls

* **Button: "Recalculate flows"**
    * [cite_start]This must re-run the optimization model with the current parameter settings[cite: 25].
* **Button: "Recalculate capacities"**
    * [cite_start]This must regenerate the random maximum speed values ($C_i$) for all road segments[cite: 26, 27].
* **Configuration Inputs:**
    * [cite_start]Controls (e.g., sliders, number inputs) to modify the ranges $[R_{min}, R_{max}]$ and $[C_{min}, C_{max}]$[cite: 28].
    * [cite_start]Controls to set the operational cost for each of the three ambulance types[cite: 20].

---

## 5.  deliverables

The final submission must include:

1.  [cite_start]**Python Script/Notebook:** The complete code implementing the model using OSMnx and PuLP[cite: 42].
2.  [cite_start]**Streamlit Application:** The interactive `.py` file for the Streamlit app[cite: 43].
3.  [cite_start]**Technical Report:** A document containing[cite: 44]:
    * [cite_start]Description of the chosen study area and data[cite: 45].
    * [cite_start]The complete **mathematical formulation** (variables, objective function, constraints)[cite: 47].
    * [cite_start]The solution procedure[cite: 48].
    * [cite_start]Results and analysis for at least **3 different scenarios**[cite: 50].
4.  [cite_start]**GitHub Repository:** A link to a repository with clean, commented code[cite: 51].
5.  [cite_start]**`requirements.txt`:** A file listing all project dependencies[cite: 52].
6.  [cite_start]**Deployed App Link:** A public URL of the working application (e.g., on streamlit.io)[cite: 53].

---

## 6. 📊 Evaluation Criteria

The project will be graded based on the following rubric:

| Dimension | Weight | Indicators |
| :--- | :--- | :--- |
| **Mathematical Modeling** | 30% | [cite_start]Correct definition of variables, constraints, and objective function. [cite: 55] |
| **Computational Implementation (PuLP)** | 25% | [cite_start]Correct solution of the optimization problem using PuLP. [cite: 55] |
| **Application Deployment (Streamlit)** | 20% | [cite_start]Usability and functionality of the deployed `streamlit.io` app. [cite: 55, 56] |
| **Documentation & Report** | 15% | [cite_start]Quality, clarity, and completeness of the technical report. [cite: 56] |
| **Individual Defense** | 10% | [cite_start]Ability to explain the work done. [cite: 56] |