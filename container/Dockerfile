# syntax=docker/dockerfile:1
FROM phoronix/pts:latest

# Update and install dependencies
RUN apt-get update & apt-get upgrade -y
RUN apt-get install -y pkg-config

# Install tests
RUN /phoronix-test-suite/phoronix-test-suite install pts/sysbench pts/sockperf pts/apache pts/mysqlslap

# Phoronix config file
COPY ./phoronix-test-suite.xml /etc

# Results dir and run-tests script
RUN mkdir -p /var/ctr-tools-test/results
COPY ./run-tests.sh /var/ctr-tools-test

# Test suite
RUN mkdir -p /var/lib/phoronix-test-suite/test-suites/local/ctr-tools-test
COPY ./suite-definition.xml /var/lib/phoronix-test-suite/test-suites/local/ctr-tools-test


ENTRYPOINT [ "/bin/bash", "-c" ]
CMD [ "/var/ctr-tools-test/run-tests.sh" ]
