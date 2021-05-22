%bcond_without snmp
%bcond_without vrrp
%bcond_without sha1
%bcond_with profile
%bcond_without nftables
%bcond_with debug

%global _hardened_build 1

Name:		keepalived
Version:	2.0.20
Release:	17
Summary:	High Availability monitor built upon LVS, VRRP and service pollers
License:	GPLv2+
URL:		http://www.keepalived.org/
Source0:	http://www.keepalived.org/software/keepalived-%{version}.tar.gz
Source1: 	keepalived.service

BuildRequires:	net-snmp-devel gcc systemd-units openssl-devel libnl3-devel
BuildRequires:  ipset-devel iptables-devel libnfnetlink-devel libnftnl-devel
Requires:       %{name}-help = %{version}-%{release}
%{?systemd requires}

%description
Keeplived is a routing software written in C. The main goal of this project 
is to provide simple and robust facilities for loadbalancing and 
high-availability to Linux system and Linux based infrastructures. 
Loadbalancing framework relies on well-known and widely used Linux Virtual 
Server (IPVS) kernel module providing Layer4 loadbalancing. Keepalived 
implements a set of checkers to dynamically and adaptively maintain and 
manage loadbalanced server pool according their health. On the other hand 
high-availability is achieved by VRRP protocol. VRRP is a fundamental brick 
for router failover. In addition, Keepalived implements a set of hooks to 
the VRRP finite state machine providing low-level and high-speed protocol 
interactions. In order to offer fastest network failure detection, Keepalived 
implements BFD protocol. VRRP state transition can take into account BFD hint 
to drive fast state transition. Keepalived frameworks can be used independently 
or all together to provide resilient infrastructures.

%package_help

%prep
%autosetup -n %{name}-%{version}

%build
%configure  %{?with_debug:--enable-debug}  %{?with_profile:--enable-profile} \
            %{!?with_vrrp:--disable-vrrp} %{?with_sha1:--enable-sha1} \
	    --with-init=systemd %{!?with_vrrp:--disable-vrrp} \
            %{?with_nftables:--enable-nftables --disable-iptables --disable-ipset} \
	    %{?with_snmp:--enable-snmp --enable-snmp-rfc} \
            
%make_build STRIP=/bin/true

%install
%make_install 
pushd %{buildroot}
rm -rf .%{_initrddir}/
rm -rf .%{_sysconfdir}/keepalived/samples/
popd

install -d -m 0755 %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/keepalived.service
install -Dd -m 0755 %{buildroot}%{_libexecdir}/keepalived

%post
%systemd_post keepalived.service

%preun
%systemd_preun keepalived.service

%postun
%systemd_postun_with_restart keepalived.service

%files
%defattr(-,root,root)
%doc README 
%license COPYING
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/sysconfig/keepalived
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/keepalived/keepalived.conf
%attr(0755,root,root) %{_sbindir}/keepalived
%dir %{_sysconfdir}/keepalived/
%dir %{_libexecdir}/keepalived/
%{_bindir}/genhash
%{_datadir}/snmp/mibs/*
%{_unitdir}/keepalived.service

%files		help
%defattr(-,root,root)
%doc AUTHOR ChangeLog TODO CONTRIBUTORS 
%{_mandir}/man*

%changelog
* Sat May 22 2021 kwb0523<kwb0523@163.com> - 2.0.20-17
- rebuild keepalived

* Fri Nov 06 2020 leiju<leiju4@huawei.com> - 2.0.20-4
- Add Requires keepalived-help into keepalived

* Tue Aug 18 2020 smileknife<jackshan2010@aliyun.com> - 2.0.20-3
- update release for rebuilding

* Fri  21 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.0.20-2
- Package init
