FROM python:3.9
WORKDIR /RiskVision
COPY . /RiskVision/
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python ./app.py