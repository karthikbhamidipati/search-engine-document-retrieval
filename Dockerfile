FROM python:3.8
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY main.py  ./
COPY service/ service/
COPY utils/ utils/
COPY web/ web/
COPY data/ data/
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["./main.py", "start_app"]