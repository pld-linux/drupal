Summary:	Open source content management platform
Name:		drupal
Version:	4.6.0
Release:	0.31
Epoch:		0
License:	GPL
Group:		Applications/WWW
Source0:	http://drupal.org/files/projects/%{name}-%{version}.tar.gz
# Source0-md5:	cba80c4f511284b09d6a0a2def5cb250
Source1:	%{name}.conf
Patch0:		%{name}-config.patch
Patch1:		%{name}-includedir.patch
Patch2:		%{name}-module-themedir.patch
Patch3:		%{name}-emptypass.patch
Patch4:		%{name}-themedir.patch
Patch5:		%{name}-sitesdir.patch
Patch6:		%{name}-topdir.patch
URL:		http://drupal.org/
BuildRequires:	rpmbuild(macros) >= 1.194
BuildRequires:	sed >= 4.0
Requires:	apache >= 1.3.33-3
Requires:	apache(mod_dir)
Requires:	apache(mod_access)
Requires:	apache(mod_expires)
Requires:	apache(mod_rewrite)
Requires:	apache(mod_alias)
Requires:	php >= 3:4.3.3
Requires:	php-mysql
#Requires:	php-pgsql
#Requires:	php-xml
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_datadir}/%{name}
%define		_sysconfdir	/etc/%{name}

%description
Drupal is software that allows an individual or a community of users
to easily publish, manage and organize a great variety of content on a
website. Tens of thousands of people and organizations have used
Drupal to set up scores of different kinds of web sites, including
- community web portals and discussion sites
- corporate web sites/intranet portals
- personal web sites
- afficionado sites
- e-commerce applications
- resource directories

Drupal includes features to enable
- content management systems
- blogs
- collaborative authoring environments
- forums
- newsletters
- picture galleries
- file uploads and download

and much more.

%prep
%setup -q
%patch0 -p1 -b config
#%patch1 -p1 -b includedir
#%patch2 -p1 -b module-themedir
%patch3 -p1 -b emptypass
%patch4 -p1 -b themedir
%patch5 -p1 -b sitesdir
%patch6 -p1 -b topdir

#grep -rl 'include_once .includes/' . | xargs sed -i -e '
#	s,include_once \(.\)includes/,include_once \1%{_appdir}/includes/,g
#'

find -name '*~' | xargs -r rm -v

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir}/htdocs,%{_sysconfdir}}

cp -a *.ico index.php $RPM_BUILD_ROOT%{_appdir}/htdocs
cp -a misc $RPM_BUILD_ROOT%{_appdir}/htdocs

cp -a cron.php $RPM_BUILD_ROOT%{_appdir}
cp -a includes modules scripts $RPM_BUILD_ROOT%{_appdir}
cp -a sites $RPM_BUILD_ROOT%{_sysconfdir}

cp -a themes $RPM_BUILD_ROOT%{_appdir}/htdocs
# move .xtmpl out of htdocs
(cd $RPM_BUILD_ROOT%{_appdir}/htdocs && tar cf - --remove-files themes/*/*.xtmpl) | tar -xf - -C $RPM_BUILD_ROOT%{_appdir}
mv $RPM_BUILD_ROOT%{_appdir}/{htdocs/,}themes/engines

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache-%{name}.conf

%post
if [ "$1" = 1 ]; then
%banner -e %{name} <<EOF
If this is your first install of Drupal, you need to create drupal database:
shell$ mysqladmin create drupal

and import initial schema:
shell$ zcat %{_docdir}/%{name}-%{version}/database/database.mysql.gz | mysql drupal

(anyway, read INSTALL file from documentation).

EOF
fi

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 >= 1.3.33-2
%apache_config_install -v 1 -c %{_sysconfdir}/apache-%{name}.conf

%triggerun -- apache1 >= 1.3.33-2
%apache_config_uninstall -v 1

%triggerin -- apache >= 2.0.0
%apache_config_install -v 2 -c %{_sysconfdir}/apache-%{name}.conf

%triggerun -- apache >= 2.0.0
%apache_config_uninstall -v 2

%files
%defattr(644,root,root,755)
%doc *.txt database

%attr(750,root,http) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache-%{name}.conf

%attr(750,root,http) %dir %{_sysconfdir}/sites
%attr(750,root,http) %dir %{_sysconfdir}/sites/default
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sites/default/*

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/htdocs
%{_appdir}/includes
%{_appdir}/modules
%{_appdir}/scripts
%{_appdir}/themes
