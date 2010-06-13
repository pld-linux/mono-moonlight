######		Unknown group!
Summary:	Novell Moonlight
Name:		mono-moonlight
Version:	@VERSION@
Release:	0
License:	LGPL v2.0 only ; MIT License (or similar) ; Ms-Pl
Group:		Productivity/Multimedia/Other
URL:		http://go-mono.com/moonlight/
ExclusiveArch:	%{ix86{ %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Source0:	%{name}-%{version}.tar.bz2
# Always required
BuildRequires:	cairo-devel >= 1.8.4
BuildRequires:	gtk+2-devel
BuildRequires:	libexpat-devel
BuildRequires:	libstdc++-devel
# Technically these two could be optional
BuildRequires:	alsa-devel
BuildRequires:	gtk-sharp2
BuildRequires:	libpulse-devel
BuildRequires:	mono-devel >= 2.6
BuildRequires:	monodoc-core
BuildRequires:	rsvg2-sharp
BuildRequires:	wnck-sharp
BuildRequires:	xulrunner-devel
BuildRequires:	zip
# Required to build the desktop assemblies
# Required to build the plugin
%if %{with_ffmpeg} == yes
BuildRequires:	libffmpeg-devel
%endif

%description
Moonlight is an open source implementation of Microsoft Silverlight
for Unix systems.

%package -n libmoon
######		Unknown group!
Summary:	Novell Moonlight
License:	LGPL v2.0 only
Group:		Productivity/Multimedia/Other
Requires:	mono-core >= 2.6

%description -n libmoon
Moonlight is an open source implementation of Microsoft Silverlight
for Unix systems.

%files -n libmoon
%defattr(644,root,root,755)
%doc AUTHORS COPYING README TODO NEWS
%attr(755,root,root) %{_libdir}/libmoon.so.*

%post -n libmoon -p /sbin/ldconfig
%postun -n libmoon -p /sbin/ldconfig

%package -n libmoon-devel
######		Unknown group!
Summary:	Development files for libmoon
License:	LGPL v2.0 only
Group:		Development/Languages/C and C++
Requires:	mono-devel >= 2.6

%description -n libmoon-devel
Development files for libmoon.

Moonlight is an open source implementation of Microsoft Silverlight
for Unix systems.

%files -n libmoon-devel
%defattr(644,root,root,755)
%{_libdir}/libmoon.so

%package plugin
######		Unknown group!
Summary:	Novell Moonlight Browser Plugin
License:	LGPL v2.0 only ; MIT License (or similar) ; Ms-Pl
Group:		Productivity/Multimedia/Other
Requires:	libmoon0 == %{version}
Requires:	mono-core >= 2.6

%description plugin
Novell Moonlight Browser Plugin.

Moonlight is an open source implementation of Microsoft Silverlight
for Unix systems.

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
%{_libdir}/moonlight/plugin/mscorlib.dll* # Is there somewhere we
could put this that would be universal?
%{_libdir}/browser-plugins/libmoonloader.so

%package web-devel
Summary:	Development files for Moonlight Web
License:	MIT License (or similar) ; Ms-Pl
Group:		Development/Languages
Recommends:	%{name}-plugin == %{version}

%description web-devel
Development files for creating Moonlight web applications.

Moonlight is an open source implementation of Microsoft Silverlight
for Unix systems.

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

%package desktop
######		Unknown group!
Summary:	Mono bindings for Moonlight Desktop
License:	MIT License (or similar) ; Ms-Pl
Group:		Productivity/Multimedia/Other
Requires:	libmoon0 == %{version}

%description desktop
Mono bindings for Novell Moonlight.

Moonlight is an open source implementation of Microsoft Silverlight
for Unix systems.

%files desktop
%defattr(644,root,root,755)
%{_prefix}/lib/mono/gac/Moon.Windows.Desktop
%{_prefix}/lib/mono/gac/Moonlight.Gtk
%{_prefix}/lib/mono/gac/System.Windows
%{_prefix}/lib/mono/gac/System.Windows.Browser
%{_prefix}/lib/mono/gac/System.Windows.Controls
%{_prefix}/lib/mono/gac/System.Windows.Controls.Data

%package desktop-devel
Summary:	Development files for Moonlight Desktop
License:	MIT License (or similar) ; Ms-Pl
Group:		Development/Languages
Recommends:	%{name}-tools == %{version}
Requires:	%{name}-desktop == %{version}
Requires:	glib2-devel
Requires:	gtk-sharp2
Requires:	libmoon0 == %{version}

%description desktop-devel
Development files for Moonlight Desktop.

Moonlight is an open source implementation of Microsoft Silverlight
for Unix systems.

%files desktop-devel
%defattr(644,root,root,755)
%dir %{_prefix}/lib/mono/moonlight
%{_prefix}/lib/mono/moonlight/Moon.Windows.Desktop.dll*
%{_prefix}/lib/mono/moonlight/System.Windows.Browser.dll*
%{_prefix}/lib/mono/moonlight/System.Windows.Controls.Data.dll*
%{_prefix}/lib/mono/moonlight/System.Windows.Controls.dll*
%{_prefix}/lib/mono/moonlight/System.Windows.dll*
%{_datadir}/pkgconfig/moonlight-desktop-2.0.pc # It may make sense in
the future to have a moonlight-gtk package
%{_prefix}/lib/mono/moonlight/Moonlight.Gtk.dll*
%{_prefix}/lib/monodoc/sources/moonlight-gtk.source
%{_prefix}/lib/monodoc/sources/moonlight-gtk.tree
%{_prefix}/lib/monodoc/sources/moonlight-gtk.zip
%{_datadir}/pkgconfig/moonlight-gtk-2.0.pc

%package tools
Summary:	Various tools for Novell Moonlight
License:	MIT License (or similar)
Group:		Development/Languages
Requires:	%{name}-desktop == %{version}
Requires:	libmoon0 == %{version}

%description tools
Various tools for Novell Moonlight.

Moonlight is an open source implementation of Microsoft Silverlight
for Unix systems.

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

%prep
%setup -q
%setup -q -T -D -b 1
%setup -q -T -D -b 2

%build
# The plugin requires a complete build of it's own mono
pushd ../mono-%{included_mono}
# We have not determined which --enable-minimal options might be safe
# so please do not use any of them
./configure --prefix=%{_builddir}/install \
			--with-mcs-docs=no \
			--with-ikvm-native=no
%{__make} #%{?jobs:-j%jobs} # mono is not strictly -j safe
# This gets installed in the build dir so that it gets wiped away
# and not installed on the system
%{__make} install
popd
# And then we build moonlight
# Only needed when there are Makefile.am or configure.ac patches
#autoreconf -f -i -Wnone
%configure --without-testing --without-performance --without-examples \
		   --with-mcspath=%{_builddir}/mono-%{included_mono}/mcs \
		   --with-mono-basic-path=%{_builddir}/mono-basic-%{included_mono} \
		   --with-ffmpeg=%{with_ffmpeg} \
		   --with-cairo=%{with_cairo}
%{__make} %{?jobs:-j%jobs}
# The next lines would build the XPI if we wanted it
# So that the xpi will pick up the custom libmono.so
#export PKG_CONFIG_PATH=%{_builddir}/install/lib/pkgconfig:${PKG_CONFIG_PATH}
#%{__make} user-plugin

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT
# Symlink the loader into browser-plugins for SUSE
install -d $RPM_BUILD_ROOT%{_libdir}/browser-plugins
ln -s %{_libdir}/moonlight/plugin/libmoonloader.so $RPM_BUILD_ROOT%{_libdir}/browser-plugins/libmoonloader.so
# We don't like nasty .la files
find $RPM_BUILD_ROOT -name \*.la -delete

%clean
rm -rf $RPM_BUILD_ROOT
