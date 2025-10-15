from Network_Security.pipeline.train_pipeline import Training_Pipeline
from Network_Security.logging.logger import logging
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.utils import load_object
from Network_Security.entity.estimator import Network_model
from Network_Security.constant import TARGET_COLUMN

import os
import sys 
import uvicorn
import pandas as pd
from fastapi import FastAPI,Header,HTTPException,Request,Depends,UploadFile,File
from fastapi.responses import JSONResponse,RedirectResponse
from fastapi.background import BackgroundTasks 
from fastapi.templating import Jinja2Templates 

app = FastAPI(title='Network Security',version='0.1.1')
templates = Jinja2Templates(directory= r'Network_Security\templates') 

@app.get('/',tags=['Start'])
async def index():
    return RedirectResponse(url='/docs',status_code=302)

AUTH_KEY = "Ahmed"
def verify_api_key(x_api_key: str = Header(...)):
    """
    API key validation function
    """
    if x_api_key != AUTH_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

@app.get('/train',tags=['Train The Model'])
async def train_route(backgroundtask:BackgroundTasks,api_key: str = Depends(verify_api_key)):
    try:
        logging.info('Training Process Starting')
        logging.info('Background Trainig Processing....')
        backgroundtask.add_task(Training_Pipeline().run_pipeline)
        logging.info('Background Trainig Completed....')
        return JSONResponse(content={"message": "Training started in background!"}, status_code=202)
    except Exception as e:
        logging.info(f"Training error{str(e)}")
        return JSONResponse(content=f'error: {str(e)}',status_code=220)

@app.post('/predict', tags=['Predict The Model'])
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        # Check file format
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail='Only CSV files are allowed')

        # Load file data
        df = pd.read_csv(file.file)
        if df.empty:
            raise HTTPException(status_code=400, detail='Uploaded CSV is empty')

        # x = df.drop(columns=[TARGET_COLUMN], axis=1)
        # y = df[TARGET_COLUMN].replace(-1, 0)
        # Load preprocessor and model
        preprocessor = load_object(r'final_model\preprocessor.pkl')
        model = load_object(r'final_model\model.pkl')

        # Create network model instance
        network_model = Network_model(
            transform_object=preprocessor,
            best_model_details=model
        )

        # Predict
        pred_df = network_model.predict(df)
        #pred_df = network_model.predict(x)

        df['prediction'] = pred_df
        df['prediction'] = df['prediction'].replace(-1, 0)

        # Save results
        os.makedirs('prediction', exist_ok=True)
        df.to_csv('prediction/output.csv', index=False)

        # Render table
        table_html = df.to_html(classes='table table-striped', index=False)
        return templates.TemplateResponse(
            'table.html',
            {'request': request, 'table': table_html}
        )

    except Exception as e:
        logging.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction process failed: {e}")



if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)






# uvicorn main:app --reload

# pipeline = Training_Pipeline()
# pipeline.run_pipeline()

#'C:\\Users\\tanvi\\Network_Security_'
# http://127.0.0.1:8000

