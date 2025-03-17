FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN echo "deb http://deb.debian.org/debian buster main" > /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian buster-updates main" >> /etc/apt/sources.list && \
    echo "deb http://security.debian.org/debian-security buster/updates main" >> /etc/apt/sources.list

RUN apt-get update && apt-get install -y cron
RUN echo "0 2 * * * rm -rf /tmp/* >> /var/log/cron.log 2>&1" > /etc/cron.d/cron-rmtmp
RUN chmod 0644 /etc/cron.d/cron-rmtmp
RUN crontab /etc/cron.d/cron-rmtmp
RUN touch /var/log/cron.log
CMD cron && tail -f /var/log/cron.log

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libnss3 \
    libxss1 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libasound2 \
    software-properties-common \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    libatk-bridge2.0-0 \
    libgbm1 \
    libxkbcommon0 \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/127.0.6533.72/linux64/chrome-headless-shell-linux64.zip \
    && unzip chrome-headless-shell-linux64.zip -d / \
    && rm chrome-headless-shell-linux64.zip

RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/127.0.6533.72/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip -d / \
    && rm chromedriver-linux64.zip \
    && chmod +x /chromedriver-linux64/chromedriver

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/SSSB

#CMD ["sh", "-c", "python ../check_sssb.py --endless --headless --get_url & python ../check_sssb.py --endless --headless --check_url"]
#CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8082 & python ../check_sssb.py --endless --headless --get_url & python ../check_sssb.py --endless --headless --check_url & python ../check_sssb.py --endless --headless --check_filter"]
