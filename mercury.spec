# TODO:
# - add mercury backend for gcc
Summary:	The logic/functional programming language Mercury
Summary(pl):	Logiczno-funkcyjny jêzyk programowania Mercury
Name:		mercury
Version:	0.11.0
Release:	1
License:	GPL and LGPL
Group:		Development/Languages
Source0:	http://www.cs.mu.oz.au/research/mercury/download/files/%{name}-compiler-%{version}.tar.gz
# Source0-md5:	ccef86b46ffc043bdcd3a4775d084446
Patch0:		%{name}-tinfo.patch
Patch1:		%{name}-gcc33.patch
Patch2:		%{name}-nolibs.patch
URL:		http://www.cs.mu.oz.au/mercury/
BuildRequires:	autoconf
BuildRequires:	automake
# can use gcc 2.95.x, 3.2.x or 3.3.2+ (3.0 and 3.3.[01] are broken)
BuildRequires:	libstdc++-devel >= 5:3.3.2
BuildRequires:	readline-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mercury is a modern logic/functional programming language, which
combines the clarity and expressiveness of declarative programming
with advanced static analysis and error detection features. Its highly
optimized execution algorithm delivers efficiency far in excess of
existing logic programming systems, and close to conventional
programming systems. Mercury addresses the problems of large-scale
program development, allowing modularity, separate compilation, and
numerous optimization/time trade-offs.

This package includes the compiler, profiler, debugger, documentation,
etc. It does NOT include the "extras" distribution; that is available
from <http://www.cs.mu.oz.au/mercury/download/release.html>.

%description -l pl
Mercury jest nowoczesnym, logiczno-funkcyjnym jêzykiem programowania,
który ³±czy jasno¶æ i pe³niê wyrazu programowania deklaracyjnego z
rozszerzonymi mo¿liwo¶ciami statycznej analizy i wykrywania b³êdów.
Bardzo zoptymalizowany algorytm wykonywania daje o wiele wiêksz±
wydajno¶æ ni¿ istniej±ce systemy programowania logicznego, i prawie
tak du¿±, jak konwencjonalne systemy. Mercury wychodzi naprzeciw
problemom tworzenia oprogramowania na du¿± skalê, pozwalaj±c na
modularno¶æ, oddzieln± kompilacjê i liczne optymalizacje.

Ten pakiet zawiera kompilator, profiler, debugger, dokumentacjê itp.
Nie zawiera zestawu "extras", który jest dostêpny z
<http://www.cs.mu.oz.au/mercury/download/release.html>.

%prep
%setup -q -n %{name}-compiler-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%{__perl} -pi -e 's/OPT_OPTS="-O2.*"/OPT_OPTS="%{rpmcflags}%{!?debug: -fomit-frame-pointer}"/' scripts/mgnuc.in

%build
install %{_datadir}/automake/config.* .
%{__aclocal}
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL_PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	INSTALL_MAN_DIR=$RPM_BUILD_ROOT%{_mandir} \
	INSTALL_INFO_DIR=$RPM_BUILD_ROOT%{_infodir}

install -d $RPM_BUILD_ROOT%{_examplesdir}
cp -a samples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

find $RPM_BUILD_ROOT%{_examplesdir} -name "CVS" -type "d" | xargs rm -rf

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc README README.Linux NEWS RELEASE_NOTES WORK_IN_PROGRESS HISTORY LIMITATIONS
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/mercury
%dir %{_libdir}/mercury/bin
%dir %{_libdir}/mercury/bin/*
%attr(755,root,root) %{_libdir}/mercury/bin/*/*
%{_libdir}/mercury/elisp
%{_libdir}/mercury/inc
%{_libdir}/mercury/ints
%{_libdir}/mercury/lib
%{_libdir}/mercury/mdb
%{_libdir}/mercury/mmake
%{_libdir}/mercury/modules
%{_examplesdir}/%{name}-%{version}
%{_mandir}/man*/*
%{_infodir}/*.info*
