#
# TODO:
# - .init
#
Summary:	Domain Name Relay Daemon
Summary(pl):	-
Name:		dnrd
Version:	2.20.1
Release:	0.1
License:	GPL v2
Group:		Applications
Source0:	http://dl.sourceforge.net/dnrd/%{name}-%{version}.tar.gz
# Source0-md5:	cbd3657617ecb92e0fd19c5c9f1ccfd7
URL:		http://dnrd.sourceforge.net/
#BuildRequires:	rpmbuild(macros) >= 1.228
#Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Domain Name Relay Daemon is a caching, forwarding DNS proxy server.
Most useful on vpn or dialup firewalls but it is also a nice DNS cache
for minor networks and workstations.

%description -l pl

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
> $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/master
> $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/blacklist

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README doc/README-cache doc/README-master doc/master.sample
%{_mandir}/man8/*
%attr(755,root,root) %{_sbindir}/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*
#%%attr(754,root,root) /etc/rc.d/init.d/%{name}
#%%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
