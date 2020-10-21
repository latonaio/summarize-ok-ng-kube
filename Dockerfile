FROM l4t:latest

# Definition of a Device & Service
ENV POSITION=Runtime \
    SERVICE=summarize-ok-ng \
    AION_HOME=/var/lib/aion

RUN mkdir ${AION_HOME}
WORKDIR ${AION_HOME}
# Setup Directoties
RUN mkdir -p \
    $POSITION/$SERVICE
WORKDIR ${AION_HOME}/$POSITION/$SERVICE/

ADD . .

CMD ["python3", "-u", "main.py"]
# ENTRYPOINT ["/bin/sh", "-c", "while :; do sleep 10; done"]