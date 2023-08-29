import gzip
import logging
import pickle
from typing import List

import pandas as pd
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import lib.constants as constants

app = FastAPI()


templates = Jinja2Templates(directory="templates")


# Getting the model.
with gzip.open("model_pickle2.gz", "rb") as f:
    model = pickle.load(f)

with gzip.open("encoder_pickle2.gz", "rb") as f:
    # Technically this a encoder/decoder since its a bidict
    encoder = pickle.load(f)


def _get_actual_diagnostic_codes() -> List[str]:
    result = []
    for code in constants.DIAGNOSTIC_CODES:
        if code in encoder:
            result.append(code)
    return result


def return_med_prediction(diagnosis_list: List[str]) -> str:
    """Gets a prediction from the machine learning model.

    Args:
        diagnosis_list: A list of diagnosis codes.

    Returns:
        The code for the predicted medication.
    """
    max_length = 25
    if len(diagnosis_list) > max_length:
        raise ValueError(f"only {max_length} conditions are allowed")
    diagnosis_list_final = [0 for _ in range(max_length)]
    for i, diagnosis_code in enumerate(diagnosis_list):
        # Diagnosis needs to be encoded as int since model can only interpret numbers.
        diagnosis_list_final[i] = encoder[diagnosis_code]
    diagnosis_list_final.append(1)
    logging.info(diagnosis_list_final)
    return encoder.inverse[
        model.predict(pd.DataFrame(
            [diagnosis_list_final], columns=constants.COLUMNS))[0]
    ]


@app.get("/", response_class=HTMLResponse)
async def get_main_page(request: Request):
    return templates.TemplateResponse(
        "main.html", {"request": request,
                      "diag_codes": _get_actual_diagnostic_codes()}
    )


@app.post("/", response_class=HTMLResponse)
async def post_main_page(request: Request):
    form = await request.form()
    if form.get("num_codes") is None:
        return templates.TemplateResponse(
            "main.html", {"request": request,
                          "diag_codes": _get_actual_diagnostic_codes()}
        )
    num_codes = form.get("num_codes")
    submitted_diag_codes = []
    for i in range(0, int(num_codes)):
        submitted_diag_codes.append(form.get("input-box-" + str(i)))
    logging.info(num_codes)
    logging.info(submitted_diag_codes)
    pred = return_med_prediction(submitted_diag_codes)
    logging.info(pred)
    return templates.TemplateResponse(
        "results.html", {"request": request, "prediction": pred}
    )


if __name__ == "__main__":
    app.run(debug=True)
