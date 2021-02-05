ARG centos=7.9.2009
ARG buildrepo=php74build
ARG image=build

FROM aursu/${buildrepo}:${centos}-${image}

COPY SOURCES ${BUILD_TOPDIR}/SOURCES
COPY SPECS ${BUILD_TOPDIR}/SPECS

RUN chown -R $BUILD_USER ${BUILD_TOPDIR}/{SOURCES,SPECS}

USER $BUILD_USER

ENTRYPOINT ["/usr/bin/rpmbuild", "php74-pear.spec"]
CMD ["-ba"]
