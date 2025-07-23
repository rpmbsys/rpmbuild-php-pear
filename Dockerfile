ARG os=10.0.20250606
ARG buildrepo=php84build
ARG image=build

FROM aursu/${buildrepo}:${os}-${image}

RUN dnf -y install \
        gnupg2 \
    && dnf clean all && rm -rf /var/cache/dnf /var/lib/rpm/__db*

COPY SOURCES ${BUILD_TOPDIR}/SOURCES
COPY SPECS ${BUILD_TOPDIR}/SPECS

RUN chown -R $BUILD_USER ${BUILD_TOPDIR}/{SOURCES,SPECS}

USER $BUILD_USER

ENTRYPOINT ["/usr/bin/rpmbuild", "php8-pear.spec"]
CMD ["-ba"]
