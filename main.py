import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.config import Configuration
from app.forms.classification_form import ClassificationForm
from app.ml.classification_utils import classify_image
from app.utils import list_images
from app.histogram_utils import calculate_histogram
import io
import matplotlib.pyplot as plt


app = FastAPI()
config = Configuration()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/info")
def info() -> dict[str, list[str]]:
    """Returns a dictionary with the list of models and
    the list of available image files."""
    list_of_images = list_images()
    list_of_models = Configuration.models
    data = {"models": list_of_models, "images": list_of_images}
    return data


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """The home page of the service."""
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/classifications")
def create_classify(request: Request):
    """Render the classification selection page with available images and models."""
    return templates.TemplateResponse(
        "classification_select.html",
        {"request": request, "images": list_images(), "models": Configuration.models},
    )


@app.post("/classifications")
async def request_classification(request: Request):
    """Handle the classification request and render the classification output page."""
    form = ClassificationForm(request)
    await form.load_data()
    image_id = form.image_id
    model_id = form.model_id
    classification_scores = classify_image(model_id=model_id, img_id=image_id)
    return templates.TemplateResponse(
        "classification_output.html",
        {
            "request": request,
            "image_id": image_id,
            "classification_scores": json.dumps(classification_scores),
        },
    )

@app.get("/classifications/dowlonad/results")
async def download_classification_results(classification_scores: str):
    """Endpoint to download classification results as a JSON file."""
    results = json.loads(classification_scores)
    return StreamingResponse(
        io.BytesIO(json.dumps(results).encode()),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=classification_results.json"}
    )


@app.get("/classifications/download/plot")
async def download_classification_plot(classification_scores: str):
    """Download the classification plot as a PNG image."""
    # Parse the classification scores
    results = json.loads(classification_scores)
    labels = [item[0] for item in results]
    values = [item[1] for item in results]

    colors = [(0.102, 0.290, 0.016, 0.8),
              (0.459, 0.0, 0.078, 0.8),
              (0.475, 0.341, 0.012, 0.8),
              (0.024, 0.129, 0.424, 0.8),
              (0.247, 0.012, 0.333, 0.8)]
    plt.figure(figsize=(10, 6))
    plt.barh(labels, values, color=colors[:len(labels)])
    plt.gca().invert_yaxis()
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Confidence (%)')
    plt.title('Output scores')
    plt.grid(True, axis='x')
    plt.tight_layout()

    # create a buffer to store image data
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type="image/png",
        headers={"Content-Disposition": "attachment; filename=classification_plot.png"})


@app.get("/histograms")
def create_histogram(request: Request):
    """Render the histogram selection page with available images."""
    return templates.TemplateResponse(
        "histogram_select.html",
        {"request": request, "images": list_images()},
    )

@app.post("/histograms")
async def request_histogram(request: Request):
    """Handle the histogram request and render the histogram output page."""
    form = ClassificationForm(request)
    await form.load_data()
    image_id = form.image_id
    histogram_values = calculate_histogram(image_id)
    return templates.TemplateResponse(
        "histogram_output.html",
        {"request": request, "image_id": image_id, "histogram_values": histogram_values},
    )