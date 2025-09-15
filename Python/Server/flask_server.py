import cv2
import torch
import numpy as np
from flask import Flask, request, jsonify, send_file
from torchvision.transforms import Compose, Resize, ToTensor, Normalize
import io
from PIL import Image

midas = torch.hub.load("intel-isl/MiDaS", "MiDaS_small")
midas.eval()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
midas.to(device)

midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
transform = midas_transforms.small_transform

app = Flask("Sensewave")

@app.route("/process", methods=["POST"])
def process_frame():
    file = request.files['frame']
    img = Image.open(file.stream).convert("RGB")
    img = np.array(img)

    input_batch = transform(img).to(device)

    with torch.no_grad():
        prediction = midas(input_batch)
        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=img.shape[:2],
            mode="bicubic",
            align_corners=False,
        ).squeeze()

    depth_map = prediction.cpu().numpy()

    depth_norm = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX)
    depth_color = cv2.applyColorMap(depth_norm.astype(np.uint8), cv2.COLORMAP_MAGMA)

    overlay = cv2.addWeighted(cv2.cvtColor(img, cv2.COLOR_RGB2BGR), 0.6, depth_color, 0.4, 0)

    _, buffer = cv2.imencode(".jpg", overlay)
    return send_file(
        io.BytesIO(buffer),
        mimetype='image/jpeg'
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
