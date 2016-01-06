%define         debug_package %{nil}
%define         __vendor_perl %{_libdir}/perl5/vendor_perl
%define         __pkg_config_dir %{_libdir}/pkgconfig
%define         __site_packages %{_libdir}/python2.7/site-packages
%define         __easyprof_dir  %{_datarootdir}/%{name}/easyprof
%define         __extra_profiles_dir %{_datarootdir}/%{name}/extra-profiles
%define         __workdir /var/lib/%{name}

Name:           apparmor
Version:        2.10
Release:        1%{?dist}
Summary:        Linux application security framework - mandatory access control for programs

Group:          AppArmor
License:        GPL
URL:            http://wiki.apparmor.net
#Source0:	      https://launchpad.net/%{name}/%{version}/%{version}/+download/%{name}-%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Source1:        apparmor_load.sh
Source2:        apparmor_unload.sh
Source3:        apparmor.service

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  pam-devel
BuildRequires:  python-devel
BuildRequires:  perl-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libstdc++-static
BuildRequires:  bison
BuildRequires:	bzr
BuildRequires:  flex
BuildRequires:  swig
BuildRequires:  perl-gettext
BuildRequires:  perl-podlators
BuildRequires:  perl-Pod-Checker
BuildRequires:  perl-Test-Harness
BuildRequires:  perl-RPC-XML
BuildRequires:  perl-Pod-MinimumVersion
BuildRequires:  audit
Requires:       audit
Requires:       perl-TermReadKey
Requires:       perl-File-Tail

%description
AppArmor is an effective and easy-to-use Linux application security system
AppArmor proactively protects the operating system and applications from external or
internal threats, even zero-day attacks, by enforcing good behavior and 
preventing even unknown application flaws from being exploited.
AppArmor security policies completely define what system resources individual 
applications can access, and with what privileges. A number of default policies are 
included with AppArmor, and using a combination of advanced static analysis and 
learning-based tools, AppArmor policies for even very complex applications 
can be deployed successfully in a matter of hours.

%prep
%setup -q


%build
## Building libapparmor
pushd %{_builddir}/%{name}-%{version}/libraries/libapparmor
NOCONFIGURE=1 ./autogen.sh
./configure --prefix=/usr --sbindir=/usr/bin --with-perl --with-python
make
popd

## Building Parser library
pushd %{_builddir}/%{name}-%{version}/parser
sed -i -e 's/pdflatex/true/g' Makefile
make
popd

## Buildding AppArmor utils
pushd %{_builddir}/%{name}-%{version}/utils
make
popd

## Building AppArmor profiles
pushd %{_builddir}/%{name}-%{version}/profiles
make
popd

## Building pam-apparmor module
pushd %{_builddir}/%{name}-%{version}/changehat/pam_apparmor
make
popd

## Building vim plugin
pushd %{_builddir}/%{name}-%{version}/utils/vim
make -j1
popd

%install
mkdir -p %{buildroot}/%{_unitdir}
install -m 0644 %{SOURCE3} %{buildroot}/%{_unitdir}

## apparmor-libapparmor
pushd %{_builddir}/%{name}-%{version}/libraries/libapparmor
make install DESTDIR=%{buildroot}
install -D -m644 swig/perl/LibAppArmor.pm %{buildroot}/%{_libdir}/perl5/vendor_perl
popd

## apparmor-parser
pushd %{_builddir}/%{name}-%{version}/parser
make install DESTDIR=%{buildroot}
mv %{buildroot}/lib %{buildroot}/usr/lib
mv %{buildroot}/sbin %{buildroot}/usr/bin
popd

## apparmor-utils
pushd %{_builddir}/%{name}-%{version}/utils
make install DESTDIR=%{buildroot} BINDIR=%{buildroot}/%{_bindir}
install -D -m755 %{SOURCE1} %{buildroot}/%{_bindir}
install -D -m755 %{SOURCE2} %{buildroot}/%{_bindir}
popd

## apparmor-profiles
pushd %{_builddir}/%{name}-%{version}/profiles
make install DESTDIR=%{buildroot}
popd

## pam-apparmor
pushd %{_builddir}/%{name}-%{version}/changehat/pam_apparmor
make install DESTDIR=%{buildroot}
install -D -m644 README %{buildroot}/%{_defaultdocdir}/%{name}/README.pam_%{name}
popd

## vim pugin
mkdir -p %{buildroot}/%{_datarootdir}/vim/vimfiles/syntax
pushd %{_builddir}/%{name}-%{version}/utils/vim
install -m 0644 %{name}.vim %{buildroot}/%{_datarootdir}/vim/vimfiles/syntax
popd

%files
%doc
%dir %{_sysconfdir}/%{name}.d
%{_sysconfdir}/%{name}/easyprof.conf
%{_sysconfdir}/%{name}/logprof.conf
%{_sysconfdir}/%{name}/notify.conf
%{_sysconfdir}/%{name}/parser.conf
%{_sysconfdir}/%{name}/severity.db
%{_sysconfdir}/%{name}/subdomain.conf

%{_bindir}/aa-audit
%{_bindir}/aa-autodep
%{_bindir}/aa-cleanprof
%{_bindir}/aa-complain
%{_bindir}/aa-decode
%{_bindir}/aa-disable
%{_bindir}/aa-easyprof
%{_bindir}/aa-enforce
%{_bindir}/aa-exec
%{_bindir}/aa-genprof
%{_bindir}/aa-logprof
%{_bindir}/aa-mergeprof
%{_bindir}/aa-notify
%{_bindir}/aa-status
%{_bindir}/aa-unconfined
%{_bindir}/%{name}_load.sh
%{_bindir}/%{name}_parser
%{_bindir}/%{name}_status
%{_bindir}/%{name}_unload.sh
%{_bindir}/rc%{name}
%{_bindir}/rcsubdomain

/lib/security/pam_%{name}.so

%{_libdir}/perl5/perllocal.pod
%{_libdir}/lib%{name}.a
%{_libdir}/lib%{name}.la
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}.so.1
%{_libdir}/lib%{name}.so.1.3.0

%{__vendor_perl}/LibAppArmor.pm

%dir %{__vendor_perl}/auto/LibAppArmor
%{__vendor_perl}/auto/LibAppArmor/.packlist
%{__vendor_perl}/auto/LibAppArmor/LibAppArmor.bs
%{__vendor_perl}/auto/LibAppArmor/LibAppArmor.so

%{__pkg_config_dir}/lib%{name}.pc

%dir %{__site_packages}/%{name}
%{__site_packages}/%{name}/*

%dir %{__site_packages}/LibAppArmor
%{__site_packages}/LibAppArmor/*

%{__site_packages}/%{name}-%{version}-py2.7.egg-info
%{__site_packages}/LibAppArmor-2.10-py2.7.egg-info

%dir %{_datarootdir}/%{name}
%{_datarootdir}/%{name}/%{name}.vim

%dir %{_datarootdir}/vim/vimfiles/syntax
%{_datarootdir}/vim/vimfiles/syntax/%{name}.vim

%dir %{_datarootdir}/%{name}/easyprof/policygroups
%{_datarootdir}/%{name}/easyprof/policygroups/opt-application
%{_datarootdir}/%{name}/easyprof/policygroups/user-application

%dir %{_datarootdir}/%{name}/easyprof/templates
%{_datarootdir}/%{name}/easyprof/templates/default
%{_datarootdir}/%{name}/easyprof/templates/sandbox
%{_datarootdir}/%{name}/easyprof/templates/sandbox-x
%{_datarootdir}/%{name}/easyprof/templates/user-application

%dir %{_includedir}/aalogparse
%{_includedir}/aalogparse/aalogparse.h

%dir %{_includedir}/sys
%{_includedir}/sys/%{name}.h
%{_includedir}/sys/%{name}_private.h

%dir %{__extra_profiles_dir}
%{__extra_profiles_dir}/*

%dir %{_libdir}/lib/%{name}
%{_libdir}/lib/%{name}/rc.%{name}.functions

%dir %{_defaultdocdir}/%{name}
%{_defaultdocdir}/%{name}/README.pam_apparmor

%dir %{__workdir}

%{_datarootdir}/locale/*
%{_datarootdir}/man/*

%{_sysconfdir}/%{name}.d/*
%{_unitdir}/%{name}.service

%exclude %{_sysconfdir}/init.d

%changelog
* Sun Dec 13 2015 <vitvelg@gmail.com> - 2.10-1
- initial build
