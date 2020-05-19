ARG centos=7.8.2003

FROM aursu/php74build:${centos}-build

RUN yum -y --enablerepo custom --enablerepo=bintray-php74custom install \
        php-pear \
    && yum clean all && rm -rf /var/cache/yum /var/cache/dnf
