FROM python:3.7
COPY . /code
WORKDIR /code
RUN mkdir captured_hars
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["HAR-Capture.py"]