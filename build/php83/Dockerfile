ARG os=9.4.20240523
FROM aursu/php83build:${os}-build

RUN dnf -y --enablerepo=bintray-phpcustom install \
        php-pear \
    && dnf clean all && rm -rf /var/cache/dnf /var/lib/rpm/__db*
