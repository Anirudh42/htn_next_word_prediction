FROM 
COPY . /app
WORKDIR 
RUN 
ENTRYPOINT ["python"]
CMD ["app.py"]
EXPOSE 5000