FROM debian:latest
# Test with Debian
# Replace by Unbutu if has error

MAINTAINER DmKnght <dmknght@parrotsec.org>

# Install dependencies
# Can run both python2 and 3

RUN apt update && \
    apt install python-bs4 python-regex python-lxml -y

COPY . /usr/local/share/BruteforceHTTP/

RUN cd /usr/local/share/BruteforceHTTP/

ENTRYPOINT ["/bin/bash"]