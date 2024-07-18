#
# Conditional build:
%bcond_without	perl		# Perl bindings
%bcond_without	python2		# CPython 2.x bindings
%bcond_without	python3		# CPython 3.x bindings
%bcond_without	ruby		# Ruby bindings
%bcond_without	static_libs	# static library
%bcond_with	sse2		# SSE2 instructions
%bcond_with	sse3		# SSE3 instructions
%bcond_with	ssse3		# SSSE3 instructions
%bcond_with	sse4		# SSE4 instructions
%bcond_with	sse41		# SSE4.1 instructions
%bcond_with	sse42		# SSE4.2 instructions
%bcond_with	sse4a		# SSE4a instructions
%bcond_with	popcnt		# POPCNT instructions
%bcond_with	bmi		# BMI instructions
%bcond_with	bmi2		# BMI2 instructions
#
%ifarch %{x8664} x32 pentium4
%define	with_sse2	1
%endif
Summary:	MARISA: Matching Algorithm with Recursively Implemented StorAge
Summary(pl.UTF-8):	MARISA - algorytm dopasowywania z rekurencyjnie zaimplementowanym trzymaniem danych
Name:		marisa
Version:	0.2.6
Release:	1
License:	BSD or LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/s-yata/marisa-trie/releases
Source0:	https://github.com/s-yata/marisa-trie/files/4832504/%{name}-%{version}.tar.gz
# Source0-md5:	695cecf504ced27ac13aa33d97d69dd0
URL:		https://github.com/s-yata/marisa-trie
BuildRequires:	autoconf >= 2.67
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
%{?with_perl:BuildRequires:	perl-devel >= 1:5.8.0}
%{?with_python2:BuildRequires:	python-devel >= 1:2.5}
%{?with_python3:BuildRequires:	python3-devel >= 1:3.2}
%{?with_ruby:BuildRequires:	ruby-devel}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.745
%{?with_perl:BuildRequires:	swig-perl}
%if %{with python2} || %{with python3}
BuildRequires:	swig-python
%endif
%{?with_ruby:BuildRequires:	swig-ruby}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Matching Algorithm with Recursively Implemented StorAge (MARISA) is a
static and space-efficient trie data structure. And libmarisa is a C++
library to provide an implementation of MARISA. Also, the package of
libmarisa contains a set of command line tools for building and
operating a MARISA-based dictionary.

A MARISA-based dictionary supports not only lookup but also reverse
lookup, common prefix search and predictive search.

%description -l pl.UTF-8
Matching Algorithm with Recursively Implemented StorAge (MARISA) to
statyczna, wydajna pod względem zajętości struktura danych trie.
libmarisa to biblioteka C++ zapewniająca implementację struktury
MARISA. Pakiet ten zawiera także zestaw narzędzi linii poleceń do
budowania i operowania na słownikach opartych na tej strukturze.

Słownik MARISA obsługuje nie tylko wyszukiwanie, ale także
wyszukiwanie odwrotne, wyszukiwanie wspólnych prefiksów i wyszukiwanie
przewidywane.

%package devel
Summary:	Header files for MARISA library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki MARISA
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for MARISA library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki MARISA.

%package static
Summary:	Static MARISA library
Summary(pl.UTF-8):	Statyczna biblioteka MARISA
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static MARISA library.

%description static -l pl.UTF-8
Statyczna biblioteka MARISA.

%package -n perl-marisa
Summary:	Perl binding for MARISA library
Summary(pl.UTF-8):	Wiązania Perla do biblioteki MARISA
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}-%{release}

%description -n perl-marisa
Perl binding for MARISA library.

%description -n perl-marisa -l pl.UTF-8
Wiązania Perla do biblioteki MARISA.

%package -n python-marisa
Summary:	Python 2 binding for MARISA library
Summary(pl.UTF-8):	Wiązania Pythona 2 do biblioteki MARISA
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-marisa
Python 2 binding for MARISA library.

%description -n python-marisa -l pl.UTF-8
Wiązania Pythona 2 do biblioteki MARISA.

%package -n python3-marisa
Summary:	Python 3 binding for MARISA library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki MARISA
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-marisa
Python 3 binding for MARISA library.

%description -n python3-marisa -l pl.UTF-8
Wiązania Pythona 3 do biblioteki MARISA.

%package -n ruby-marisa
Summary:	Ruby binding for MARISA library
Summary(pl.UTF-8):	Wiązania języka Ruby do biblioteki MARISA
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description -n ruby-marisa
Ruby binding for MARISA library.

%description -n ruby-marisa -l pl.UTF-8
Wiązania języka Ruby do biblioteki MARISA.

%prep
%setup -q -n %{name}-trie-%{version}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	%{?with_bmi:--enable-bmi} \
	%{?with_bmi2:--enable-bmi2} \
	%{?with_popcnt:--enable-popcnt} \
	%{?with_sse2:--enable-sse2} \
	%{?with_sse3:--enable-sse3} \
	%{?with_ssse3:--enable-ssse3} \
	%{?with_sse4:--enable-sse4} \
	%{?with_sse41:--enable-sse4.1} \
	%{?with_sse42:--enable-sse4.2} \
	%{?with_sse4a:--enable-sse4a} \
	%{!?with_static_libs:--disable-static}

%{__make}

TOP=$(pwd)

%if %{with perl}
%{__make} -C bindings swig-perl
cd bindings/perl
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor \
	INC="-I${TOP}/include" \
	LIBS="-L${TOP}/lib/marisa/.libs -lmarisa"

%{__make}
cd ../..
%endif

%if %{with python2} || %{with python3}
%{__make} -C bindings swig-python
%endif
%if %{with python2}
cd bindings/python
%py_build build_ext \
	--include-dirs="${TOP}/include" \
	--library-dirs="${TOP}/lib/%{name}/.libs"
cd ../..
%endif

%if %{with python3}
cd bindings/python
%py3_build build_ext \
	--include-dirs="${TOP}/include" \
	--library-dirs="${TOP}/lib/%{name}/.libs"
cd ../..
%endif

%if %{with ruby}
%{__make} -C bindings swig-ruby
cd bindings/ruby
%{__ruby} extconf.rb \
	--with-opt-include="${TOP}/include" \
	--with-opt-lib="${TOP}/lib/%{name}/.libs" \
	--vendor

%{__make}
cd ../..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmarisa.la

%if %{with perl}
%{__make} -C bindings/perl pure_install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/{benchmark,sample}.pl
%endif

%if %{with python2}
cd bindings/python
%py_install

%py_postclean
cd ../..
%endif

%if %{with python3}
cd bindings/python
%py3_install
cd ../..
%endif

%if %{with ruby}
install -d $RPM_BUILD_ROOT%{ruby_vendorarchdir}
%{__make} -C bindings/ruby install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING.md README.md docs/{readme.en.html,style.css}
%lang(ja) %doc docs/readme.ja.html
%attr(755,root,root) %{_bindir}/marisa-*
%attr(755,root,root) %{_libdir}/libmarisa.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmarisa.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmarisa.so
%{_includedir}/marisa
%{_includedir}/marisa.h
%{_pkgconfigdir}/marisa.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libmarisa.a
%endif

%if %{with perl}
%files -n perl-marisa
%defattr(644,root,root,755)
%{perl_vendorarch}/marisa.pm
%dir %{perl_vendorarch}/auto/marisa
%attr(755,root,root) %{perl_vendorarch}/auto/marisa/marisa.so
%endif

%if %{with python2}
%files -n python-marisa
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_marisa.so
%{py_sitedir}/marisa.py[co]
%{py_sitedir}/marisa-0.0.0-py*.egg-info
%endif

%if %{with python3}
%files -n python3-marisa
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/_marisa.cpython-*.so
%{py3_sitedir}/marisa.py
%{py3_sitedir}/__pycache__/marisa.cpython-*.py[co]
%{py3_sitedir}/marisa-0.0.0-py*.egg-info
%endif

%if %{with ruby}
%files -n ruby-marisa
%defattr(644,root,root,755)
%attr(755,root,root) %{ruby_vendorarchdir}/marisa.so
%endif
