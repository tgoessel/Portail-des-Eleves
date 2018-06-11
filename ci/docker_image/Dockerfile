FROM python:alpine
RUN echo http://dl-cdn.alpinelinux.org/alpine/edge/testing >> /etc/apk/repositories && \
    apk add --no-cache moreutils git py-pip build-base libffi-dev postgresql-dev
RUN wget https://raw.githubusercontent.com/Mines-Paristech-Students/Portail-des-eleves/master/Pipfile -O /root/Pipfile && \
    wget https://raw.githubusercontent.com/Mines-Paristech-Students/Portail-des-eleves/master/Pipfile.lock -O /root/Pipfile.lock && \
    pip install pipenv
RUN cd /root/ && pipenv lock --requirements > requirements.txt && pip install -r requirements.txt
