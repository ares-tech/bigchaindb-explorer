From python:3.6
ADD explorer/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
ADD explorer /explorer
ADD main.py /main.py
CMD ["python", "/main.py"]
