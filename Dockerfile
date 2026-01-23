

FROM python:3.9-bookworm


WORKDIR /app


COPY . .


RUN pip install .


ENTRYPOINT [ "/bin/bash" ]


