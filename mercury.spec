# TODO: add mercury backend for gcc

%define		_gcc_ver	%(%{__cc} -dumpversion | cut -b 1)

Summary:	The logic/functional programming language Mercury
Name:		mercury
Version:	0.10.1
Release:	1
License:	GPL and LGPL
Group:		Development/Languages
Source0:	ftp://ftp.mercury.cs.mu.oz.au/pub/mercury/%{name}-compiler-%{version}.tar.gz
Patch0:		%{name}-tinfo.patch
URL:		http://www.cs.mu.oz.au/mercury/
BuildRequires:	readline-devel
BuildRequires:	autoconf
%if %{_gcc_ver} == 3
BuildRequires:  gcc2-c++
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# needs to be built by gcc 2.x
%if %{_gcc_ver} == 3
%define         __cc		gcc2
%define         __cxx		g++2
%ifarch athlon
%define         rpmcflags	-O2 -march=i686
%endif
%endif

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

%prep
%setup -q -n %{name}-compiler-%{version}
%patch0 -p1

%build
install /usr/share/automake/config.* .
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


%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc README README.Linux NEWS RELEASE_NOTES WORK_IN_PROGRESS HISTORY LIMITATIONS
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/mercury
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

%clean
rm -rf $RPM_BUILD_ROOT
