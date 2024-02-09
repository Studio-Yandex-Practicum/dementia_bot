from datetime import datetime
from ultralytics import YOLO


def image_detected_8(img):
    """Вопрос 8. Распознавание графического ответа и его оценка."""
    model = YOLO("botapp/yolo/last.pt")
    result = model.predict(img, conf=0.84)[0].boxes
    if len(result) == 0:
        return 0
    else:
        model = YOLO("botapp/yolo/lastv3.pt")
        results = model.predict(img, conf=0.5)
        result = results[0]
        boxs = result.boxes
        if len(boxs) > 1:
            return 0
        for box in boxs:
            class_id = result.names[box.cls[0].item()]
            conf = round(box.conf[0].item(), 2)
            if class_id == "bad_clock" and conf >= 0.55:
                return 1
            elif class_id == "clock_good" and conf <= 0.86:
                return 1
            elif class_id == "clock_good" and conf > 0.86:
                return 2
            else:
                return 0

def now_date():
    """Текущая дата-время."""
    now = datetime.now()
    return now.strftime("%Y-%m-%d_%H-%M-%S")

def image_detected_7(img):
    """Вопрос 7. Распознавание графического ответа и его оценка."""
    model = YOLO("botapp/yolo/copy_test_7.pt")
    results = model.predict(img, conf=0.5)
    result = results[0]
    boxs = result.boxes
    for box in boxs:
            class_id = result.names[box.cls[0].item()]
            conf = round(box.conf[0].item(), 2)
            if class_id == "test_good" and conf == 1:
               return 2
            elif class_id == "test_bad" and conf > 0.8:
               return 1
    return 0
