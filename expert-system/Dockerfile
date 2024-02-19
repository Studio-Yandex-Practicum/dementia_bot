FROM python:3.10-slim as builder

RUN apt-get update && apt-get install -y \
    python3-dev \
    curl

WORKDIR /app
COPY requirements.txt /app/
RUN pip install torch==1.11.0+cpu torchvision==0.12.0+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html
RUN pip install ultralytics==8.1.9 --no-deps

RUN pip install -r requirements.txt

RUN apt install -y libgl1-mesa-glx \
    libgtk2.0-dev

COPY . .

RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["sh", "docker-entrypoint.sh"]