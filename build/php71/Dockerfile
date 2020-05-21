ARG centos=7.8.2003

FROM aursu/php7build:${centos}-build

RUN yum -y --enablerepo=bintray-php71custom install \
        php-pear \
    && yum clean all && rm -rf /var/cache/yum /var/cache/dnf
