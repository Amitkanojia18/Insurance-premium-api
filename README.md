# Insurance Premium Category Predictor

A machine learning-powered API that predicts a user's insurance premium category (Low / Medium / High) based on demographic, lifestyle, and financial inputs. Built with **FastAPI** for the backend, **Streamlit** for the frontend, and containerized with **Docker** for deployment.

## Overview

Insurance premiums depend on a mix of factors that aren't always obvious from raw data alone — age, income, and smoking status matter, but so do derived signals like BMI, lifestyle risk, and the economic tier of a user's city. This project wraps a trained classification model behind a clean REST API, handling feature engineering and input validation automatically, so a frontend (or any client) only needs to send raw user data.

## Architecture

```
insurance-premium-api/
│
├── app.py                      # FastAPI entry point — routes & request handling
├── config/
│   └── city_tier.py             # Static city-to-tier mapping (tier 1 / tier 2 / tier 3)
├── model/
│   ├── model.pkl                 # Trained classification model
│   └── predict.py                # Model loading and prediction logic
├── schema/
│   ├── user_input.py             # Pydantic input schema + computed features
│   └── prediction_response.py    # Pydantic response schema
├── Dockerfile                    # Container build definition
├── requirements.txt              # Python dependencies
└── .gitignore
```

## How It Works

1. **Client sends raw user data** — age, weight, height, income, smoking status, city, occupation.
2. **Pydantic validates the input** and automatically computes derived features:
   - `bmi` — calculated from height and weight
   - `age_group` — young / adult / middle_aged / senior
   - `lifestyle_risk` — low / medium / high, based on BMI and smoking status
   - `city_tier` — 1, 2, or 3, based on a predefined city list
3. **The trained model predicts** a premium category along with class probabilities and a confidence score.
4. **The API returns a structured JSON response** with the prediction.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI |
| Data validation | Pydantic |
| ML model | scikit-learn (pickled) |
| Frontend | Streamlit |
| Containerization | Docker |

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
git clone https://github.com/Amitkanojia18/Insurance-premium-api.git
cd Insurance-premium-api
pip install -r requirements.txt
```

### Running Locally

```bash
uvicorn app:app --reload
```

The API will be live at `http://127.0.0.1:8000`
Interactive API docs (Swagger UI): `http://127.0.0.1:8000/docs`

### Running with Docker

```bash
docker build -t insurance-premium-api .
docker run -p 8000:8000 insurance-premium-api
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message / health message |
| GET | `/health` | Service health check, model load status, and model version |
| POST | `/predict` | Predicts insurance premium category from user input |

### Example Request — `POST /predict`

```json
{
  "age": 30,
  "weight": 65,
  "height": 1.7,
  "income_lpa": 10,
  "smoker": false,
  "city": "Mumbai",
  "occupation": "private_job"
}
```

### Example Response

```json
{
  "predicted_category": "Medium",
  "confidence": 0.8421,
  "class_probabilities": {
    "Low": 0.11,
    "Medium": 0.84,
    "High": 0.05
  }
}
```

## Input Validation

All inputs are validated via Pydantic before reaching the model:

- `age`: 1–119
- `height`: 0–2.5 meters
- `weight`, `income_lpa`: must be greater than 0
- `occupation`: restricted to a fixed set of valid categories (`related`, `freelancer`, `student`, `government_job`, `business_owner`, `unemployed`, `private_job`)
- `city`: normalized (trimmed, title-cased) before tier lookup

Invalid input returns a `422 Unprocessable Entity` with details on which field failed and why.

## License

This project is for learning and portfolio purposes.
