ARG centos=7
ARG buildrepo=php5build

FROM aursu/${buildrepo}:${centos}-build

RUN yum -y --enablerepo custom install \
        php-pear \
    && yum clean all && rm -rf /var/cache/yum
