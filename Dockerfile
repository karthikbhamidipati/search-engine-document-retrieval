FROM python:3.8
WORKDIR /app
COPY *.txt ./
RUN pip install -r requirements.txt
COPY *.py  ./
COPY service/ service/
COPY utils/ utils/
COPY web/ web/
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["./main.py", "start_app"]