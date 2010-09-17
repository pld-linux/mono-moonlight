# TODO
# - find pld packages: rsvg2-sharp
# - Release tarballs: http://ftp.novell.com/pub/mono/sources/moon/
# - upstream 2.3 spec http://github.com/mono/moon/blob/moon/moon-2-3/moonlight.spec.in
# - debian 1.0 repo: http://git.debian.org/?p=pkg-mono/packages/moon.git
# - fedora 1.0.1 http://olea.org/paquetes-rpm/repoview/moonlight.html
# - ubuntu 2.3 https://launchpad.net/ubuntu/+source/moon/2.3-0ubuntu1
# - not compatible with our libunwind (missing demangle.h)
# - patch to be able to disable libunwind instead of BC
# - http://lists.xensource.com/archives/html/xen-devel/2009-05/msg00075.html
Summary:	Free Software clone of Silverlight
Name:		mono-moonlight
Version:	2.3
Release:	0.1
License:	LGPL v2, MIT License (or similar), MS-PL
Group:		X11/Applications/Multimedia
URL:		http://www.mono-project.com/Moonlight
Source0:	http://ftp.novell.com/pub/mono/sources/moon/%{version}/moonlight-%{version}.tar.bz2
# Source0-md5:	164c4a5068f85244a0019ce49a6ee629
Source1:	http://ftp.novell.com/pub/mono/sources/moon/%{version}/mono-2.6.1.tar.bz2
# Source1-md5:	ad1286a66e802bf0be01cc09f433db8f
Source2:	http://ftp.novell.com/pub/mono/sources/moon/%{version}/mono-basic-2.6.tar.bz2
# Source2-md5:	172b70b30f58bf00834db223ab8d620e
Patch0:		minizip.patch
Patch1:		moon_fix_gdk_pointer_size.patch
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	cairo-devel >= 1.8.4
BuildRequires:	curl-devel
BuildRequires:	dotnet-gnome-desktop-sharp-devel
BuildRequires:	dotnet-gtk-sharp2
BuildRequires:	dotnet-gtk-sharp2-devel
BuildRequires:	expat-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	minizip-devel
BuildRequires:	mono-compat-links
BuildRequires:	mono-csharp
BuildRequires:	mono-devel >= 2.6
BuildRequires:	mono-monodoc
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel
BuildRequires:	rpmbuild(macros) >= 1.357
#BuildRequires:	rsvg2-sharp
#BuildRequires:	wnck-sharp
BuildRequires:	xulrunner-devel
BuildRequires:	zip
BuildConflicts:	libunwind-devel
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Moonlight is an open source implementation of Microsoft Silverlight
for Unix systems.

%package -n libmoon
Summary:	Novell Moonlight
License:	LGPL v2
Group:		X11/Applications/Multimedia
Requires:	mono-core >= 2.6

%description -n libmoon
Moonlight is an open source implementation of Microsoft Silverlight
for Unix systems.

%package -n libmoon-devel
Summary:	Development files for libmoon
License:	LGPL v2
Group:		Libraries
Requires:	mono-devel >= 2.6

%description -n libmoon-devel
Development files for libmoon.

Moonlight is an open source implementation of Microsoft Silverlight
for Unix systems.

%package -n browser-plugin-moonlight
Summary:	Novell Moonlight Browser Plugin
License:	LGPL v2, MIT License (or similar), MS-PL
Group:		X11/Applications/Multimedia
Requires:	browser-plugins >= 2.0
Requires:	libmoon = %{version}-%{release}
Requires:	mono-core >= 2.6
Obsoletes:	mono-moonlight-plugin

%description -n browser-plugin-moonlight
Novell Moonlight Browser Plugin.

Moonlight is an open source implementation of Microsoft Silverlight
for Unix systems.

%package web-devel
Summary:	Development files for Moonlight Web
License:	MIT License (or similar), MS-PL
Group:		Development/Languages
Suggests:	%{name}-plugin = %{version}-%{release}

%description web-devel
Development files for creating Moonlight web applications.

Moonlight is an open source implementation of Microsoft Silverlight
for Unix systems.

%package desktop
Summary:	Mono bindings for Moonlight Desktop
License:	MIT License (or similar), MS-PL
Group:		X11/Applications/Multimedia
Requires:	libmoon = %{version}-%{release}

%description desktop
Mono bindings for Novell Moonlight.

Moonlight is an open source implementation of Microsoft Silverlight
for Unix systems.

%package desktop-devel
Summary:	Development files for Moonlight Desktop
License:	MIT License (or similar), MS-PL
Group:		Development/Languages
Requires:	%{name}-desktop = %{version}-%{release}
Requires:	dotnet-gtk-sharp2
Requires:	glib2-devel
Requires:	libmoon = %{version}-%{release}
Suggests:	%{name}-tools = %{version}-%{release}

%description desktop-devel
Development files for Moonlight Desktop.

Moonlight is an open source implementation of Microsoft Silverlight
for Unix systems.

%package tools
Summary:	Various tools for Novell Moonlight
License:	MIT License (or similar)
Group:		Development/Languages
Requires:	%{name}-desktop = %{version}-%{release}
Requires:	libmoon = %{version}-%{release}

%description tools
Various tools for Novell Moonlight.

Moonlight is an open source implementation of Microsoft Silverlight
for Unix systems.

%prep
%setup -q -n moonlight-%{version} -a1 -a2
%patch0 -p1
%patch1 -p1

mv mono-2.6.1 mono
mv mono-basic-2.6 mono-basic

rm -r pixman cairo src/zip curl

# force rebuild
rm -f configure

%build
topdir=$(pwd)
# build mono first
# The plugin requires a complete build of it's own mono
if [ ! -f mono.built ]; then
	cd mono
	# We have not determined which --enable-minimal options might be safe
	# so please do not use any of them
	./configure \
		--prefix=$topdir/install \
		--with-mcs-docs=no \
		--with-ikvm-native=no
	%{__make} -j1
	cd ..
	touch mono.built
fi

if [ ! -f configure ]; then
	%{__libtoolize}
	%{__aclocal} -I m4
	%{__autoconf}
	%{__automake}
fi
%configure \
	--enable-dependency-tracking \
	--without-testing \
	--without-performance \
	--without-examples \
	--with-system-minizip=yes \
	--with-alsa=yes \
	--with-cairo=system \
	--with-curl=system \
	--with-debug=no \
	--with-ff2=no \
	--with-ff3=yes \
	--with-ffmpeg=yes \
	--with-managed=no \
	--with-pulse-audio=yes \
	--with-pulseaudio=yes \
	--with-mcspath=$topdir/mono/mcs \
	--with-mono-basic-path=$topdir/mono-basic \

%{__make} -j1

# The next lines would build the XPI if we wanted it
# So that the xpi will pick up the custom libmono.so
#export PKG_CONFIG_PATH=%{_builddir}/install/lib/pkgconfig:${PKG_CONFIG_PATH}
#%{__make} user-plugin

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install -j1 \
	DESTDIR=$RPM_BUILD_ROOT

# Symlink the loader into browser-plugins for SUSE
install -d $RPM_BUILD_ROOT%{_browserpluginsdir}
ln -s %{_libdir}/moonlight/plugin/libmoonloader.so $RPM_BUILD_ROOT%{_browserpluginsdir}/libmoonloader.so

# We don't like nasty .la files
find $RPM_BUILD_ROOT -name '*.la' | xargs rm -v

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n libmoon -p /sbin/ldconfig
%postun	-n libmoon -p /sbin/ldconfig

%post -n browser-plugin-moonlight
%update_browser_plugins

%postun -n browser-plugin-moonlight
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%files -n libmoon
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSE NEWS README TODO
%attr(755,root,root) %{_libdir}/libmoon.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmoon.so.0

%files -n libmoon-devel
%defattr(644,root,root,755)
%{_libdir}/libmoon.so

%files -n browser-plugin-moonlight
%defattr(644,root,root,755)
%attr(755,root,root) %{_browserpluginsdir}/libmoonloader.so
%dir %{_libdir}/moonlight/plugin
%attr(755,root,root) %{_libdir}/moonlight/plugin/libmoonloader.so
%attr(755,root,root) %{_libdir}/moonlight/plugin/libmoonplugin.so
%attr(755,root,root) %{_libdir}/moonlight/plugin/libmoonplugin-curlbridge.so
%attr(755,root,root) %{_libdir}/moonlight/plugin/libmoonplugin-ff3bridge.so
%{_libdir}/moonlight/plugin/Microsoft.VisualBasic.dll*
%{_libdir}/moonlight/plugin/System.Core.dll*
%{_libdir}/moonlight/plugin/System.Net.dll*
%{_libdir}/moonlight/plugin/System.Runtime.Serialization.dll*
%{_libdir}/moonlight/plugin/System.ServiceModel.Web.dll*
%{_libdir}/moonlight/plugin/System.ServiceModel.dll*
%{_libdir}/moonlight/plugin/System.Windows.Browser.dll*
%{_libdir}/moonlight/plugin/System.Windows.dll*
%{_libdir}/moonlight/plugin/System.Xml.dll*
%{_libdir}/moonlight/plugin/System.dll*
%{_libdir}/moonlight/plugin/mscorlib.dll*

%files web-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/smcs
%dir %{_prefix}/lib/moonlight
%dir %{_prefix}/lib/moonlight/2.0-redist
%{_prefix}/lib/moonlight/2.0-redist/System.Windows.Controls.Data.dll*
%{_prefix}/lib/moonlight/2.0-redist/System.Windows.Controls.dll*
%{_prefix}/lib/moonlight/2.0-redist/System.Xml.Linq.dll*
%dir %{_prefix}/lib/moonlight/2.0
%{_prefix}/lib/moonlight/2.0/Microsoft.VisualBasic.dll*
%{_prefix}/lib/moonlight/2.0/Mono.CompilerServices.SymbolWriter.dll*
%{_prefix}/lib/moonlight/2.0/System.Core.dll*
%{_prefix}/lib/moonlight/2.0/System.Net.dll*
%{_prefix}/lib/moonlight/2.0/System.Runtime.Serialization.dll*
%{_prefix}/lib/moonlight/2.0/System.ServiceModel.Web.dll*
%{_prefix}/lib/moonlight/2.0/System.ServiceModel.dll*
%{_prefix}/lib/moonlight/2.0/System.Windows.Browser.dll*
%{_prefix}/lib/moonlight/2.0/System.Windows.dll*
%{_prefix}/lib/moonlight/2.0/System.Xml.dll*
%{_prefix}/lib/moonlight/2.0/System.dll*
%{_prefix}/lib/moonlight/2.0/mscorlib.dll*
%{_prefix}/lib/moonlight/2.0/respack.exe*
%{_prefix}/lib/moonlight/2.0/smcs
%{_prefix}/lib/moonlight/2.0/smcs.exe*
%{_prefix}/lib/moonlight/2.0/buildversion
%{_npkgconfigdir}/moonlight-web-2.0.pc

%files desktop
%defattr(644,root,root,755)
%{_prefix}/lib/mono/gac/Moon.Windows.Desktop
%{_prefix}/lib/mono/gac/Moonlight.Gtk
%{_prefix}/lib/mono/gac/System.Windows
%{_prefix}/lib/mono/gac/System.Windows.Browser
%{_prefix}/lib/mono/gac/System.Windows.Controls
%{_prefix}/lib/mono/gac/System.Windows.Controls.Data

%files desktop-devel
%defattr(644,root,root,755)
%dir %{_prefix}/lib/mono/moonlight
%{_prefix}/lib/mono/moonlight/Moon.Windows.Desktop.dll*
%{_prefix}/lib/mono/moonlight/System.Windows.Browser.dll*
%{_prefix}/lib/mono/moonlight/System.Windows.Controls.Data.dll*
%{_prefix}/lib/mono/moonlight/System.Windows.Controls.dll*
%{_prefix}/lib/mono/moonlight/System.Windows.dll*
%{_npkgconfigdir}/moonlight-desktop-2.0.pc
# It may make sense in the future to have a moonlight-gtk package
%{_prefix}/lib/mono/moonlight/Moonlight.Gtk.dll*
%{_prefix}/lib/monodoc/sources/moonlight-gtk.source
%{_prefix}/lib/monodoc/sources/moonlight-gtk.tree
%{_prefix}/lib/monodoc/sources/moonlight-gtk.zip
%{_npkgconfigdir}/moonlight-gtk-2.0.pc

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mopen
%attr(755,root,root) %{_bindir}/munxap
%attr(755,root,root) %{_bindir}/mxap
%attr(755,root,root) %{_bindir}/respack
%attr(755,root,root) %{_bindir}/sockpol
%attr(755,root,root) %{_bindir}/unrespack
%attr(755,root,root) %{_bindir}/xaml2html
%attr(755,root,root) %{_bindir}/xamlg
%{_mandir}/man1/mopen.1*
%{_mandir}/man1/mxap.1*
%{_mandir}/man1/respack.1*
%{_mandir}/man1/sockpol.1*
%{_mandir}/man1/svg2xaml.1*
%{_mandir}/man1/xamlg.1*
%dir %{_libdir}/moonlight
%{_libdir}/moonlight/mopen.exe*
%{_libdir}/moonlight/munxap.exe*
%{_libdir}/moonlight/mxap.exe*
%{_libdir}/moonlight/respack.exe*
%{_libdir}/moonlight/sockpol.exe*
%{_libdir}/moonlight/xaml2html.exe*
%{_libdir}/moonlight/xamlg.exe*
