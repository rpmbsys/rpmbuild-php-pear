ARG os=8.10.20240528
ARG buildrepo=php56build
ARG image=build
FROM ghcr.io/rpmbsys/${buildrepo}:${os}-${image}

RUN dnf -y --enablerepo=bintray-phpcustom install \
        php-pear \
    && dnf clean all && rm -rf /var/cache/dnf /var/lib/rpm/__db*
