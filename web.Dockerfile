FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN curl -fsSL https://deb.nodesource.com/setup_20.x -o nodesource_setup.sh
RUN bash nodesource_setup.sh
RUN apt-get install -y nodejs

WORKDIR /app/SSSB/frontend
COPY . /app

RUN npm install
RUN npm run build

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/SSSB

#CMD ["sh", "-c", "python ../check_sssb.py --endless --headless --get_url & python ../check_sssb.py --endless --headless --check_url"]
#CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8082 & python ../check_sssb.py --endless --headless --get_url & python ../check_sssb.py --endless --headless --check_url & python ../check_sssb.py --endless --headless --check_filter"]
