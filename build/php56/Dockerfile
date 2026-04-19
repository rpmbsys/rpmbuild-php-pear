ARG os=8.10.20240528
FROM aursu/php56build:${os}-build

RUN dnf -y --enablerepo=bintray-phpcustom install \
        php-pear \
    && dnf clean all && rm -rf /var/cache/dnf /var/lib/rpm/__db*
