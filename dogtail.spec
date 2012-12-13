%define beta beta5

Summary: GUI test tool and automation framework
Name: dogtail
Version: 0.8.2
Release: 0.5.%{beta}%{?dist}
License: GPLv2
URL: http://dogtail.fedorahosted.org/
Source0: %{name}-%{version}.tar.gz
#Source0: http://fedorahosted.org/released/dogtail/%{name}-%{version}.tar.gz

BuildArch: noarch

BuildRequires: python2-devel
BuildRequires: desktop-file-utils

Obsoletes: pyspi

Requires: pyatspi
Requires: pygobject3
Requires: pycairo
Requires: pygtk2
Requires: rpm-python
Requires: xorg-x11-xinit
Requires: python-imaging
Requires: sudo

%description
GUI test tool and automation framework that uses assistive technologies to 
communicate with desktop applications.

%prep
%setup -q -n %{name}-%{version}

%build
python ./setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python ./setup.py install -O2 --root=$RPM_BUILD_ROOT --record=%{name}.files
rm -rf $RPM_BUILD_ROOT/%{_docdir}/dogtail
rm -f $RPM_BUILD_ROOT/%{python_sitelib}/%{name}-%{version}-py%{python_version}.egg-info
find examples -type f -exec chmod 0644 \{\} \;
desktop-file-install $RPM_BUILD_ROOT/%{_datadir}/applications/sniff.desktop \
  --vendor=fedora \
  --dir=$RPM_BUILD_ROOT/%{_datadir}/applications \
  --add-category X-Fedora \
  --delete-original

%post
touch --no-create %{_datadir}/icons/hicolor || :
[ -x /usr/bin/gtk-update-icon-cache ] && gtk-update-icon-cache --quiet -f %{_datadir}/icons/hicolor || :

%postun
touch --no-create %{_datadir}/icons/hicolor || :
[ -x /usr/bin/gtk-update-icon-cache ] && gtk-update-icon-cache --quiet -f %{_datadir}/icons/hicolor || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{python_sitelib}/dogtail/
%{_datadir}/applications/*
%{_datadir}/dogtail/
%{_datadir}/icons/hicolor/*
%doc COPYING
%doc README
%doc NEWS
%doc examples/

%changelog

* Wed Nov 2 2012 Vitezslav Humpa <vhumpa@redhat.com> - 0.8.2-0.1.beta1
- Internal EL7 release/beta build 
- Wrote a dogtail-run-headless-next - script that uses a DisplayManager
 (gdm/kdm) to handle the X server / session management. Should replace
  headless in the future if systemd spreads.
 
-Also fixed a wrong condition in the sessions module

* Wed Oct 18 2012 Vitezslav Humpa <vhumpa@redhat.com> - 0.8.1-2
- Respin

* Wed Oct 16 2012 Vitezslav Humpa <vhumpa@redhat.com> - 0.8.1-1
- New upstream release

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 04 2012 Jaroslav Reznik <jreznik@redhat.com> - 0.8.0-2
- respin

* Thu May 31 2012 Jaroslav Reznik <jreznik@redhat.com> - 0.8.0-1
- Update to 0.8.0 Final
- New upstream release

* Mon Apr 16 2012 Jaroslav Reznik <jreznik@redhat.com> - 0.8.0-0.5.beta5
- Update to 0.8.0 beta 5

* Mon Apr 02 2012 Jaroslav Reznik <jreznik@redhat.com> - 0.8.0-0.2.beta2
- Update to 0.8.0 beta 2

* Mon Mar 19 2012 Jaroslav Reznik <jreznik@redhat.com> - 0.8.0-0.1.beta1
- Update to 0.8.0 beta 1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Oct 08 2009 Zack Cerza <zcerza@redhat.com> - 0.7.0-1
- New upstream release.
- Drop Requires on xorg-x11-server-Xvfb.
- Update URL and Source0.
- Ship NEWS file.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.90-4.401
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.90-3.401
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.6.90-2.401
- Rebuild for Python 2.6

* Tue Aug 12 2008 Zack Cerza <zcerza@redhat.com> - 0.6.90-1.401
- New upstream snapshot.
- Require python-imaging

* Tue Aug 12 2008 Zack Cerza <zcerza@redhat.com> - 0.6.90-1.381.2
- Really fix license tag.

* Wed Jul 16 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.6.90-1.381.1
- fix license tag

* Thu Jan 31 2008 Zack Cerza <zcerza@redhat.com> - 0.6.90-1.381
- New upstream snapshot.
- Obsolete pyspi; Require at-spi-python.
- Require pygtk2-libglade.
- Don't ship the .egg-info file.

* Wed Jan  3 2007 Zack Cerza <zcerza@redhat.com> - 0.6.1-1
- New upstream release.

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 0.6.0-2
- build for python 2.5
- BR python-devel

* Wed Sep 13 2006 Zack Cerza <zcerza@redhat.com> - 0.6.0-1
- New upstream release.
- Add Requires for xorg-x11-xinit.
- Add Requires for gnome-python2-gconf.
- Bump pyspi Requires.
- Remove upstreamed patches.

* Fri Aug 18 2006 Zack Cerza <zcerza@redhat.com> - 0.5.2-3
- Add Requires for xorg-x11-xinit. Closes: #203189.

* Fri Aug 11 2006 Zack Cerza <zcerza@redhat.com> - 0.5.2-2
- Added headless-gconf.patch to use the python gconf bindings.
- Added desktop-file-categories.patch to put sniff and dogtail-recorder under
  the 'Programming' menu.

* Tue Aug 01 2006 Zack Cerza <zcerza@redhat.com> - 0.5.2-1
- New upstream release.
- Update Requires from Xvfb to xorg-x11-server-Xvfb.
- Bump pyspi Requires.
- Remove ImageMagick Requires.
- Escape post-macro in changelog-macro.

* Mon Apr 17 2006 Zack Cerza <zcerza@redhat.com> - 0.5.1-3
- Fix the URL field.

* Tue Mar 21 2006 Zack Cerza <zcerza@redhat.com> - 0.5.1-2
- Fix URL and Source0 fields.
- Fix desktop-file-utils magic; use desktop-file-install.

* Fri Feb 24 2006 Zack Cerza <zcerza@redhat.com> - 0.5.1-1
- Remove BuildRequires on at-spi-devel. Added one on python.
- Use macros instead of absolute paths.
- Touch _datadir/icons/hicolor/ before running gtk-update-icon-cache.
- Require and use desktop-file-utils.
- postun = post.
- Shorten BuildArchitectures to BuildArch. The former worked, but even vim's 
  hilighting hated it.
- Put each *Requires on a separate line.
- Remove __os_install_post definition.
- Use Fedora Extras BuildRoot.
- Instead of _libdir, which kills the build if it's /usr/lib64, use a
  python macro to define python_sitelib and use that.
- Remove the executable bit on the examples in install scriptlet.
- Remove call to /bin/rm in post scriptlet.
- Use dist in Release.

* Fri Feb 17 2006 Zack Cerza <zcerza@redhat.com> - 0.5.0-2
- It looks like xorg-x11-Xvfb changed names. Require 'Xvfb' instead.
- Remove Requires on python-elementtree, since RHEL4 didn't have it. The 
  functionality it provides is probably never used anyway, and will most likely
  be removed in the future.
- Don't run gtk-update-icon-cache if it doesn't exist.

* Fri Feb  3 2006 Zack Cerza <zcerza@redhat.com> - 0.5.0-1
- New upstream release.
- Added missing BuildRequires on at-spi-devel.
- Added Requires on pyspi >= 0.5.3.
- Added Requires on rpm-python, pygtk2, ImageMagick, xorg-x11-Xvfb, 
  python-elementtree.
- Moved documentation (including examples) to the correct place.
- Make sure /usr/share/doc/dogtail is removed.
- Added 'gtk-update-icon-cache' to %%post.

* Mon Oct 24 2005 Zack Cerza <zcerza@redhat.com> - 0.4.3-1
- New upstream release.

* Sat Oct  8 2005 Jeremy Katz <katzj@redhat.com> - 0.4.2-1
- Initial build.

