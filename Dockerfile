FROM tensorflow/tensorflow:latest-py3
RUN mkdir apps
COPY static/ apps/static
COPY predict_app.py apps/
COPY shell_scripts/ apps/shell_scripts/
COPY PALM_MODEL.h5 apps/
RUN pip install --upgrade pip
RUN pip install flask
RUN pip install Pillow
RUN pip install numpy
RUN pip install keras
RUN python --version
RUN python3 --version
RUN pip install opencv-python
RUN apt-get install -y libsm6 libxext6 libxrender-dev
RUN ls -lR /apps
WORKDIR /apps
ENTRYPOINT [ "python" ]
CMD ["predict_app.py"]
