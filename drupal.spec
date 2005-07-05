Summary:	Open source content management platform
Summary(pl):	Platforma do zarz±dzania tre¶ci± o otwartych ¼ród³ach
Name:		drupal
Version:	4.6.2
Release:	0.6
Epoch:		0
License:	GPL
Group:		Applications/WWW
Source0:	http://drupal.org/files/projects/%{name}-%{version}.tar.gz
# Source0-md5:	7bbee605d6b57052e27adb1a61685ec1
Source1:	%{name}.conf
Source2:	%{name}.cron
Source3:	http://www.drupal.org/misc/favicon.ico
# Source3-md5:	f0ee98b4394dfdab17c16245dd799204
Patch0:		%{name}-config.patch
Patch1:		%{name}-includedir.patch
Patch2:		%{name}-module-themedir.patch
Patch3:		%{name}-emptypass.patch
Patch4:		%{name}-themedir.patch
Patch5:		%{name}-sitesdir.patch
Patch6:		%{name}-topdir.patch
Patch7:		%{name}-themedir2.patch
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
Requires:	php-pcre
#Requires:	php-pgsql
Requires:	php-xml
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

%description -l pl
Drupal to oprogramowanie pozwalaj±ce osobie lub spo³eczno¶ci
u¿ytkowników na ³atwe publikowanie, zarz±dzanie i organizowanie ró¿nej
tre¶ci na stronie WWW. Dziesi±tki tysiêcy ludzi i organizacji u¿ywali
Drupala do ustawiania wyników ró¿nych rodzajów stron WWW, w tym:
- portale WWW i strony dyskusyjne spo³eczno¶ci
- korporacyjne strony WWW/portale intranetowe
- osobiste strony WWW
- strony mi³o¶ników
- aplikacje e-commerce
- s³owniki zasobów

Drupal zawiera zasoby umo¿liwiaj±ce tworzenie:
- systemów zarz±dzania tre¶ci±
- blogów
- ¶rodowisk pracy grupowej
- forów
- nowin
- galerii zdjêæ
- wrzucania i ¶ci±gania plików

i wiele wiêcej.

%package cron
Summary:	Drupal cron
Summary(pl):	Us³uga cron dla Drupala
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}
Requires:	crondaemon
Requires:	php-cli >= 3:4.3.3

%description cron
This package contains script which invokes cron hooks for Drupal.

%description cron -l pl
Ten pakiet zawiera skrypt wywo³uj±cy uchwyty crona dla Drupala.

%prep
%setup -q
%patch0 -p1
#%patch1 -p1
#%patch2 -p1
%patch3 -p1
#%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

#grep -rl 'include_once .includes/' . | xargs sed -i -e '
#	s,include_once \(.\)includes/,include_once \1%{_appdir}/includes/,g
#'

find -name '*~' | xargs -r rm -v

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir}/htdocs/files,%{_sysconfdir},/etc/cron.d}

cp -a *.ico index.php $RPM_BUILD_ROOT%{_appdir}/htdocs
cp -a misc $RPM_BUILD_ROOT%{_appdir}/htdocs

cp -a cron.php $RPM_BUILD_ROOT%{_appdir}
cp -a includes modules scripts $RPM_BUILD_ROOT%{_appdir}
cp -a sites $RPM_BUILD_ROOT%{_sysconfdir}

cp -a themes $RPM_BUILD_ROOT%{_appdir}/htdocs

# move .xtmpl/.theme out of htdocs
(cd $RPM_BUILD_ROOT%{_appdir}/htdocs && tar cf - --remove-files themes/*/*.{xtmpl,theme}) | tar -xf - -C $RPM_BUILD_ROOT%{_appdir}
mv $RPM_BUILD_ROOT%{_appdir}/{htdocs/,}themes/engines

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache-%{name}.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT%{_appdir}/htdocs

%clean
rm -rf $RPM_BUILD_ROOT

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
%{_appdir}/includes
%{_appdir}/modules
%{_appdir}/scripts
%{_appdir}/themes

%dir %{_appdir}/htdocs
%{_appdir}/htdocs/*.*
%{_appdir}/htdocs/misc
%{_appdir}/htdocs/themes
%dir %attr(775,root,http) %{_appdir}/htdocs/files

%files cron
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/%{name}
%{_appdir}/cron.php
