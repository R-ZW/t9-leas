# Ambiente de execução da T9 (LEAS 2026/2) — Foremost-NG
#
# Um contêiner novo por cadeia. A LLM avaliadora (Claude Code, no host) executa
# o próprio roteiro dentro dele com `docker exec`.
#
# Ubuntu 24.04 limpo, com o arquivo apt fixado no dia do commit avaliado
# (bb812a22, 08/07/2025), como na execução de referência da T8. As dependências
# do Foremost-NG NÃO vêm instaladas: instalá-las faz parte do roteiro da LLM.
#
# Construção (na pasta ambiente/):  docker build -t t9/foremost-ng-exec:1 .

FROM ubuntu:noble-20250619@sha256:440dcf6a5640b2ae5c77724e68787a906afb8ddee98bf86db94eea8528c2c076

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8

ARG APT_SNAPSHOT=20250708T190020Z
RUN echo "APT::Snapshot \"${APT_SNAPSHOT}\";" > /etc/apt/apt.conf.d/50snapshot

# A imagem base não traz certificados e o snapshot só atende por HTTPS. Só este
# passo desliga a verificação TLS; a assinatura GPG do apt continua valendo.
RUN apt-get update -o Acquire::https::Verify-Peer=false \
 && apt-get install -y --no-install-recommends -o Acquire::https::Verify-Peer=false \
      ca-certificates=20240203 \
 && rm -rf /var/lib/apt/lists/*

# Mínimo de um revisor no terminal: sudo (o README usa `sudo make install`),
# unzip (para abrir artefato.zip) e o man real. Nenhum compilador.
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      sudo=1.9.15p5-3ubuntu5.24.04.1 \
      unzip=6.0-28ubuntu4.1 \
      man-db=2.12.0-4build2 \
 && rm -rf /var/lib/apt/lists/* \
 && if [ -f /usr/bin/man.REAL ]; then \
      rm -f /usr/bin/man && dpkg-divert --quiet --remove --rename /usr/bin/man; \
    fi

RUN useradd -m -s /bin/bash revisor \
 && echo 'revisor ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/revisor \
 && chmod 0440 /etc/sudoers.d/revisor

USER revisor
WORKDIR /home/revisor
CMD ["sleep", "infinity"]
