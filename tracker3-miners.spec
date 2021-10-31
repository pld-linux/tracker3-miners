#
# Conditional build:
%bcond_with	ffmpeg		# FFmpeg instead of GStreamer as generic media extractor
%bcond_with	gupnp		# GStreamer gupnp backend instead of discoverer
%bcond_with	icu		# ICU instead of enca for MP3 encoding detection

%define		abiver	3.0
Summary:	Tracker miners and metadata extractors
Summary(pl.UTF-8):	Narzędzia wydobywania danych dla programu Tracker
Name:		tracker3-miners
Version:	3.2.1
Release:	1
# see COPYING for details
License:	LGPL v2.1+ (libs), GPL v2+ (miners)
Group:		Applications
Source0:	https://download.gnome.org/sources/tracker-miners/3.2/tracker-miners-%{version}.tar.xz
# Source0-md5:	822d829e924657fc3434d69fb5a32630
URL:		https://wiki.gnome.org/Projects/Tracker
BuildRequires:	NetworkManager-devel
BuildRequires:	asciidoc
# sha256sum
BuildRequires:	coreutils >= 6.0
BuildRequires:	dbus-devel >= 1.3.1
%{!?with_icu:BuildRequires:	enca-devel >= 1.9}
BuildRequires:	exempi-devel >= 2.1.0
# libavcodec libavformat libavutil
%{?with_ffmpeg:BuildRequires:	ffmpeg-devel >= 0.8.4}
BuildRequires:	gexiv2-devel
BuildRequires:	giflib-devel
BuildRequires:	glib2-devel >= 1:2.70.0
BuildRequires:	gstreamer-devel >= 1.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0
%if %{with gupnp}
BuildRequires:	gupnp-dlna-devel >= 0.9.4
BuildRequires:	gupnp-dlna-gst-devel >= 0.9.4
%endif
BuildRequires:	libcue-devel >= 2.0.0
BuildRequires:	libexif-devel >= 0.6
BuildRequires:	libgrss-devel >= 0.7
BuildRequires:	libgsf-devel >= 1.14.24
BuildRequires:	libgxps-devel
%{?with_icu:BuildRequires:	libicu-devel >= 4.8.1.1}
BuildRequires:	libiptcdata-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libosinfo-devel >= 0.2.9
BuildRequires:	libpng-devel >= 0.89
%ifnarch alpha ia64 m68k parisc parisc64 riscv64 sh4 sparc sparcv9 sparc64
BuildRequires:	libseccomp-devel >= 2.0
%endif
BuildRequires:	libtiff-devel >= 4
BuildRequires:	libxml2-devel >= 1:2.6
BuildRequires:	libxslt-progs
BuildRequires:	meson >= 0.51
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	poppler-glib-devel >= 0.16.0
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	totem-pl-parser-devel
BuildRequires:	tracker3-devel >= 3.2.0
BuildRequires:	tracker3-testutils >= 3.2.0
BuildRequires:	upower-devel >= 0.9.0
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	dbus >= 1.3.1
%{!?with_icu:Requires:	enca-libs >= 1.9}
Requires:	exempi >= 2.1.0
Requires:	glib2 >= 1:2.70.0
%if %{with gupnp}
Requires:	gupnp-dlna >= 0.9.4
Requires:	gupnp-dlna-gst >= 0.9.4
%endif
Requires:	libcue >= 2.0.0
Requires:	libexif >= 0.6
Requires:	libgrss >= 0.7
Requires:	libgsf >= 1.14.24
Requires:	libosinfo >= 0.2.9
Requires:	libxml2 >= 1:2.6
Requires:	systemd-units >= 1:242
Requires:	tracker3 >= 3.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains various miners and metadata extractors for
tracker.

%description -l pl.UTF-8
Ten pakiet zawiera narzędzia wydobywania danych dla programu Tracker.

%prep
%setup -q -n tracker-miners-%{version}

%build
%meson build \
	--default-library=shared \
	-Dbattery_detection=upower \
	-Dcharset_detection=%{?with_icu:icu}%{!?with_icu:enca} \
	-Dfunctional_tests=false \
	-Dgeneric_media_extractor=%{?with_ffmpeg:libav}%{!?with_ffmpeg:gstreamer} \
	-Dgstreamer_backend=%{?with_gupnp:gupnp}%{!?with_gupnp:discoverer} \
	-Dsystemd_user_services_dir=%{systemduserunitdir}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%find_lang tracker3-miners

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas

%postun
%glib_compile_schemas

%files -f tracker3-miners.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING MAINTAINERS NEWS README.md
%attr(755,root,root) %{_libexecdir}/tracker-extract-3
%attr(755,root,root) %{_libexecdir}/tracker-miner-fs-3
%attr(755,root,root) %{_libexecdir}/tracker-miner-fs-control-3
%attr(755,root,root) %{_libexecdir}/tracker-miner-rss-3
%attr(755,root,root) %{_libexecdir}/tracker-writeback-3
%dir %{_libexecdir}/tracker3
%attr(755,root,root) %{_libexecdir}/tracker3/daemon
%attr(755,root,root) %{_libexecdir}/tracker3/extract
%attr(755,root,root) %{_libexecdir}/tracker3/index
%attr(755,root,root) %{_libexecdir}/tracker3/info
%attr(755,root,root) %{_libexecdir}/tracker3/reset
%attr(755,root,root) %{_libexecdir}/tracker3/search
%attr(755,root,root) %{_libexecdir}/tracker3/status
%attr(755,root,root) %{_libexecdir}/tracker3/tag
%{systemduserunitdir}/tracker-extract-3.service
%{systemduserunitdir}/tracker-miner-fs-3.service
%{systemduserunitdir}/tracker-miner-fs-control-3.service
%{systemduserunitdir}/tracker-miner-rss-3.service
%{systemduserunitdir}/tracker-writeback-3.service
/etc/xdg/autostart/tracker-miner-fs-3.desktop
/etc/xdg/autostart/tracker-miner-rss-3.desktop
%dir %{_libdir}/tracker-miners-%{abiver}
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/libtracker-extract.so
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/libtracker-miner-3.0.so
%dir %{_libdir}/tracker-miners-%{abiver}/extract-modules
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/extract-modules/libextract-abw.so
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/extract-modules/libextract-bmp.so
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/extract-modules/libextract-desktop.so
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/extract-modules/libextract-disc-generic.so
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/extract-modules/libextract-dummy.so
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/extract-modules/libextract-epub.so
# R: giflib
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/extract-modules/libextract-gif.so
# R: gstreamer gstreamer-plugins-base
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/extract-modules/libextract-gstreamer.so
# R: libxml2
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/extract-modules/libextract-html.so
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/extract-modules/libextract-icon.so
# R: libosinfo
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/extract-modules/libextract-iso.so
# R: libiptcdata libjpeg
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/extract-modules/libextract-jpeg.so
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/extract-modules/libextract-mp3.so
# R: libgsf
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/extract-modules/libextract-msoffice.so
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/extract-modules/libextract-msoffice-xml.so
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/extract-modules/libextract-oasis.so
# R: poppler-glib
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/extract-modules/libextract-pdf.so
# R: totem-plparser
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/extract-modules/libextract-playlist.so
# R: libpng
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/extract-modules/libextract-png.so
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/extract-modules/libextract-ps.so
# R: libgexiv2
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/extract-modules/libextract-raw.so
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/extract-modules/libextract-text.so
# R: libtiff
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/extract-modules/libextract-tiff.so
# R: libgxps
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/extract-modules/libextract-xps.so
%dir %{_libdir}/tracker-miners-%{abiver}/writeback-modules
# R: gstreamer gstreamer-plugins-base
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/writeback-modules/libwriteback-gstreamer.so
# R: exempi
%attr(755,root,root) %{_libdir}/tracker-miners-%{abiver}/writeback-modules/libwriteback-xmp.so
%{_datadir}/dbus-1/interfaces/org.freedesktop.Tracker3.Miner.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.Tracker3.Miner.Files.Index.xml
%{_datadir}/dbus-1/services/org.freedesktop.Tracker3.Miner.Extract.service
%{_datadir}/dbus-1/services/org.freedesktop.Tracker3.Miner.Files.service
%{_datadir}/dbus-1/services/org.freedesktop.Tracker3.Miner.Files.Control.service
%{_datadir}/dbus-1/services/org.freedesktop.Tracker3.Miner.RSS.service
%{_datadir}/dbus-1/services/org.freedesktop.Tracker3.Writeback.service
%{_datadir}/glib-2.0/schemas/org.freedesktop.Tracker3.Extract.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.Tracker3.FTS.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.Tracker3.Miner.Files.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.TrackerMiners3.enums.xml
%dir %{_datadir}/tracker3-miners
%dir %{_datadir}/tracker3-miners/domain-ontologies
%{_datadir}/tracker3-miners/domain-ontologies/default.rule
%dir %{_datadir}/tracker3-miners/extract-rules
# standalone (builtin?) rules
%{_datadir}/tracker3-miners/extract-rules/10-comics.rule
%{_datadir}/tracker3-miners/extract-rules/10-ebooks.rule
%{_datadir}/tracker3-miners/extract-rules/10-svg.rule
%{_datadir}/tracker3-miners/extract-rules/15-executable.rule
%{_datadir}/tracker3-miners/extract-rules/15-games.rule
# modules
%{_datadir}/tracker3-miners/extract-rules/10-abw.rule
%{_datadir}/tracker3-miners/extract-rules/10-bmp.rule
%{_datadir}/tracker3-miners/extract-rules/10-desktop.rule
%{_datadir}/tracker3-miners/extract-rules/10-epub.rule
%{_datadir}/tracker3-miners/extract-rules/10-gif.rule
%{_datadir}/tracker3-miners/extract-rules/10-html.rule
%{_datadir}/tracker3-miners/extract-rules/10-ico.rule
%{_datadir}/tracker3-miners/extract-rules/10-jpeg.rule
%{_datadir}/tracker3-miners/extract-rules/10-mp3.rule
%{_datadir}/tracker3-miners/extract-rules/10-msoffice.rule
%{_datadir}/tracker3-miners/extract-rules/10-oasis.rule
%{_datadir}/tracker3-miners/extract-rules/10-pdf.rule
%{_datadir}/tracker3-miners/extract-rules/10-png.rule
%{_datadir}/tracker3-miners/extract-rules/10-ps.rule
%{_datadir}/tracker3-miners/extract-rules/10-raw.rule
%{_datadir}/tracker3-miners/extract-rules/10-tiff.rule
%{_datadir}/tracker3-miners/extract-rules/10-xps.rule
%{_datadir}/tracker3-miners/extract-rules/11-iso.rule
%{_datadir}/tracker3-miners/extract-rules/11-msoffice-xml.rule
# libextract-gstreamer
%{_datadir}/tracker3-miners/extract-rules/15-gstreamer-guess.rule
%{_datadir}/tracker3-miners/extract-rules/15-playlist.rule
# libextract-text
%{_datadir}/tracker3-miners/extract-rules/15-text.rule
%{_datadir}/tracker3-miners/extract-rules/90-disc-generic.rule
# libextract-gstreamer
%{_datadir}/tracker3-miners/extract-rules/90-gstreamer-audio-generic.rule
# libextract-gstreamer
%{_datadir}/tracker3-miners/extract-rules/90-gstreamer-video-generic.rule
%dir %{_datadir}/tracker3-miners/miners
%{_datadir}/tracker3-miners/miners/org.freedesktop.Tracker3.Miner.Files.service
%{_datadir}/tracker3-miners/miners/org.freedesktop.Tracker3.Miner.RSS.service
%{_mandir}/man1/tracker-miner-fs-3.1*
%{_mandir}/man1/tracker-miner-rss-3.1*
%{_mandir}/man1/tracker-writeback-3.1*
%{_mandir}/man1/tracker3-daemon.1*
%{_mandir}/man1/tracker3-extract.1*
%{_mandir}/man1/tracker3-index.1*
%{_mandir}/man1/tracker3-info.1*
%{_mandir}/man1/tracker3-reset.1*
%{_mandir}/man1/tracker3-search.1*
%{_mandir}/man1/tracker3-status.1*
%{_mandir}/man1/tracker3-tag.1*
