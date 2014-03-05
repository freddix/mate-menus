Summary:	Implementation of the draft Desktop Menu Specification
Name:		mate-menus
Version:	1.8.0
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz
# Source0-md5:	360bba4f4f2d0f24ebebb2c8517d996a
Patch0:		%{name}-layout.patch
Patch1:		%{name}-nokde.patch
URL:		http://www.gnome.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	glib-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkg-config
BuildRequires:	python-devel
Provides:	xdg-menus
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The package contains an implementation of the draft "Desktop Menu
Specification" from freedesktop.org:
http://www.freedesktop.org/Standards/menu-spec

%package libs
Summary:	mate-menu library
Group:		Libraries

%description libs
mate-menu library.

%package devel
Summary:	Header files of mate-menus library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Headers for mate-menus library.

%package -n python-matemenu
Summary:	Python binding for mate-menu library
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}
%pyrequires_eq	python-libs
Requires:	xdg-menus

%description -n python-matemenu
Python binding for mate-menus library.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# kill mate-common deps
%{__sed} -i -e '/MATE_COMPILE_WARNINGS.*/d'	\
    -i -e '/MATE_MAINTAINER_MODE_DEFINES/d'	\
    -i -e '/MATE_COMMON_INIT/d'			\
    -i -e '/MATE_CXX_WARNINGS.*/d'		\
    -i -e '/MATE_DEBUG_CHECK/d' configure.ac

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-silent-rules	\
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	directorydir=%{_datadir}/desktop-directories

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/*.la
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,crh,dv,en@shaw,gn,ha,ig,io,ps}

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%{_datadir}/desktop-directories/mate*.directory
%{_sysconfdir}/xdg/menus/mate-*.menu

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libmate-menu.so.?
%attr(755,root,root) %{_libdir}/libmate-menu.so.*.*.*
%{_libdir}/girepository-1.0/MateMenu-2.0.typelib

%files devel
%attr(755,root,root) %{_libdir}/lib*.so
%{_pkgconfigdir}/*.pc
%{_includedir}/*
%{_datadir}/gir-1.0/MateMenu-2.0.gir

%files -n python-matemenu
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/matemenu.so

