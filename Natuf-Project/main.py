from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from enum import Enum
import pandas as pd

from factory import run_factory
from factory_history import run_factory_hist
from cafe import run_cafe
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

class TaskName(str, Enum):
    factory = "factory"
    factory_hist = "factory_hist"
    cafe = "cafe"

@app.get("/run/{task}")
def run_task(task: TaskName):
    try:
        if task == TaskName.factory:
            df = run_factory()
        elif task == TaskName.factory_hist:
            df = run_factory_hist()
        elif task == TaskName.cafe:
            df = run_cafe()
        else:
            raise HTTPException(status_code=400, detail="Invalid task name")

        return df

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

