FROM fedora:28
WORKDIR /var/www/html
EXPOSE 80

RUN dnf -y update && dnf clean all

RUN dnf install -y \
    nginx \
    screen \
    unzip \
    wget \
    nodejs \
    && dnf clean all \
    && npm update -g \
    && npm install -g n \
    && npm cache clean -f \
    && n stable

RUN pip3 install \
    envs \
    flask \
    flask-admin \
    peewee \
    wtf-peewee \
    psycopg2-binary \
    cryptography==2.0 \
    pymysql \
    flask-security-too \
    pandas \
    scikit-learn \
    geopandas \
    geopy \
    elasticsearch \
    geojson \
    plotly \
    tqdm \
    mapboxgl \
    cufflinks \
    geohash2 \
    tables \
    mixpanel \
    GeoAlchemy2 \
    nltk \
    beautifulsoup4 \
    flask-uploads \
    flask-dropzone

COPY . /var/www/html
COPY ./docker/nginx.conf /etc/nginx/
COPY ./jupyter/nltk_data/ /usr/share/nltk_data/
RUN ln -sf /dev/stdout /var/www/html/access.log && ln -sf /dev/stderr /var/www/html/error.log
RUN echo "screen -r" > /root/.bash_history

ENTRYPOINT ["/var/www/html/start.sh"]

