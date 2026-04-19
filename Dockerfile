ARG os=8.10.20240528
ARG buildrepo=php56build
ARG image=build

FROM ghcr.io/rpmbsys/${buildrepo}:${os}-${image}

RUN dnf -y install \
        gnupg2 \
    && dnf clean all && rm -rf /var/cache/dnf /var/lib/rpm/__db*

COPY SOURCES ${BUILD_TOPDIR}/SOURCES
COPY SPECS ${BUILD_TOPDIR}/SPECS

RUN chown -R $BUILD_USER ${BUILD_TOPDIR}/{SOURCES,SPECS}

USER $BUILD_USER

ENTRYPOINT ["/usr/bin/rpmbuild", "php-pear.spec"]
CMD ["-ba"]
