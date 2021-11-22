FROM public.ecr.aws/z7p8p5g2/workshop-alpine:latest
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD [ "flask", "run", "--host=0.0.0.0" ]
