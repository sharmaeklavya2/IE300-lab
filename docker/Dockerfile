FROM debian:bookworm-slim

RUN apt-get update

COPY install-python.sh /tmp/install-python.sh
RUN bash /tmp/install-python.sh

COPY tl.profile /tmp/tl.profile
COPY install-texlive.sh /tmp/install-texlive.sh
RUN bash /tmp/install-texlive.sh

RUN rm -rf /var/lib/apt/lists/*

ENV PATH="/texlive/bin/active:${PATH}"

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /workspace
ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
