ARG centos=7

FROM aursu/php7build:${centos}-build

RUN yum -y --enablerepo custom --enablerepo=bintray-php71custom install \
        php-pear \
    && yum clean all && rm -rf /var/cache/yum /var/cache/dnf
