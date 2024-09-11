FROM nginx:latest
RUN apt-get update && apt-get install -y git
RUN rm -rf /usr/share/nginx/html/*
RUN git clone https://github.com/codewithsadee/grilli.git /usr/share/nginx/html
EXPOSE 80
