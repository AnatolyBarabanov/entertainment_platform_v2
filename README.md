# 🎬 Entertainment & Media Recommendation Platform

**Course:** CMPSC 462 – Data Structures (Fall 2025)  
**Authors:** Anatoly Barabanov & Michael Calle  
**Instructor:** Vinayak Elangovan  

---

## 📌 Project Overview

The **Entertainment & Media Recommendation Platform** is an interactive system designed to help users discover movies and music that best match their preferences. Instead of relying on broad search results, the platform uses structured data and similarity-based relationships to generate meaningful recommendations.

Users can select genres, artists, directors, actors, and optional seed items to receive ranked recommendations along with visual explanations of how media items are related.

---

## 🧠 Key Concepts & Data Structures

This project uses a **hybrid data structure approach**:

### 🌳 Hierarchical Tree
- Organizes media by **type → genre → creator → item**
- Enables fast, intuitive browsing and filtering
- Displays a structured view of the media library

### 🔗 Weighted Graph
- Each media item is a **node**
- Edges represent similarity based on:
  - Genre
  - Artist / Director
  - Actors (movies)
  - Album (music)
  - Feature similarity
- Edge weights determine recommendation strength

This combination ensures both **efficient organization** and **intelligent recommendations**.

---

## ⚙️ Design & Implementation

- Implemented in **Python**
- Backend logic handles:
  - Tree construction
  - Graph similarity scoring
  - Recommendation ranking and grouping
- Frontend built using **Streamlit**
- Interactive features include:
  - Sidebar preference selection
  - Ranked recommendation lists
  - Interactive graph visualization
  - Tree-based library view

Recommendations are **not random** — they are driven by user preferences and graph-based similarity traversal.

---

## 📊 Results & Performance

- The system consistently produces relevant recommendations
- Items matching multiple preferences are prioritized
- Graph visualization helps explain why items are recommended
- Tree structure provides clarity and organization
- Performance scales well for the provided dataset

Overall, combining a tree for structure and a graph for similarity proved effective and interpretable.

---

## 🧪 Testing & Validation

- Manual testing across multiple preference combinations
- Verified recommendation accuracy and consistency
- Ensured correct graph connections and tree hierarchy
- Validated UI responsiveness and visualization updates

---

## 👥 Team Contributions

### **Anatoly Barabanov**
- Backend architecture and algorithms
- Implemented tree and graph data structures
- Developed recommendation logic and similarity scoring
- Managed data loading and traversal optimization

### **Michael Calle**
- User interface and Streamlit integration
- Designed layout and interactive controls
- Connected backend logic to frontend displays
- Managed visual presentation of results

### **Both Members**
- Testing, debugging, and validation
- Documentation and report writing
- Planning future enhancements

---

## 🚀 How to Run the Project

### 1️⃣ Clone or Download
```bash
git clone https://github.com/AnatolyBarabanov/entertainment_platform_v2.git
cd entertainment_platform_v2
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Application
```bash
streamlit run app/ui/streamlit_app.py
```
