# syntax=docker/dockerfile:1
FROM phoronix/pts:latest

RUN apt-get update & apt-get upgrade -y
RUN apt-get install -y pkg-config
RUN /phoronix-test-suite/phoronix-test-suite install pts/sysbench pts/sockperf

COPY ./phoronix-test-suite.xml /etc

RUN mkdir -p /var/ctr-tools-test/results
COPY ./run-tests.sh /var/ctr-tools-test

RUN mkdir -p /var/lib/phoronix-test-suite/test-suites/local/containerization-tools-testing
COPY ./suite-definition.xml /var/lib/phoronix-test-suite/test-suites/local/ctr-tools-test


ENTRYPOINT [ "echo", "'test'" ]
