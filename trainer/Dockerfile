FROM tensorflow/tensorflow

RUN mkdir -p /tmp/numberClassifier
WORKDIR /tmp/numberClassifier

COPY . /tmp/numberClassifier
RUN mkdir output

CMD ["python", "train.py"]
