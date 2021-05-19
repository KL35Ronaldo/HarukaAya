FROM registry.gitlab.com/harukanetwork/oss/harukaaya:dockerstation-beta

RUN git clone https://gitlab.com/HarukaNetwork/OSS/HarukaAya.git -b ptb13-revive /data/HarukaBeta

COPY ./config.yml /data/HarukaBeta

WORKDIR /data/HarukaBeta

CMD ["python", "-m", "haruka"]
