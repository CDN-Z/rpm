FROM ubuntu:latest
LABEL authors="brianvo"

ENTRYPOINT ["top", "-b"]