# Fedora spec file for php-pear
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global with_relocation 0%{?_with_relocation:1}

%define _debugsource_template %{nil}
%define debug_package %{nil}

%if %{with_relocation}
%global program_suffix      7
%global main_name           php7
%global php_sysconfdir      %{_sysconfdir}/php7
%global php_datadir         %{_datadir}/php7
%global php_sharedstatedir  %{_sharedstatedir}/php7
%global php_docdir          %{_docdir}/php7
%global pear_cachedir       %{_localstatedir}/cache/php7-pear
%global pear_sharedstatedir %{php_sharedstatedir}/pear
%global pear_datadir        %{php_datadir}
%global tests_datadir       %{php_datadir}/tests
%global bin_cli             php%{program_suffix}
%global bin_pecl            pecl%{program_suffix}
%global bin_pear            pear%{program_suffix}
%global bin_peardev         peardev%{program_suffix}
%else
%global main_name           php
%global php_sysconfdir      %{_sysconfdir}
%global php_datadir         %{_datadir}/php
%global php_sharedstatedir  %{_sharedstatedir}/php
%global php_docdir          %{_docdir}
%global pear_cachedir       %{_localstatedir}/cache/php-pear
%global pear_sharedstatedir %{_sharedstatedir}/pear
%global pear_datadir        %{_datadir}
%global tests_datadir       %{_datadir}/tests
%global bin_cli             php
%global bin_pecl            pecl
%global bin_pear            pear
%global bin_peardev         peardev
%endif

%global pear_name           %{main_name}-pear
%global cli_name            %{main_name}-cli
%global xml_name            %{main_name}-xml
%global devel_name          %{main_name}-devel
%global peardir             %{pear_datadir}/pear
%global metadir             %{pear_sharedstatedir}

%global getoptver 1.4.3
%global arctarver 1.4.14
# https://pear.php.net/bugs/bug.php?id=19367
# Structures_Graph 1.0.4 - incorrect FSF address
%global structver 1.1.1
%global xmlutil   1.4.5
%global manpages  1.10.0

# Tests are only run with rpmbuild --with tests
# Can't be run in mock / koji because PEAR is the first package
%global with_tests 0%{?_with_tests:1}

%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

%{!?pecl_xmldir: %global pecl_xmldir %{php_sharedstatedir}/peclxml}

Summary: PHP Extension and Application Repository framework
Name: %{pear_name}
Version: 1.10.13
Release: 1%{?dist}
Epoch: 1
# PEAR, PEAR_Manpages, Archive_Tar, XML_Util, Console_Getopt are BSD
# Structures_Graph is LGPLv3+
License: BSD and LGPLv3+
Group: Development/Languages
URL: http://pear.php.net/package/PEAR
Source0: http://download.pear.php.net/package/PEAR-%{version}%{?pearprever}.tgz
# wget https://raw.githubusercontent.com/pear/pear-core/stable/install-pear.php
Source1: install-pear.php

Source3: cleanup.php
Source10: pear.sh
Source11: pecl.sh
Source12: peardev.sh
Source13: macros.pear

Source103: php7-cleanup.php
Source110: php7-pear.sh
Source111: php7-pecl.sh
Source112: php7-peardev.sh
Source113: php7-macros.pear

Source213: macros.pear.php7

Source21: http://pear.php.net/get/Archive_Tar-%{arctarver}.tgz
Source22: http://pear.php.net/get/Console_Getopt-%{getoptver}.tgz
Source23: http://pear.php.net/get/Structures_Graph-%{structver}.tgz
Source24: http://pear.php.net/get/XML_Util-%{xmlutil}.tgz
Source25: http://pear.php.net/get/PEAR_Manpages-%{manpages}.tgz

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php(language) >= 7
BuildRequires: %{cli_name}
BuildRequires: %{xml_name}
BuildRequires: %{_bindir}/gpg
# For pecl_xmldir macro
BuildRequires: %{devel_name}
%if %{with_tests}
BuildRequires:  %{_bindir}/phpunit
%endif
%if 0%{?fedora}
BuildRequires:  php-fedora-autoloader-devel
%endif

Provides: php-pear(Console_Getopt) = %{getoptver}
Provides: php-pear(Archive_Tar) = %{arctarver}
Provides: php-pear(PEAR) = %{version}
Provides: php-pear(Structures_Graph) = %{structver}
Provides: php-pear(XML_Util) = %{xmlutil}
Provides: php-pear(PEAR_Manpages) = %{manpages}

Provides: php-composer(pear/console_getopt) = %{getoptver}
Provides: php-composer(pear/archive_tar) = %{arctarver}
Provides: php-composer(pear/pear-core-minimal) = %{version}
Provides: php-composer(pear/structures_graph) = %{structver}
Provides: php-composer(pear/xml_util) = %{xmlutil}
%if 0%{?fedora}
Provides: php-autoloader(pear/console_getopt) = %{getoptver}
Provides: php-autoloader(pear/archive_tar) = %{arctarver}
Provides: php-autoloader(pear/pear-core-minimal) = %{version}
Provides: php-autoloader(pear/structures_graph) = %{structver}
Provides: php-autoloader(pear/xml_util) = %{xmlutil}
%endif

# Archive_Tar requires 5.2
# XML_Util, Structures_Graph require 5.3
# Console_Getopt requires 5.4
# PEAR requires 5.4
Requires: php(language) >= 7
Requires: %{cli_name}
# phpci detected extension
# PEAR (date, spl always builtin):
Requires: php-ftp >= 7
Requires: php-pcre >= 7
Requires: php-posix >= 7
Requires: php-tokenizer >= 7
Requires: %{xml_name}
Requires: php-zlib >= 7
# Console_Getopt: pcre
# Archive_Tar: pcre, posix, zlib
Requires: php-bz2 >= 7
# Structures_Graph: none
# XML_Util: pcre
# optional: overload and xdebug
%if 0%{?fedora}
Requires: php-composer(fedora/autoloader)
%endif

%description
PEAR is a framework and distribution system for reusable PHP
components.  This package contains the basic PEAR components.

%package -n php-pear-doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
Conflicts: php-pear

%description -n php-pear-doc
Documentation for %{name}.

%prep
%setup -cT

# Create a usable PEAR directory (used by install-pear.php)
for archive in %{SOURCE0} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24} %{SOURCE25}
do
    tar xzf  $archive --strip-components 1 || tar xzf  $archive --strip-path 1
    file=${archive##*/}
    [ -f LICENSE ] && mv LICENSE LICENSE-${file%%-*}
    [ -f README ]  && mv README  README-${file%%-*}

    tar xzf $archive --wildcards 'package*xml'
    [ -f package2.xml ] && mv package2.xml ${file%%-*}.xml \
                        || mv package.xml  ${file%%-*}.xml
done
cp %{SOURCE1} .

# apply patches on PEAR needed during install
# other patches applied on installation tree

sed -e 's:@BINDIR@:%{_bindir}:' \
    -e 's:@LIBDIR@:%{_localstatedir}/lib:' \
%if %{with_relocation}
    %{SOURCE113} > macros.pear
%else
%if "%{php_version}" < "7.4"
    %{SOURCE13} > macros.pear
%else
    %{SOURCE213} > macros.pear
%endif # php_version
%endif # with_relocation

%build
%if 0%{?fedora}
# Create per package autoloader
phpab --template fedora \
      --output PEAR/autoload.php\
      PEAR OS System.php PEAR.php

phpab --template fedora \
      --output Structures/Graph/autoload.php \
      Structures

mkdir Archive/Tar
phpab --template fedora \
      --output Archive/Tar/autoload.php \
      Archive

mkdir Console/Getopt
phpab --template fedora \
      --output Console/Getopt/autoload.php \
      Console

mkdir XML/Util
phpab --template fedora \
      --output XML/Util/autoload.php \
      XML
%endif

%install
rm -rf %{buildroot}

export PHP_PEAR_SYSCONF_DIR=%{php_sysconfdir}
export PHP_PEAR_SIG_KEYDIR=%{php_sysconfdir}/pearkeys
export PHP_PEAR_SIG_BIN=%{_bindir}/gpg
export PHP_PEAR_INSTALL_DIR=%{peardir}

# 1.4.11 tries to write to the cache directory during installation
# so it's not possible to set a sane default via the environment.
# The ${PWD} bit will be stripped via relocate.php later.
export PHP_PEAR_CACHE_DIR=${PWD}%{pear_cachedir}
export PHP_PEAR_TEMP_DIR=/var/tmp

install -d %{buildroot}%{peardir} \
           %{buildroot}%{pear_cachedir} \
           %{buildroot}%{_localstatedir}/www/html \
           %{buildroot}%{pear_sharedstatedir}/pkgxml \
           %{buildroot}%{php_sysconfdir}/pear

export INSTALL_ROOT=%{buildroot}

%{_bindir}/%{bin_cli} --version

%{_bindir}/%{bin_cli} -dmemory_limit=64M -dshort_open_tag=0 -dsafe_mode=0 \
         -d 'error_reporting=E_ALL&~E_DEPRECATED' -ddetect_unicode=0 \
         install-pear.php --force \
                 --dir      %{peardir} \
                 --cache    %{pear_cachedir} \
                 --config   %{php_sysconfdir}/pear \
                 --bin      %{_bindir} \
                 --www      %{_localstatedir}/www/html \
                 --doc      %{php_docdir}/pear \
                 --test     %{tests_datadir}/pear \
                 --data     %{pear_datadir}/pear-data \
                 --metadata %{metadir} \
                 --man      %{_mandir} \
                 --php      %{_bindir}/%{bin_cli} \
                 %{SOURCE0} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24} %{SOURCE25}

# Replace /usr/bin/* with simple scripts:
%if %{with_relocation}
install -m 755 %{SOURCE110} %{buildroot}%{_bindir}/%{bin_pear}
install -m 755 %{SOURCE111} %{buildroot}%{_bindir}/%{bin_pecl}
install -m 755 %{SOURCE112} %{buildroot}%{_bindir}/%{bin_peardev}
%{_bindir}/%{bin_cli} %{SOURCE103} %{buildroot}%{php_sysconfdir}/pear.conf %{_datadir}
%else
install -m 755 %{SOURCE10} %{buildroot}%{_bindir}/%{bin_pear}
install -m 755 %{SOURCE11} %{buildroot}%{_bindir}/%{bin_pecl}
install -m 755 %{SOURCE12} %{buildroot}%{_bindir}/%{bin_peardev}
%{_bindir}/%{bin_cli} %{SOURCE3} %{buildroot}%{php_sysconfdir}/pear.conf %{_datadir}
%endif

# Display configuration for debug
%{_bindir}/%{bin_cli} -r "print_r(unserialize(substr(file_get_contents('%{buildroot}%{php_sysconfdir}/pear.conf'),17)));"

%if %{with_relocation}
install -m 644 -D macros.pear \
           %{buildroot}%{macrosdir}/macros.pear7
%else
install -m 644 -D macros.pear \
           %{buildroot}%{macrosdir}/macros.pear
%endif

# apply patches on installed PEAR tree
pushd %{buildroot}%{peardir}
: no patch
popd

# Why this file here ?
rm -rf %{buildroot}/.depdb* %{buildroot}/.lock %{buildroot}/.channels %{buildroot}/.filemap

# Need for re-registrying XML_Util
install -m 644 *.xml %{buildroot}%{pear_sharedstatedir}/pkgxml

%if 0%{?fedora}
# install autoloaders
for i in PEAR/autoload.php Structures/Graph/autoload.php Archive/Tar/autoload.php Console/Getopt/autoload.php XML/Util/autoload.php
do install -Dpm 644 $i %{buildroot}%{peardir}/$i
done
%endif

%check
# Check that no bogus paths are left in the configuration, or in
# the generated registry files.
grep %{buildroot} %{buildroot}%{php_sysconfdir}/pear.conf && exit 1
grep %{_libdir} %{buildroot}%{php_sysconfdir}/pear.conf && exit 1
grep '"/tmp"' %{buildroot}%{php_sysconfdir}/pear.conf && exit 1
grep /usr/local %{buildroot}%{php_sysconfdir}/pear.conf && exit 1
grep -rl %{buildroot} %{buildroot} && exit 1


%if %{with_tests}
cp %{php_sysconfdir}/php.ini .
echo "include_path=.:%{buildroot}%{peardir}:%{php_sharedstatedir}" >>php.ini
export PHPRC=$PWD/php.ini
LOG=$PWD/rpmlog
ret=0

cd %{buildroot}%{tests_datadir}/pear/Structures_Graph/tests
phpunit \
   AllTests || ret=1

cd %{buildroot}%{tests_datadir}/pear/XML_Util/tests
%{_bindir}/%{bin_cli} \
   %{buildroot}%{pear_sharedstatedir}/pearcmd.php \
   run-tests --ini="-d include_path=.:%{buildroot}%{peardir}:%{php_sharedstatedir}" \
   | tee $LOG

cd %{buildroot}%{tests_datadir}/pear/Console_Getopt/tests
%{_bindir}/%{bin_cli} \
   %{buildroot}%{pear_sharedstatedir}/pearcmd.php \
   run-tests --ini="-d include_path=.:%{buildroot}%{peardir}:%{php_sharedstatedir}" \
   | tee -a $LOG

grep "FAILED TESTS" $LOG && ret=1

exit $ret
%else
echo 'Test suite disabled (missing "--with tests" option)'
%endif

%clean
rm -rf %{buildroot}

%pre
# Manage relocation of metadata, before update to pear
if [ -d %{peardir}/.registry -a ! -d %{metadir}/.registry ]; then
  mkdir -p %{metadir}
  mv -f %{peardir}/.??* %{metadir}
fi

%post
# force new value as pear.conf is (noreplace)
current=$(%{_bindir}/%{bin_pear} config-get test_dir system)
if [ "$current" != "%{tests_datadir}/pear" ]; then
%{_bindir}/%{bin_pear} config-set \
    test_dir %{tests_datadir}/pear \
    system >/dev/null || :
fi

current=$(%{_bindir}/%{bin_pear} config-get data_dir system)
if [ "$current" != "%{pear_datadir}/pear-data" ]; then
%{_bindir}/%{bin_pear} config-set \
    data_dir %{pear_datadir}/pear-data \
    system >/dev/null || :
fi

current=$(%{_bindir}/%{bin_pear} config-get metadata_dir system)
if [ "$current" != "%{metadir}" ]; then
%{_bindir}/%{bin_pear} config-set \
    metadata_dir %{metadir} \
    system >/dev/null || :
fi

current=$(%{_bindir}/%{bin_pear} config-get -c pecl doc_dir system)
if [ "$current" != "%{php_docdir}/pecl" ]; then
%{_bindir}/%{bin_pear} config-set \
    -c pecl \
    doc_dir %{php_docdir}/pecl \
    system >/dev/null || :
fi

current=$(%{_bindir}/%{bin_pear} config-get -c pecl test_dir system)
if [ "$current" != "%{tests_datadir}/pecl" ]; then
%{_bindir}/%{bin_pear} config-set \
    -c pecl \
    test_dir %{tests_datadir}/pecl \
    system >/dev/null || :
fi

%postun
if [ $1 -eq 0 -a -d %{metadir}/.registry ] ; then
  rm -rf %{metadir}/.registry
fi

%files
%defattr(-,root,root,-)
%{peardir}
%dir %{metadir}
%{metadir}/.channels
%verify(not mtime size md5) %{metadir}/.depdb
%verify(not mtime)          %{metadir}/.depdblock
%verify(not mtime size md5) %{metadir}/.filemap
%verify(not mtime)          %{metadir}/.lock
%{metadir}/.registry
%{metadir}/pkgxml
%{_bindir}/%{bin_pear}
%{_bindir}/%{bin_pecl}
%{_bindir}/%{bin_peardev}
%config(noreplace) %{php_sysconfdir}/pear.conf
%if %{with_relocation}
%{macrosdir}/macros.pear7
%else
%{macrosdir}/macros.pear
%endif
%dir %{pear_cachedir}
%dir %{php_sysconfdir}/pear
%{!?_licensedir:%global license %%doc}
%license LICENSE*
%{tests_datadir}/pear
%{pear_datadir}/pear-data
%dir %{php_docdir}/pear
%doc %{php_docdir}/pear/*
%if %{with_relocation}
%exclude %{_bindir}/pear
%exclude %{_bindir}/peardev
%exclude %{_bindir}/pecl
%endif

%files -n php-pear-doc
%doc README*
%{_mandir}/man1/pear.1*
%{_mandir}/man1/pecl.1*
%{_mandir}/man1/peardev.1*
%{_mandir}/man5/pear.conf.5*

%changelog
* Wed Aug 11 2021 Remi Collet <remi@remirepo.net> - 1.10.13-1
- update to 1.10.13

* Wed Jul 21 2021 Remi Collet <remi@remirepo.net> - 1:1.10.12-9
- update Archive_Tar to 1.4.14

* Fri Feb  5 2021 Alexander Ursu <alexander.ursu@gmail.com> - 1:1.10.12-6
- Setup pecl_xmldir in macros file

* Tue Jan 19 2021 Remi Collet <remi@remirepo.net> - 1:1.10.12-5
- update Archive_Tar to 1.4.12

* Mon Nov 23 2020 Remi Collet <remi@remirepo.net> - 1:1.10.12-4
- update Archive_Tar to 1.4.11

* Wed Sep 16 2020 Remi Collet <remi@remirepo.net> - 1:1.10.12-3
- update Archive_Tar to 1.4.10

* Sun Jun 28 2020 Alexander Ursu <alexander.ursu@gmail.com> - 1:1.10.12-2
- Build for CentOS 8.2

* Mon Apr 20 2020 Remi Collet <remi@remirepo.net> - 1:1.10.12-1
- update PEAR to 1.10.12
- update XML_Util to 1.4.5
- update Archive_Tar to 1.4.9

* Thu Nov 21 2019 Remi Collet <remi@remirepo.net> - 1:1.10.10-2
- update Console_Getopt to 1.4.3
- drop patches merged upstream

* Wed Nov 20 2019 Remi Collet <remi@remirepo.net> - 1:1.10.10-1
- update PEAR to 1.10.10

* Tue Oct 22 2019 Remi Collet <remi@remirepo.net> - 1:1.10.9-4
- update Archive_Tar to 1.4.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.10.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr  8 2019 Remi Collet <remi@remirepo.net> - 1:1.10.9-2
- update Archive_Tar to 1.4.7

* Thu Mar 14 2019 Remi Collet <remi@remirepo.net> - 1:1.10.9-1
- update PEAR to 1.10.9

* Fri Feb  8 2019 Remi Collet <remi@remirepo.net> - 1:1.10.8-1
- update PEAR to 1.10.8
- source generated from github tag
- drop patch merged upstream

* Thu Feb  7 2019 Remi Collet <remi@remirepo.net> - 1:1.10.7-5
- update Console_Getopt to 1.4.2

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.10.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan  3 2019 Remi Collet <remi@remirepo.net> - 1:1.10.7-3
- update Archive_Tar to 1.4.5

* Fri Dec 21 2018 Remi Collet <remi@remirepo.net> - 1:1.10.7-2
- update Archive_Tar to 1.4.4
- drop PHP 7.2 deprecated option, patch from
  https://github.com/pear/pear-core/pull/83

* Thu Dec  6 2018 Remi Collet <remi@remirepo.net> - 1:1.10.7-1
- update PEAR to 1.10.7

* Thu Aug 23 2018 Remi Collet <remi@remirepo.net> - 1:1.10.6-1
- update PEAR to 1.10.6

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.10.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Apr 11 2018 Remi Collet <remi@remirepo.net> - 1:1.10.5-8
- require /usr/bin/gpg instead of gnupg

* Tue Mar  6 2018 Remi Collet <remi@remirepo.net> - 1:1.10.5-7
- enable autoloader only in Fedora

* Tue Feb 13 2018 Remi Collet <remi@remirepo.net> - 1:1.10.5-6
- add patch for PHP 7.2 from
  https://github.com/pear/pear-core/pull/71

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.10.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Dec 19 2017 Remi Collet <remi@remirepo.net> - 1:1.10.5-4
- add autoloader for each package

* Thu Jun 29 2017 Remi Collet <remi@remirepo.net> - 1:1.10.5-2
- update XML_Util to 1.4.3 (no change)

* Wed Jun 28 2017 Remi Collet <remi@remirepo.net> 1:1.10.5-1
- update PEAR to 1.10.5 (no change)

* Mon Jun 12 2017 Remi Collet <remi@remirepo.net> 1:1.10.4-2
- update Archive_Tar to 1.4.3

* Thu Apr 27 2017 Remi Collet <remi@remirepo.net> 1:1.10.4-1
- update PEAR to 1.10.4

* Tue Feb 28 2017 Remi Collet <remi@fedoraproject.org> 1:1.10.3-1
- update PEAR to 1.10.3

* Thu Feb 23 2017 Remi Collet <remi@fedoraproject.org> 1:1.10.1-12
- update XML_Util to 1.4.2
- drop patch merged upstream

* Wed Feb 22 2017 Remi Collet <remi@fedoraproject.org> 1:1.10.1-11
- add patch to fix XML_Serializer with XML_Util 1.4.1
  from https://github.com/pear/XML_Util/pull/8

* Wed Feb  8 2017 Remi Collet <remi@fedoraproject.org> 1:1.10.1-10
- update XML_Util to 1.4.1

* Sat Feb  4 2017 Remi Collet <remi@fedoraproject.org> 1:1.10.1-9
- update XML_Util to 1.4.0

* Fri Sep 30 2016 Remi Collet <remi@fedoraproject.org> 1:1.10.1-7
- fix https connection via a proxy
  patch from https://github.com/pear/pear-core/pull/51
- silent the new scriplets

* Fri Aug  5 2016 Remi Collet <remi@fedoraproject.org> 1:1.10.1-6
- improve default config, to avoid change in scriptlet
- spec cleanup and remove unneeded scriplets

* Thu Jun 30 2016 Remi Collet <remi@fedoraproject.org> 1:1.10.1-5
- don't own test/doc directories for pecl packages #1351345

* Thu Feb 25 2016 Remi Collet <remi@fedoraproject.org> 1:1.10.1-4
- update Archive_Tar to 1.4.2

* Wed Feb 10 2016 Remi Collet <remi@fedoraproject.org> 1:1.10.1-3
- use file triggers for pecl extensions (un)registration
- define %%pecl_install and %%pecl_uninstall as noop macro

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Oct 17 2015 Remi Collet <remi@fedoraproject.org> 1:1.10.1-1
- update PEAR to 1.10.1

* Wed Oct  7 2015 Remi Collet <remi@fedoraproject.org> 1:1.10.0-1
- update PEAR and PEAR_Manpages to 1.10.0

* Tue Sep 29 2015 Remi Collet <remi@fedoraproject.org> 1:1.10.0-0.2.dev3
- update PEAR to 1.10.0dev3

* Fri Jul 31 2015 Remi Collet <remi@fedoraproject.org> 1:1.10.0-0.1.dev2
- update PEAR to 1.10.0dev2
- drop all patches, merged upstream
- drop man pages from sources
- add PEAR_Manpages upstream package

* Tue Jul 21 2015 Remi Collet <remi@fedoraproject.org> 1:1.9.5-12
- update Console_Getopt to 1.4.1
- update Structures_Graph to 1.1.1

* Mon Jul 20 2015 Remi Collet <remi@fedoraproject.org> 1:1.9.5-10
- update Archive_Tar to 1.4.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.9.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 14 2015 Remi Collet <remi@fedoraproject.org> 1:1.9.5-8
- update Archive_Tar to 1.3.16 (no change)

* Fri Mar 13 2015 Remi Collet <remi@fedoraproject.org> 1:1.9.5-7
- update Archive_Tar to 1.3.15 (no change)
- add composer provides

* Mon Mar  2 2015 Remi Collet <remi@fedoraproject.org> 1:1.9.5-6
- update XML_Util to 1.3.0

* Fri Feb 27 2015 Remi Collet <remi@fedoraproject.org> 1:1.9.5-5
- update Structures_Graph to 1.1.0
- update Archive_Tar to 1.3.14

* Mon Feb 23 2015 Remi Collet <remi@fedoraproject.org> 1:1.9.5-4
- update Console_Getopt to 1.4.0
- raise php minimum version to 5.4
- cleanup registry after removal
- drop old php-pear-XML-Util scriptlets
- remove PHP from License, Console_Getopt is now BSD

* Thu Sep  4 2014 Remi Collet <remi@fedoraproject.org> 1:1.9.5-3
- update Archive_Tar to 1.3.13
- requires httpd-filesystem for /var/www/html ownership (F21+)
- fix license handling

* Tue Aug 12 2014 Remi Collet <remi@fedoraproject.org> 1:1.9.5-2
- update Archive_Tar to 1.3.12

* Tue Jul 15 2014 Remi Collet <remi@fedoraproject.org> 1:1.9.5-1
- update PEAR to 1.9.5

* Sat Jun  7 2014 Remi Collet <remi@fedoraproject.org> 1:1.9.4-29
- update XML_Util to 1.2.3
- fix test suite (not used)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.9.4-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 17 2014 Remi Collet <rcollet@redhat.com> 1:1.9.4-27
- revert previous, was a bad solution

* Wed Apr  9 2014 Remi Collet <rcollet@redhat.com> 1:1.9.4-25
- only enable needed extensions for pear/pecl commands
- fix typo in pear man page

* Tue Feb 11 2014 Remi Collet <rcollet@redhat.com> 1:1.9.4-24
- Expand path in macros.pear
- Install macros to /usr/lib/rpm/macros.d where available

* Tue Oct 15 2013 Remi Collet <rcollet@redhat.com> 1:1.9.4-23
- set pecl test_dir to /usr/share/tests/pecl

* Mon Oct 14 2013 Remi Collet <rcollet@redhat.com> 1:1.9.4-22
- set pecl doc_dir to /usr/share/doc/pecl

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.9.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 10 2013 Remi Collet <rcollet@redhat.com> 1:1.9.4-20
- add man page for pear.conf file

* Tue Jun 18 2013 Remi Collet <rcollet@redhat.com> 1:1.9.4-19
- add man pages for pear, peardev and pecl commands

* Fri May  3 2013 Remi Collet <rcollet@redhat.com> 1:1.9.4-18
- don't verify metadata file content

* Thu Apr 25 2013 Remi Collet <rcollet@redhat.com> 1:1.9.4-17
- improve post scriptlet to avoid updating pear.conf
  when not needed

* Tue Mar 12 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1:1.9.4-16
- Remove %%config from %%{_sysconfdir}/rpm/macros.*
  (https://fedorahosted.org/fpc/ticket/259).

* Sat Feb  9 2013 Remi Collet <remi@fedoraproject.org> 1:1.9.4-15
- update Archive_Tar to 1.3.11
- drop php 5.5 patch merged upstream

* Tue Dec 11 2012 Remi Collet <remi@fedoraproject.org> 1:1.9.4-14
- add explicit requires on all needed extensions (phpci)
- fix pecl launcher (need ini to be parsed for some
  extenstions going to be build as shared, mainly simplexml)
- add fix for new unpack format (php 5.5)

* Wed Sep 26 2012 Remi Collet <remi@fedoraproject.org> 1:1.9.4-13
- move metadata to /var/lib/pear

* Wed Sep 26 2012 Remi Collet <remi@fedoraproject.org> 1:1.9.4-12
- drop relocate stuff, no more needed

* Sun Aug 19 2012 Remi Collet <remi@fedoraproject.org> 1:1.9.4-11
- move data to /usr/share/pear-data
- provides all package.xml

* Wed Aug 15 2012 Remi Collet <remi@fedoraproject.org> 1:1.9.4-10
- enforce test_dir on update

* Mon Aug 13 2012 Remi Collet <remi@fedoraproject.org> 1:1.9.4-9
- move tests to /usr/share/tests/pear
- move pkgxml to /var/lib/pear
- remove XML_RPC
- refresh installer

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.9.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 11 2012 Remi Collet <remi@fedoraproject.org> 1:1.9.4-7
- Update Archive_Tar to 1.3.10

* Wed Apr 04 2012 Remi Collet <remi@fedoraproject.org> 1:1.9.4-6
- fix Obsoletes version for XML_Util (#226295)
- add link to upstream bug - please Provides LICENSE file
  https://pear.php.net/bugs/bug.php?id=19368
- add link to upstream bug - Incorrect FSF address
  https://pear.php.net/bugs/bug.php?id=19367

* Mon Feb 27 2012 Remi Collet <remi@fedoraproject.org> 1:1.9.4-5
- Update Archive_Tar to 1.3.9
- add patch from RHEL (Joe Orton)
- fix install-pear.php URL (with our patch for doc_dir applied)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.9.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 15 2011 Remi Collet <remi@fedoraproject.org> 1:1.9.4-3
- update Archive_Tar to 1.3.8
- allow to build with "tests" option

* Sat Aug 27 2011 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.4-2
- update to XML_RPC-1.5.5

* Thu Jul 07 2011 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.4-1
- update to 1.9.4

* Fri Jun 10 2011 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.3-2
- fix pecl launcher

* Fri Jun 10 2011 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.3-1
- update to 1.9.3
- sync options in launcher (pecl, pear, peardev) with upstream

* Wed Mar 16 2011 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.2-3
- move %%{pear_docdir} to %%{_docdir}/pear
  https://fedorahosted.org/fpc/ticket/69

* Tue Mar  8 2011 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.2-2
- update Console_Getopt to 1.3.1 (no change)

* Mon Feb 28 2011 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.2-1
- update to 1.9.2 (bug + security fix)
  http://pear.php.net/advisory-20110228.txt

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.9.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 12 2010 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.1-6
- update Console_Getopt to 1.3.0
- don't require php-devel (#657812)
- update install-pear.php

* Tue Oct 26 2010 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.1-5
- update Structures_Graph to 1.0.4

* Fri Sep 10 2010 Joe Orton <jorton@redhat.com> - 1:1.9.1-4
- ship LICENSE file for XML_RPC

* Fri Sep 10 2010 Joe Orton <jorton@redhat.com> - 1:1.9.1-3
- require php-devel (without which pecl doesn't work)

* Mon Jul 05 2010 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.1-2
- update to XML_RPC-1.5.4

* Thu May 27 2010 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.1-1
- update to 1.9.1

* Thu Apr 29 2010 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.0-5
- update to Archive_Tar-1.3.7 (only metadata fix)

* Tue Mar 09 2010 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.0-4
- update to Archive_Tar-1.3.6

* Sat Jan 16 2010 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.0-3
- update to XML_RPC-1.5.3
- fix licenses (multiple)
- provide bundled LICENSE files

* Fri Jan 01 2010 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.0-2
- update to Archive_Tar-1.3.5, Structures_Graph-1.0.3

* Sat Sep 05 2009 Remi Collet <Fedora@FamilleCollet.com> 1:1.9.0-1
- update to PEAR 1.9.0, XML_RPC 1.5.2

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 30 2009 Remi Collet <Fedora@FamilleCollet.com> 1:1.8.1-1
- update to 1.8.1
- Update install-pear.php script (1.39)
- add XML_Util

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun May 18 2008 Remi Collet <Fedora@FamilleCollet.com> 1:1.7.2-2
- revert to install-pear.php script 1.31 (for cfg_dir)

* Sun May 18 2008 Remi Collet <Fedora@FamilleCollet.com> 1:1.7.2-1
- update to 1.7.2
- Update install-pear.php script (1.32)

* Tue Mar 11 2008 Tim Jackson <rpm@timj.co.uk> 1:1.7.1-2
- Set cfg_dir to be %%{_sysconfdir}/pear (and own it)
- Update install-pear.php script
- Add %%pear_cfgdir and %%pear_wwwdir macros

* Sun Feb  3 2008 Remi Collet <Fedora@FamilleCollet.com> 1:1.7.1-1
- update to 1.7.1

* Fri Feb  1 2008 Remi Collet <Fedora@FamilleCollet.com> 1:1.7.0-1
- update to 1.7.0

* Thu Oct  4 2007 Joe Orton <jorton@redhat.com> 1:1.6.2-2
- require php-cli not php

* Sun Sep  9 2007 Remi Collet <Fedora@FamilleCollet.com> 1:1.6.2-1
- update to 1.6.2
- remove patches merged upstream
- Fix : "pear install" hangs on non default channel (#283401)

* Tue Aug 21 2007 Joe Orton <jorton@redhat.com> 1:1.6.1-2
- fix License

* Thu Jul 19 2007 Remi Collet <Fedora@FamilleCollet.com> 1:1.6.1-1
- update to PEAR-1.6.1 and Console_Getopt-1.2.3

* Thu Jul 19 2007 Remi Collet <Fedora@FamilleCollet.com> 1:1.5.4-5
- new SPEC using install-pear.php instead of install-pear-nozlib-1.5.4.phar

* Mon Jul 16 2007 Remi Collet <Fedora@FamilleCollet.com> 1:1.5.4-4
- update macros.pear (without define)

* Mon Jul 16 2007 Joe Orton <jorton@redhat.com> 1:1.5.4-3
- add pecl_{un,}install macros to macros.pear (from Remi)

* Fri May 11 2007 Joe Orton <jorton@redhat.com> 1:1.5.4-2
- update to 1.5.4

* Tue Mar  6 2007 Joe Orton <jorton@redhat.com> 1:1.5.0-3
- add redundant build section (#226295)
- BR php-cli not php (#226295)

* Mon Feb 19 2007 Joe Orton <jorton@redhat.com> 1:1.5.0-2
- update builtin module provides (Remi Collet, #226295)
- drop patch 0

* Thu Feb 15 2007 Joe Orton <jorton@redhat.com> 1:1.5.0-1
- update to 1.5.0

* Mon Feb  5 2007 Joe Orton <jorton@redhat.com> 1:1.4.11-4
- fix Group, mark pear.conf noreplace (#226295)

* Mon Feb  5 2007 Joe Orton <jorton@redhat.com> 1:1.4.11-3
- use BuildArch not BuildArchitectures (#226925)
- fix to use preferred BuildRoot (#226925)
- strip more buildroot-relative paths from *.reg
- force correct gpg path in default pear.conf

* Thu Jan  4 2007 Joe Orton <jorton@redhat.com> 1:1.4.11-2
- update to 1.4.11

* Fri Jul 14 2006 Joe Orton <jorton@redhat.com> 1:1.4.9-4
- update to XML_RPC-1.5.0
- really package macros.pear

* Thu Jul 13 2006 Joe Orton <jorton@redhat.com> 1:1.4.9-3
- require php-cli
- add /etc/rpm/macros.pear (Christopher Stone)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.4.9-2.1
- rebuild

* Mon May  8 2006 Joe Orton <jorton@redhat.com> 1:1.4.9-2
- update to 1.4.9 (thanks to Remi Collet, #183359)
- package /usr/share/pear/.pkgxml (#190252)
- update to XML_RPC-1.4.8
- bundle the v3.0 LICENSE file

* Tue Feb 28 2006 Joe Orton <jorton@redhat.com> 1:1.4.6-2
- set cache_dir directory, own /var/cache/php-pear

* Mon Jan 30 2006 Joe Orton <jorton@redhat.com> 1:1.4.6-1
- update to 1.4.6
- require php >= 5.1.0 (#178821)

* Fri Dec 30 2005 Tim Jackson <tim@timj.co.uk> 1:1.4.5-6
- Patches to fix "pear makerpm"

* Wed Dec 14 2005 Joe Orton <jorton@redhat.com> 1:1.4.5-5
- set default sig_keydir to /etc/pearkeys
- remove ext_dir setting from /etc/pear.conf (#175673)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Dec  6 2005 Joe Orton <jorton@redhat.com> 1:1.4.5-4
- fix virtual provide for PEAR package (#175074)

* Sun Dec  4 2005 Joe Orton <jorton@redhat.com> 1:1.4.5-3
- fix /usr/bin/{pecl,peardev} (#174882)

* Thu Dec  1 2005 Joe Orton <jorton@redhat.com> 1:1.4.5-2
- add virtual provides (#173806)

* Wed Nov 23 2005 Joe Orton <jorton@redhat.com> 1.4.5-1
- initial build (Epoch: 1 to allow upgrade from php-pear-5.x)
