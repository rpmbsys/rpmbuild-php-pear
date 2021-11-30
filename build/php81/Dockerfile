ARG centos=7.9.2009
FROM aursu/php81build:${centos}-build

RUN yum -y --enablerepo=bintray-php81custom install \
        php-pear \
    && yum clean all && rm -rf /var/cache/yum /var/cache/dnf
