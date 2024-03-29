Summary:	Open source content management platform
Summary(pl.UTF-8):	Platforma do zarządzania treścią o otwartych źródłach
Name:		drupal
Version:	6.20
Release:	0.1
License:	GPL
Group:		Applications/WWW
Source0:	http://ftp.drupal.org/files/projects/%{name}-%{version}.tar.gz
# Source0-md5:	a4f59401fbb3e20e3a03ac5fc11bd27c
Source1:	%{name}.conf
Source2:	%{name}.cron
Source3:	%{name}.PLD
Patch0:		%{name}-cron.patch
Patch1:		%{name}-sitesdir.patch
Patch2:		%{name}-topdir.patch
#Patchx:	%{name}-replication.patch
#Patchx:	%{name}-emptypass.patch
URL:		http://www.drupal.org/
BuildRequires:	rpmbuild(macros) >= 1.264
BuildRequires:	sed >= 4.0
Requires:	%{name}(DB_Driver) = %{version}-%{release}
Requires:	apache(mod_access)
Requires:	apache(mod_alias)
Requires:	apache(mod_dir)
Requires:	apache(mod_expires)
Requires:	apache(mod_rewrite)
Requires:	php(mbstring)
Requires:	php(pcre)
Requires:	php(xml)
Requires:	webapps
Requires:	webserver = apache
Requires:	webserver(php) >= 4.3.3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_datadir}/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}

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

%description -l pl.UTF-8
Drupal to oprogramowanie pozwalające osobie lub społeczności
użytkowników na łatwe publikowanie, zarządzanie i organizowanie różnej
treści na stronie WWW. Dziesiątki tysięcy ludzi i organizacji używali
Drupala do ustawiania wyników różnych rodzajów stron WWW, w tym:
- portale WWW i strony dyskusyjne społeczności
- korporacyjne strony WWW/portale intranetowe
- osobiste strony WWW
- strony miłośników
- aplikacje e-commerce
- słowniki zasobów

Drupal zawiera zasoby umożliwiające tworzenie:
- systemów zarządzania treścią
- blogów
- środowisk pracy grupowej
- forów
- nowin
- galerii zdjęć
- wrzucania i ściągania plików

i wiele więcej.

%package cron
Summary:	Drupal cron
Summary(pl.UTF-8):	Usługa cron dla Drupala
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}
Requires:	crondaemon
Requires:	php-cli >= 3:4.3.3

%description cron
This package contains script which invokes cron hooks for Drupal.

%description cron -l pl.UTF-8
Ten pakiet zawiera skrypt wywołujący uchwyty crona dla Drupala.

%package db-mysql
Summary:	Drupal DB Driver for MySQL
Summary(pl.UTF-8):	Sterownik bazy danych MySQL dla Drupala
Group:		Applications/WWW
Requires:	php(mysql)
Provides:	%{name}(DB_Driver) = %{version}-%{release}

%description db-mysql
This virtual package provides MySQL database backend for Drupal.

%description db-mysql -l pl.UTF-8
Ten wirtualny pakiet dostarcza backend bazy danych MySQL dla Drupala.

%package db-pgsql
Summary:	Drupal DB Driver for PostgreSQL
Summary(pl.UTF-8):	Sterownik bazy danych PostgreSQL dla Drupala
Group:		Applications/WWW
Requires:	php(pgsql)
Provides:	%{name}(DB_Driver) = %{version}-%{release}

%description db-pgsql
This virtual package provides PostgreSQL database backend for Drupal.

NOTE: This driver is not tested in PLD, and not all modules have
database schema for PostgreSQL. Use this driver at your own risk!

%description db-pgsql -l pl.UTF-8
Ten wirtualny pakiet dostarcza backend bazy danych PostgreSQL dla
Drupala.

UWAGA: Ten sterownik nie był testowany w PLD i nie wszystkie moduły
mają schematy bazy danych dla PostgreSQL-a. Można go używać na własne
ryzyko.

%package update
Summary:	Package to perform Drupal database updates
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description update
This package contains scripts needed to do database updates via web.

%package xmlrpc
Summary:	XMLRPC server for Drupal
Summary(pl.UTF-8):	Serwer XMLRPC dla Drupala
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description xmlrpc
XMLRPC server for Drupal allows other Drupals authorize with your
Drupal's user creditentials, this is called Distributed Authentication
in Drupal world.

%description xmlrpc -l pl.UTF-8
Serwer XMLRPC dla Drupala pozwala innym Drupalom autoryzować się z
danymi uwierzytelniającymi użytkownika danego Drupala - jest to
nazywane rozproszonym uwierzytelnianiem.

%prep
%setup -q %{?_rc:-n %{name}-%{version}-%{_rc}}
%patch0 -p1
%patch1 -p1
%patch2 -p1

# cleanup backups after patching
find . '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f
cp -p %{SOURCE3} README.PLD

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/cron.d,/var/{cache,lib}/%{name}} \
	$RPM_BUILD_ROOT%{_appdir}/{po,database,modules/po,htdocs/modules,themes}

cp -a index.php $RPM_BUILD_ROOT%{_appdir}/htdocs
cp -a misc $RPM_BUILD_ROOT%{_appdir}/htdocs
cp -a install.php update.php xmlrpc.php $RPM_BUILD_ROOT%{_appdir}/htdocs

cp -a cron.php $RPM_BUILD_ROOT%{_appdir}
cp -a includes scripts $RPM_BUILD_ROOT%{_appdir}
cp -a sites $RPM_BUILD_ROOT%{_sysconfdir}
cp -a modules/* $RPM_BUILD_ROOT%{_appdir}/modules
cp -a themes/* $RPM_BUILD_ROOT%{_appdir}/themes
cp -Rl $RPM_BUILD_ROOT%{_appdir}/modules $RPM_BUILD_ROOT%{_appdir}/htdocs
cp -Rl $RPM_BUILD_ROOT%{_appdir}/themes $RPM_BUILD_ROOT%{_appdir}/htdocs

find $RPM_BUILD_ROOT%{_appdir}/htdocs/themes/ $RPM_BUILD_ROOT%{_appdir}/htdocs/modules/ \
  -type f -regextype posix-awk \
  -regex '.*\.(engine|inc|info|install|module|profile|po|sh|.*sql|theme|php|xtmpl)$|.*/(code-style\.pl|Entries.*|Repository|Root|Tag|Template)$' \
  -print0 | xargs -0 -r -l512 rm -f
find $RPM_BUILD_ROOT%{_appdir}/themes/ $RPM_BUILD_ROOT%{_appdir}/modules/ \
  -type f -regextype posix-awk \
  ! -regex '.*\.(engine|inc|info|install|module|profile|po|sh|.*sql|theme|php|xtmpl)$|.*/(code-style\.pl|Entries.*|Repository|Root|Tag|Template)$' \
  -print0 | xargs -0 -r -l512 rm -f

# avoid pulling perl dep
chmod -x $RPM_BUILD_ROOT%{_appdir}/scripts/*

ln -s /var/lib/%{name} $RPM_BUILD_ROOT%{_appdir}/files

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 1 ]; then
%banner -e %{name} <<'EOF'
If this is your first install of Drupal, You need at least configure
$db_url and $base_url in %{_sysconfdir}/sites/default/settings.php

EOF
fi

%post db-mysql
if [ "$1" = 1 ]; then
%banner -e %{name}-db-mysql <<'EOF'
If this is your first install of Drupal, you need to create Drupal database:

mysqladmin create drupal
zcat %{_docdir}/%{name}-db-mysql-%{version}/database.mysql.gz | mysql drupal
mysql -e "GRANT SELECT, INSERT, UPDATE, DELETE ON drupal.* TO 'drupal'@'localhost' IDENTIFIED BY 'password'"
mysql -e "GRANT CREATE TEMPORARY TABLES, LOCK TABLES ON *.* TO 'drupal'@'localhost'"

EOF
fi

%post db-pgsql
if [ "$1" = 1 ]; then
%banner -e %{name}-db-pgsql <<'EOF'
If this is your first install of Drupal, you need to create Drupal database:

and import initial schema from
%{_docdir}/%{name}-db-pgsql-%{version}/database.pgsql.gz

EOF
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc *.txt README.PLD

%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf

%attr(750,root,http) %dir %{_sysconfdir}/sites
%attr(750,root,http) %dir %{_sysconfdir}/sites/default
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sites/default/*
%attr(750,root,http) %dir %{_sysconfdir}/sites/all
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sites/all/*

%dir %{_appdir}
%{_appdir}/includes
%{_appdir}/modules
%{_appdir}/scripts
%{_appdir}/themes
%{_appdir}/po
# symlink
%{_appdir}/files

%dir %{_appdir}/htdocs
%{_appdir}/htdocs/index.php
%{_appdir}/htdocs/install.php
%{_appdir}/htdocs/misc
%{_appdir}/htdocs/themes
%{_appdir}/htdocs/modules

%dir %attr(775,root,http) /var/lib/%{name}
%dir %attr(775,root,http) /var/cache/%{name}

%files cron
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/%{name}
%attr(775,root,root) %{_appdir}/cron.php

%files db-mysql
%defattr(644,root,root,755)
#%doc README.replication

%files db-pgsql
%defattr(644,root,root,755)

%files update
%defattr(644,root,root,755)
%{_appdir}/htdocs/update.php
%{_appdir}/database

%files xmlrpc
%defattr(644,root,root,755)
%{_appdir}/htdocs/xmlrpc.php
