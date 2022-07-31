Name:          tpm2-tss
Version:       3.1.0
Release:       3%{?dist}
Summary:       TPM2.0 Software Stack

# The entire source code is under BSD except implementation.h and tpmb.h which
# is under TCGL(Trusted Computing Group License).
License:       BSD and TCGL
URL:           https://github.com/tpm2-software/tpm2-tss
Source0:       https://github.com/tpm2-software/tpm2-tss/releases/download/%{version}/%{name}-%{version}.tar.gz
# doxygen crash
Patch0:        tpm2-tss-3.0.0-doxygen.patch

%global udevrules_prefix 60-

BuildRequires: make
BuildRequires: autoconf-archive
BuildRequires: doxygen
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: json-c-devel
BuildRequires: libcurl-devel
BuildRequires: libgcrypt-devel
BuildRequires: libtool
BuildRequires: openssl-devel
BuildRequires: pkgconfig
BuildRequires: systemd
Requires(pre): shadow-utils

%description
tpm2-tss is a software stack supporting Trusted Platform Module(TPM) 2.0 system
APIs. It sits between TPM driver and applications, providing TPM2.0 specified
APIs for applications to access TPM module through kernel TPM drivers.

%prep
%autosetup -n %{name}-%{version}

%build
# Use built-in tpm-udev.rules, with specified installation path and prefix.
%configure --disable-static --disable-silent-rules \
           --with-udevrulesdir=%{_udevrulesdir} --with-udevrulesprefix=%{udevrules_prefix} \
           --with-runstatedir=%{_rundir} --with-tmpfilesdir=%{_tmpfilesdir} --with-sysusersdir=%{_sysusersdir}

# This is to fix Rpath errors. Taken from https://fedoraproject.org/wiki/Packaging:Guidelines#Removing_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
%make_install
find %{buildroot}%{_libdir} -type f -name \*.la -delete

%pre
getent group tss >/dev/null || groupadd -f -g 59 -r tss
if ! getent passwd tss >/dev/null ; then
    if ! getent passwd 59 >/dev/null ; then
      useradd -r -u 59 -g tss -d /dev/null -s /sbin/nologin -c "Account used for TPM access" tss
    else
      useradd -r -g tss -d /dev/null -s /sbin/nologin -c "Account used for TPM access" tss
    fi
fi
exit 0

%ldconfig_scriptlets

%files
%doc README.md CHANGELOG.md
%license LICENSE
%{_sysconfdir}/tpm2-tss/
%{_libdir}/libtss2-mu.so.0*
%{_libdir}/libtss2-sys.so.1*
%{_libdir}/libtss2-esys.so.0*
%{_libdir}/libtss2-fapi.so.1*
%{_libdir}/libtss2-rc.so.0*
%{_libdir}/libtss2-tctildr.so.0*
%{_libdir}/libtss2-tcti-cmd.so.0*
%{_libdir}/libtss2-tcti-device.so.0*
%{_libdir}/libtss2-tcti-mssim.so.0*
%{_libdir}/libtss2-tcti-pcap.so.0*
%{_libdir}/libtss2-tcti-swtpm.so.0*
%{_sysusersdir}/tpm2-tss.conf
%{_tmpfilesdir}/tpm2-tss-fapi.conf
%{_udevrulesdir}/%{udevrules_prefix}tpm-udev.rules

%package        devel
Summary:        Headers and libraries for building apps that use tpm2-tss 
Requires:       %{name}%{_isa} = %{version}-%{release}

%description    devel
This package contains headers and libraries required to build applications that
use tpm2-tss.

%files devel
%{_includedir}/tss2/
%{_libdir}/libtss2-mu.so
%{_libdir}/libtss2-sys.so
%{_libdir}/libtss2-esys.so
%{_libdir}/libtss2-fapi.so
%{_libdir}/libtss2-rc.so
%{_libdir}/libtss2-tctildr.so
%{_libdir}/libtss2-tcti-cmd.so
%{_libdir}/libtss2-tcti-device.so
%{_libdir}/libtss2-tcti-mssim.so
%{_libdir}/libtss2-tcti-pcap.so
%{_libdir}/libtss2-tcti-swtpm.so
%{_libdir}/pkgconfig/tss2-mu.pc
%{_libdir}/pkgconfig/tss2-sys.pc
%{_libdir}/pkgconfig/tss2-esys.pc
%{_libdir}/pkgconfig/tss2-fapi.pc
%{_libdir}/pkgconfig/tss2-rc.pc
%{_libdir}/pkgconfig/tss2-tctildr.pc
%{_libdir}/pkgconfig/tss2-tcti-cmd.pc
%{_libdir}/pkgconfig/tss2-tcti-device.pc
%{_libdir}/pkgconfig/tss2-tcti-mssim.pc
%{_libdir}/pkgconfig/tss2-tcti-pcap.pc
%{_libdir}/pkgconfig/tss2-tcti-swtpm.pc
%{_mandir}/man3/*.3.gz
%{_mandir}/man5/*.5.gz
%{_mandir}/man7/tss2*.7.gz


%changelog
* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jul 10 2021 Björn Esser <besser82@fedoraproject.org> - 3.1.0-2
- Rebuild for versioned symbols in json-c

* Mon May 17 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 3.1.0-1
- Update to 3.1.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 26 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 3.0.3-1
- Update to 3.0.2

* Sun Nov 22 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 3.0.2-1
- Update to 3.0.2

* Wed Sep 23 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 3.0.1-1
- Update to 3.0.1

* Tue Sep 15 2020 Than Ngo <than@redhat.com> - 3.0.0-4
- Fix doxygen crash

* Tue Sep 15 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 3.0.0-3
- Create tss user, if it doesn't exist, for userspace TPM access

* Fri Aug 07 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 3.0.0-2
- Install sysusers config in sysusersdir (rhbz #1834519)

* Wed Aug 05 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 3.0.0-1
- Update to 3.0.0

* Wed Aug 05 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2.4.2-1
- Update to 2.4.2

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu May 14 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2.4.1-1
- Update to 2.4.1

* Fri May 08 2020 Paul Wouters <pwouters@redhat.com> - 2.4.0-3
- Use proper rundir and tmpfiles macros so proper directories are used

* Tue Apr 21 2020 Björn Esser <besser82@fedoraproject.org> - 2.4.0-2
- Rebuild (json-c)

* Thu Mar 12 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2.4.0-1
- Update to 2.4.0 release

* Mon Feb 24 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2.3.3-1
- Update to 2.3.3 release

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 13 2019 Yunying Sun <yunying.sun@intel.com> - 2.3.2-1
- Update to 2.3.2 release

* Fri Sep 6 2019 Yunying Sun <yunying.sun@intel.com> - 2.3.1-1
- Update to 2.3.1 release

* Thu Aug 15 2019 Yunying Sun <yunying.sun@intel.com> - 2.3.0-1
- Update to 2.3.0 release

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 29 2019 Yunying Sun <yunying.sun@intel.com> - 2.2.3-1
- Update to 2.2.3 release

* Fri Mar 29 2019 Yunying Sun <yunying.sun@intel.com> - 2.2.2-1
- Update to 2.2.2 release

* Mon Mar  4 2019 Peter Robinson <pbrobinson@fedoraproject.org> 2.2.1-1
- Update to 2.2.1 release

* Wed Feb 06 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.2.0-1
- Update to 2.2.0 release

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 10 2018 Yunying Sun <yunying.sun@intel.com> - 2.1.0-1
- Update to 2.1.0 release

* Thu Aug 30 2018 Yunying Sun <yunying.sun@intel.com> - 2.0.1-1
- Update to 2.0.1 release

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 4 2018 Yunying Sun <yunying.sun@intel.com> - 2.0.0-2
- Re-enable ESAPI since gcrypt dependency is not an issue for Fedora
- Bump release version to 2.0.0-2

* Mon Jul 2 2018 Yunying Sun <yunying.sun@intel.com> - 2.0.0-1
- Update to 2.0.0 release (RHBZ#1508870)
- Remove patch file 60-tpm-udev.rules, use upstream tpm-udev.rules instead
- Disable ESAPI to fix build errors caused by dependency to libgcrypt 1.6.0
- Add scriptlet to fix Rpath errors
- Update file installation paths and names accordingly 

* Sun Mar 04 2018 Javier Martinez Canillas <javierm@redhat.com> - 1.4.0-1
- Update URLs to point to the new project location
- Add README.md CHANGELOG.md to %%files directive
- Update to 1.4.0 release (RHBZ#1508870)

* Fri Feb 23 2018 Javier Martinez Canillas <javierm@redhat.com> - 1.3.0-4
- Install udev rule for TPM character devices

* Wed Feb 21 2018 Javier Martinez Canillas <javierm@redhat.com> - 1.3.0-3
- Remove ExclusiveArch: %%{ix86} x86_64 directive

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.0-2
- Escape macros in %%changelog

* Fri Dec 08 2017 Javier Martinez Canillas <javierm@redhat.com> - 1.3.0-1
- Update to 1.3.0 release

* Wed Nov 29 2017 Javier Martinez Canillas <javierm@redhat.com> - 1.3.0-0.1.rc2
- Update to 1.3.0 release candidate 2 (RHBZ#1508870)
- Remove global pkg_prefix since now the upstream repo and package names match
- Update URLs to point to the new project location
- Remove -Wno-int-in-bool-context compiler flag since now upstream takes care
- Remove %%doc directive since README.md and CHANGELOG.md are not in the tarball
- Add patch to include a LICENSE since the generated tarball does not have it

* Mon Aug 28 2017 Javier Martinez Canillas <javierm@redhat.com> - 1.2.0-1
- Update to 1.2.0 release
- Use tpm2-tss instead of TPM2.0-TSS as prefix since project name changed
- Fix SPEC file access mode
- Include new man pages in %%files directive

* Fri Aug 18 2017 Javier Martinez Canillas <javierm@redhat.com> - 1.1.0-3
- Remove unneeded source tarballs (RHBZ#1482828)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Sun Yunying <yunying.sun@intel.com> - 1.1.0-1
- Update to 1.1.0 release

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Sun Yunying <yunying.sun@intel.com> - 1.0-2
- Remove global macro pkg_version to avoid duplicate of version
- Use ExclusiveArch instead of ExcludeArch
- Use less wildcard in %%files section to be more specific
- Add trailing slash at end of added directory in %%file section
- Remove autoconf/automake/pkgconfig(cmocka) from BuildRequires
- Increase release version to 2

* Fri Dec 2 2016 Sun Yunying <yunying.sun@intel.com> - 1.0-1
- Initial version of the package
