# TODO
# - find pld packages: rsvg2-sharp wnck-sharp
Summary:	Novell Moonlight
Name:		mono-moonlight
Version:	3.0
Release:	0.1
License:	LGPL v2, MIT License (or similar), MS-PL
Group:		X11/Applications/Multimedia
URL:		http://go-mono.com/moonlight/
Source0:	http://download.github.com/mono-moon-moon-0.8-10290-g3ff068e.tar.gz
# Source0-md5:	24967265d29388c52df72135a9582b74
# Always required
BuildRequires:	cairo-devel >= 1.8.4
BuildRequires:	expat-devel
BuildRequires:	gtk+2-devel
BuildRequires:	libstdc++-devel
# Technically these two could be optional
BuildRequires:	alsa-lib-devel
BuildRequires:	dotnet-gtk-sharp2
BuildRequires:	mono-devel >= 2.6
BuildRequires:	mono-monodoc
BuildRequires:	pulseaudio-devel
#BuildRequires:	rsvg2-sharp
#BuildRequires:	wnck-sharp
BuildRequires:	xulrunner-devel
BuildRequires:	zip
# Required to build the desktop assemblies
# Required to build the plugin
BuildRequires:	ffmpeg-devel
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

%package plugin
Summary:	Novell Moonlight Browser Plugin
License:	LGPL v2, MIT License (or similar), MS-PL
Group:		X11/Applications/Multimedia
Requires:	libmoon = %{version}-%{release}
Requires:	mono-core >= 2.6

%description plugin
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
%setup -qc
mv mono-moon-*/* .

%build
# The plugin requires a complete build of it's own mono
cd ../mono-%{included_mono}
# We have not determined which --enable-minimal options might be safe
# so please do not use any of them
./configure \
	--prefix=%{_builddir}/install \
	--with-mcs-docs=no \
	--with-ikvm-native=no

# mono is not strictly -j safe
%{__make} -j1
# This gets installed in the build dir so that it gets wiped away
# and not installed on the system
%{__make} install
cd -

# And then we build moonlight
# Only needed when there are Makefile.am or configure.ac patches
#autoreconf -f -i -Wnone
%configure \
	--without-testing \
	--without-performance \
	--without-examples \
	--with-mcspath=%{_builddir}/mono-%{included_mono}/mcs \
	--with-mono-basic-path=%{_builddir}/mono-basic-%{included_mono} \
	--with-ffmpeg=%{with_ffmpeg} \
	--with-cairo=%{with_cairo}

%{__make}

# The next lines would build the XPI if we wanted it
# So that the xpi will pick up the custom libmono.so
#export PKG_CONFIG_PATH=%{_builddir}/install/lib/pkgconfig:${PKG_CONFIG_PATH}
#%{__make} user-plugin

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# Symlink the loader into browser-plugins for SUSE
install -d $RPM_BUILD_ROOT%{_libdir}/browser-plugins
ln -s %{_libdir}/moonlight/plugin/libmoonloader.so $RPM_BUILD_ROOT%{_libdir}/browser-plugins/libmoonloader.so

# We don't like nasty .la files
find $RPM_BUILD_ROOT -name '*.la' | xargs rm -v

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n libmoon -p /sbin/ldconfig
%postun	-n libmoon -p /sbin/ldconfig

%files -n libmoon
%defattr(644,root,root,755)
%doc AUTHORS COPYING README TODO NEWS
%attr(755,root,root) %{_libdir}/libmoon.so.*

%files -n libmoon-devel
%defattr(644,root,root,755)
%{_libdir}/libmoon.so

%files plugin
%defattr(644,root,root,755)
%dir %{_libdir}/moonlight/plugin
%{_libdir}/moonlight/plugin/libmoonloader.so
%{_libdir}/moonlight/plugin/libmoonplugin-ff3bridge.so
%{_libdir}/moonlight/plugin/libmoonplugin.so
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
# Is there somewhere we could put this that would be universal?
%{_libdir}/moonlight/plugin/mscorlib.dll*
%{_libdir}/browser-plugins/libmoonloader.so

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
%{_prefix}/lib/moonlight/2.0-redist/System.Windows.Controls.dll*
%{_prefix}/lib/moonlight/2.0-redist/System.Xml.Linq.dll*
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
%{_prefix}/lib/moonlight/2.0/smcs.exe*
%{_prefix}/lib/moonlight/2.0/buildversion
%{_datadir}/pkgconfig/moonlight-web-2.0.pc

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
# It may make sense in the future to have a moonlight-gtk package
%{_datadir}/pkgconfig/moonlight-desktop-2.0.pc
%{_prefix}/lib/mono/moonlight/Moonlight.Gtk.dll*
%{_prefix}/lib/monodoc/sources/moonlight-gtk.source
%{_prefix}/lib/monodoc/sources/moonlight-gtk.tree
%{_prefix}/lib/monodoc/sources/moonlight-gtk.zip
%{_datadir}/pkgconfig/moonlight-gtk-2.0.pc

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mopen
%{_bindir}/munxap %{_bindir}/mxap %{_bindir}/respack
%{_bindir}/sockpol %{_bindir}/unrespack %{_bindir}/xaml2html
%{_bindir}/xamlg %{_mandir}/man1/mopen.1%ext_man
%{_mandir}/man1/mxap.1%ext_man %{_mandir}/man1/respack.1%ext_man
%{_mandir}/man1/sockpol.1%ext_man %{_mandir}/man1/svg2xaml.1%ext_man
%{_mandir}/man1/xamlg.1%ext_man
%dir %{_libdir}/moonlight
%{_libdir}/moonlight/mopen.exe*
%{_bindir}/munxap %{_bindir}/mxap %{_bindir}/respack
%{_bindir}/sockpol %{_bindir}/unrespack %{_bindir}/xaml2html
%{_bindir}/xamlg %{_mandir}/man1/mopen.1%ext_man
%{_mandir}/man1/mxap.1%ext_man %{_mandir}/man1/respack.1%ext_man
%{_mandir}/man1/sockpol.1%ext_man %{_mandir}/man1/svg2xaml.1%ext_man
%{_mandir}/man1/xamlg.1%ext_man %{_libdir}/moonlight/munxap.exe*
%{_libdir}/moonlight/mxap.exe* %{_libdir}/moonlight/respack.exe*
%{_libdir}/moonlight/sockpol.exe* %{_libdir}/moonlight/xaml2html.exe*
%{_libdir}/moonlight/xamlg.exe*
