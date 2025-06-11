# 🛒 Product Tagging CrewAI Agent

A simple AI-powered product description & tag generator using CrewAI, Gemini API, and SQLite memory.

---

## 📌 Problem Statement

> Build a simple CrewAI agent that takes a product (e.g., “Reusable Water Bottle”) and a short persona description (e.g., “eco-conscious Gen Z buyer”) and returns:
> 
> - A short product description tailored to that persona
> - Three product tags that match the tone (e.g., “vegan,” “trendy,” “reusable”)

---

## 🚀 Features

- ✅ CrewAI agent architecture with YAML-based configuration
- ✅ Input validation (length, completeness, quality)
- ✅ Memory (SQLite DB) to avoid redundant API calls
- ✅ Display of recent runs and most used tags
- ✅ Error handling with user-friendly messages
- ✅ CLI-based interface for easy interaction

---

## 🛠 Tech Stack

- Python 3.10+
- CrewAI
- Gemini 1.5 Flash (Google AI)
- SQLite (Memory DB)
- dotenv (for API key management)

---

## 🗂 Project Structure

```bash
product_agent/
│
├── src/
│   └── crewai_prod/
│       ├── config/
│       │   ├── agents.yaml
│       │   └── tasks.yaml
│       └── crew.py
│
├── memory_db.py
├── main.py
├── requirements.txt
└── README.md
```

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone <your-repo-link>
cd product_agent
```
### 2️⃣ Create Virtual Environment

```bash
python -m venv cenv
```

## 3️⃣ Activate Environment

### On Windows:
```bash
cenv\Scripts\activate
```

### On Mac/Linux:
```bash
source cenv/bin/activate
```

## 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 🔑 Environment Variables

Create a `.env` file in the project root with:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

✅ **Note:** Make sure you have access to Gemini 1.5 Flash via Google AI Studio or VertexAI.

## ▶️ Running the Agent

Run the main script:

```bash
python main.py
```

You will be prompted to enter:
- Product Name
- Persona Description

## Output

The CrewAI agent will generate:
- Product Description (2-3 sentences)
- 3 Product Tags suitable for marketing/e-commerce

## Results

Results are:
- Printed to the console
- Saved to `product_output.md`
- Stored in the local SQLite database (`memory.db`)

## 💾 Memory Behavior

- Previous results are saved in the SQLite DB
- If the same Product and Persona are input again, cached results are retrieved instead of calling Gemini API again
- Recent runs and popular tags are shown on startup

## 📽️ Demo Videos

- [Demo Video Working](https://drive.google.com/file/d/1VVXUs8hUrlrrTnnpK0vMBch1ZYpXibxp/view?usp=sharing)

- This video shows sample examples and all input validations.

- [Demo Video - Database Storage](https://drive.google.com/file/d/14Y3VeCKKIAKvxFE24GNMaQRAttYSZ07x/view?usp=sharing)

- This video shows the stored values in the database after each run.
- If same inputs are entered already stored output responses will be returned. (Caching)