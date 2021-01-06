FROM python:3.8.6-slim
WORKDIR /Api
RUN pip install torch==1.7.0+cpu torchvision==0.8.1+cpu torchaudio==0.7.0 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install transformers==3.3.0 \
                nltk==3.5 \
                fastapi==0.61.2 \
                uvicorn==0.12.3 \
                pyYAML==5.3.1
RUN python3 -m nltk.downloader popular
ADD . .
# RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]