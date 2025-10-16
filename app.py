from Network_Security.pipeline.train_pipeline import Training_Pipeline
from Network_Security.logging.logger import logging
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.utils import load_object
from Network_Security.entity.estimator import Network_model
from Network_Security.constant import TARGET_COLUMN
from Network_Security.pipeline.prediction_pipe import NetworkSecurity_Features

import os
import sys
import uvicorn
import pandas as pd
from io import StringIO
import io
from fastapi import FastAPI, Header, HTTPException, Request, Depends, UploadFile, File, Form
from fastapi.responses import JSONResponse, RedirectResponse, FileResponse
from fastapi.background import BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='Phishing URL Detection App', version='0.1.1')

# Static & templates
app.mount("/static", StaticFiles(directory= r"Network_Security\static"), name="static")
templates = Jinja2Templates(directory=r'Network_Security\templates')

# CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------- HOME ROUTE ----------------------
@app.get('/', tags=['Start'])
async def index():
    # Redirect to Swagger docs
    return RedirectResponse(url='/docs')

# ---------------------- API KEY VERIFICATION ----------------------
AUTH_KEY = "Ahmed"

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != AUTH_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

# ---------------------- TRAIN ROUTE ----------------------
@app.get('/train', tags=['Train The Model'])
async def train_route(
    request: Request,
    backgroundtask: BackgroundTasks,
    api_key: str = Depends(verify_api_key)
):
    try:
        logging.info('Training Process Starting')
        backgroundtask.add_task(Training_Pipeline().run_pipeline)
        logging.info('Background Training Started')
        # set status_code=202 to indicate accepted and background processing
        return templates.TemplateResponse(
            "train.html",
            {"request": request, "message": "Training started in background!"},
            status_code=202
        )
    except Exception as e:
        logging.error(f"Training error: {e}")
        # you can still return 500 or 400 for failure
        return templates.TemplateResponse(
            "train.html",
            {"request": request, "message": f"Training failed: {str(e)}"},
            status_code=500
        )
    

# CSV upload route
@app.post('/test', tags=['Predict The Model'])
async def predict_csv_route(request: Request, file: UploadFile = File(...)):
    try:
        # Validate file type
        if not file.filename.lower().endswith('.csv'):
            raise HTTPException(status_code=400, detail='Only CSV files are allowed')

        # Read CSV content safely
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode('utf-8')))

        if df.empty:
            raise HTTPException(status_code=400, detail='Uploaded CSV is empty')

        # Load preprocessor and model
        preprocessor = load_object(r'final_model\preprocessor.pkl')
        model = load_object(r'final_model\model.pkl')

        # Make predictions
        network_model = Network_model(transform_object=preprocessor, best_model_details=model)
        pred_df = network_model.predict(df)
        df['prediction'] = pd.Series(pred_df).replace(-1, 0)

        # Save prediction file
        os.makedirs('prediction', exist_ok=True)
        df.to_csv('prediction/output.csv', index=False)

        # Convert dataframe to HTML table
        table_html = df.to_html(classes='table table-striped table-bordered', index=False)

        # Render template
        return templates.TemplateResponse(
            'prediction.html',
            {
                'request': request,
                'table': table_html,
                'filename': file.filename
            }
        )

    except Exception as e:
        logging.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction process failed: {e}")
    
# Form prediction route
@app.post("/predict", tags=["Predict Form"])
def predict_form(
    request: Request,
    having_ip_address: int = Form(...),
    url_length: int = Form(...),
    shortining_service: int = Form(...),
    having_at_symbol: int = Form(...),
    double_slash_redirecting: int = Form(...),
    prefix_suffix: int = Form(...),
    having_sub_domain: int = Form(...),
    sslfinal_state: int = Form(...),
    domain_registration_length: int = Form(...),
    favicon: int = Form(...),
    port: int = Form(...),
    https_token: int = Form(...),
    request_url: int = Form(...),
    url_of_anchor: int = Form(...),
    links_in_tags: int = Form(...),
    sfh: int = Form(...),
    submitting_to_email: int = Form(...),
    abnormal_url: int = Form(...),
    redirect: int = Form(...),
    on_mouseover: int = Form(...),
    rightclick: int = Form(...),
    popupwindow: int = Form(...),
    iframe: int = Form(...),
    age_of_domain: int = Form(...),
    dnsrecord: int = Form(...),
    web_traffic: int = Form(...),
    page_rank: int = Form(...),
    google_index: int = Form(...),
    links_pointing_to_page: int = Form(...),
    statistical_report: int = Form(...)
):
    try:
        # Create feature object
        features = NetworkSecurity_Features(
            having_ip_address,
            url_length,
            shortining_service,
            having_at_symbol,
            double_slash_redirecting,
            prefix_suffix,
            having_sub_domain,
            sslfinal_state,
            domain_registration_length,
            favicon,
            port,
            https_token,
            request_url,
            url_of_anchor,
            links_in_tags,
            sfh,
            submitting_to_email,
            abnormal_url,
            redirect,
            on_mouseover,
            rightclick,
            popupwindow,
            iframe,
            age_of_domain,
            dnsrecord,
            web_traffic,
            page_rank,
            google_index,
            links_pointing_to_page,
            statistical_report
        )

        df = pd.DataFrame([features.dict_data()])

        preprocessor = load_object(r"final_model\preprocessor.pkl")
        model = load_object(r"final_model\model.pkl")

        network_model = Network_model(transform_object=preprocessor, best_model_details=model)
        prediction = network_model.predict(df)

        # Add styled output
        if prediction == 1:
            result_html = '<h3 style="color:red;">⚠️ Phishing Website Detected!</h3>'
        else:
            result_html = '<h3 style="color:green;">✅ Legitimate Website</h3>'

        return templates.TemplateResponse('predict.html', {'request': request, 'table': result_html})

    except Exception as e:
        logging.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction process failed: {e}")


# Download CSV route
@app.get("/download-predictions", tags=["Download Prediction"])
async def download_predictions():
    file_path = "prediction/output.csv"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Prediction file not found")
    return FileResponse(file_path, media_type="text/csv", filename="predictions.csv")



if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)







# uvicorn main:app --reload

# pipeline = Training_Pipeline()
# pipeline.run_pipeline()

#'C:\\Users\\tanvi\\Network_Security_'
# http://127.0.0.1:8000

