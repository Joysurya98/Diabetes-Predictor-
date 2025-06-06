import pandas as pd
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from app.JWTUtilities import decode_access_token
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime
import io
from typing import List
from fastapi import Form
import os
import pickle

# Get absolute path to the model file
model_path = os.path.join(os.path.dirname(__file__), "D:\python_practice\DiabetesPredictor\diabetes_model.pkl")

# Load the model
with open(model_path, "rb") as f:
    model = pickle.load(f)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# ✅ Get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def run_model(data: pd.DataFrame) -> list:
    try:
        predictions = model.predict(data)
        results = ["Diabetic" if p == 1 else "Not Diabetic" for p in predictions]
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")
    
# ✅ Route: Upload CSV and get prediction

@router.post("/predict")
async def predict(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    file: UploadFile = File(...)  # 👈 file must come LAST
):
    # ✅ Decode user from token
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_id = int(payload.get("sub"))
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ Read uploaded CSV file
    contents = await file.read()
    try:
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid CSV format")
    REQUIRED_COLUMNS = ["Pregnancies", "Glucose", "BloodPressure"]

# ✅ Check required columns
    for col in REQUIRED_COLUMNS:
     if col not in df.columns:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required column: {col}"
        )
    # ✅ Run batch prediction
    results = run_model(df)

# ✅ Log the batch as one entry
    log = models.PredictionLog(
    user_id=user.id,
    input_data=df.to_json(),
    prediction_result=", ".join(results),  # log all predictions
    timestamp=datetime.utcnow()
)
    db.add(log)
    db.commit()
    db.refresh(log)

# ✅ Prepare response
    return {
    "user": user.name,
    "predictions": [
        {"input": row, "result": results[i]}
        for i, row in enumerate(df.to_dict(orient="records"))
    ],
    "logged_at": log.timestamp
}
    

@router.get("/history")
def get_prediction_history(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    # ✅ Decode token and get user
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_id = int(payload.get("sub"))
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ Get all predictions for this user
    predictions = db.query(models.PredictionLog)\
        .filter(models.PredictionLog.user_id == user.id)\
        .order_by(models.PredictionLog.timestamp.desc())\
        .all()
    
    # ✅ Format the response
    history = []
    for log in predictions:
        history.append({
            "input_data": log.input_data,
            "prediction": log.prediction_result,
            "timestamp": log.timestamp
        })
    
    return {"user": user.name, "history": history}

@router.delete("/clear")
def clear_prediction_history(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    # ✅ Decode token
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = int(payload.get("sub"))
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ Delete user's predictions
    deleted = db.query(models.PredictionLog)\
        .filter(models.PredictionLog.user_id == user.id)\
        .delete()
    
    db.commit()

    return {"message": f"{deleted} prediction(s) deleted successfully"}