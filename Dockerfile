ARG os=9.4.20240523
ARG buildrepo=php83build
ARG image=build

FROM aursu/${buildrepo}:${os}-${image}

COPY SOURCES ${BUILD_TOPDIR}/SOURCES
COPY SPECS ${BUILD_TOPDIR}/SPECS

RUN chown -R $BUILD_USER ${BUILD_TOPDIR}/{SOURCES,SPECS}

USER $BUILD_USER

ENTRYPOINT ["/usr/bin/rpmbuild", "php8-pear.spec"]
CMD ["-ba"]
