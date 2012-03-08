# Use rpmbuild --without gcj to disable native bits
%define with_gcj %{!?_without_gcj:1}%{?_without_gcj:0}

Name: pentaho-reporting-flow-engine
Version: 0.9.2
Release: 5.OOo31%{?dist}
Summary: Pentaho Flow Reporting Engine
License: LGPLv2+
Epoch: 1
Group: System Environment/Libraries
Source: http://downloads.sourceforge.net/jfreereport/flow-engine-%{version}-OOo31.zip
URL: http://reporting.pentaho.org/
BuildRequires: ant, java-devel, jpackage-utils, libbase, jcommon-serializer
BuildRequires: libloader, libfonts, pentaho-libxml, xml-commons-apis
BuildRequires: librepository, sac, flute, liblayout, libformula
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: java, jpackage-utils, libbase >= 1.0.0, libfonts >= 0.3.4
Requires: pentaho-libxml, libformula >= 0.1.18, librepository >= 0.1.6
Requires: sac, flute, liblayout >= 0.2.9, jcommon-serializer
%if %{with_gcj}
BuildRequires: java-gcj-compat-devel >= 1.0.31
Requires(post): java-gcj-compat >= 1.0.31
Requires(postun): java-gcj-compat >= 1.0.31
%else
BuildArch: noarch
%endif

%description
Pentaho Reporting Flow Engine is a free Java report library, formerly
known as 'JFreeReport'

%package javadoc
Summary: Javadoc for %{name}
Group: Development/Documentation
Requires: %{name} = 1:%{version}-%{release}
Requires: jpackage-utils
%if %{with_gcj}
BuildArch: noarch
%endif

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -c
mkdir -p lib
find . -name "*.jar" -exec rm -f {} \;
build-jar-repository -s -p lib commons-logging-api libbase libloader \
    libfonts libxml jaxp libformula librepository sac flute liblayout \
    libserializer

%build
ant jar javadoc

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/lib/flow-engine.jar $RPM_BUILD_ROOT%{_javadir}/flow-engine.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp build/api $RPM_BUILD_ROOT%{_javadocdir}/%{name}
%if %{with_gcj}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%if %{with_gcj}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%postun
%if %{with_gcj}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(0644,root,root,0755)
%doc licence-LGPL.txt README.txt ChangeLog.txt
%{_javadir}/*.jar
%if %{with_gcj}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}

%changelog
* Fri Jul 24 2009 Caolan McNamara <caolanm@redhat.com> 0.9.2-5.OOo31
- make javadoc no-arch when building as arch-dependant aot

* Sun Mar 29 2009 Caolan McNamara <caolanm@redhat.com> 0.9.2-4.OOo31
- wrong num

* Sat Mar 28 2009 Caolan McNamara <caolanm@redhat.com> 0.9.2-3.OOo31
- tweak version

* Mon Mar 16 2009 Caolan McNamara <caolanm@redhat.com> 0.9.2-1
- OOo tuned version

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep 05 2008 Caolan McNamara <caolanm@redhat.com> 0.9.3-2
- wrong liblayout version required

* Wed May 07 2008 Caolan McNamara <caolanm@redhat.com> 0.9.3-1
- initial fedora import
