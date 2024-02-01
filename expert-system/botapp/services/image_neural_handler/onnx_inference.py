import cv2
import numpy as np
import onnxruntime
import torch.onnx
from albumentations import Compose, Normalize, Resize
from albumentations.pytorch import ToTensorV2

from django.db.models.fields.files import ImageFieldFile


NEURAL_NET_NAMES = {
    "clock": "./demencia_test/services/image_neural_handler/clock.onnx",
    "figure": "./demencia_test/services/image_neural_handler/figure.onnx",
}


def get_val_augmentations(image_size):
    return Compose(
        [
            Resize(image_size, image_size),
            Normalize(
                mean=[0.487, 0.457, 0.395],
                std=[0.227, 0.222, 0.224],
            ),
            ToTensorV2(),
        ]
    )


def to_numpy(tensor):
    return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()


def get_image_score(neural_net_name, image_from_test: ImageFieldFile):
    # Этот параметр обозначает сколько картинок за раз запихиваем в модель
    """neural_net_name = clock или figure(для получения файла нейронки из словаря NEURAL_NET_NAMES)
    image_from_test - кртинка из теста на деменцию, загружаемая для оценки"""
    # batch_size = 1
    image_size = 256

    ort_session = onnxruntime.InferenceSession(NEURAL_NET_NAMES[neural_net_name])
    image = np.fromfile(image_from_test.file, dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # ниже вызывается модель
    transform = get_val_augmentations(image_size)
    augmented = transform(image=image)
    image = augmented["image"]
    # Если batch_size>1 то эта строчка не нужна. Тогда сделай список imgs в 40 строке
    image.unsqueeze_(0)

    ort_inputs = {ort_session.get_inputs()[0].name: to_numpy(image)}
    ort_outs = ort_session.run(None, ort_inputs)
    result = ort_outs[0]
    # [[ 0.5828074  0.8418093 -1.40597  ]]
    # получить класс
    class_id = torch.argmax(torch.softmax(torch.tensor(result), 1), 1)
    return class_id.item()
    # tensor([1])