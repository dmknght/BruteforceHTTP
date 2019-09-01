FROM debian:latest
# Test with Debian
# Replace by Unbutu if has error

MAINTAINER DmKnght <dmknght@parrotsec.org>

# Install dependencies
# Can run both python2 and 3

RUN apt-get update && \
    apt-get install python-bs4 python-regex python-lxml -y \
    apt-get -y clean

COPY . /usr/local/share/BruteforceHTTP

RUN cd /usr/local/share/BruteforceHTTP && \

ENTRYPOINT ["main"]