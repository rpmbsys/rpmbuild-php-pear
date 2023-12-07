ARG os=8.7.20221112
FROM aursu/php83build:${os}-build

RUN dnf -y --enablerepo=bintray-phpcustom install \
        php-pear \
    && dnf clean all && rm -rf /var/cache/dnf /var/lib/rpm/__db*
