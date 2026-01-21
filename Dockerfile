

FROM python:3.11-bookworm


WORKDIR /app


COPY . .


RUN pip install .


ENTRYPOINT [ "/bin/bash" ]


