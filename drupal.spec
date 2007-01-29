Summary:	Open source content management platform
Summary(pl):	Platforma do zarz±dzania tre¶ci± o otwartych ¼ród³ach
Name:		drupal
Version:	5.0
Release:	0.2
License:	GPL
Group:		Applications/WWW
Source0:	http://ftp.osuosl.org/pub/drupal/files/projects/%{name}-%{version}.tar.gz
# Source0-md5:	2e1d7573d21b8c97b02b63e28d356200
Source1:	%{name}.conf
Source2:	%{name}.cron
Source3:	%{name}.PLD
#Patch0:	%{name}-replication.patch
Patch1:		%{name}-sitesdir.patch
Patch2:		%{name}-topdir.patch
Patch3:		%{name}-themedir2.patch
#Patch4:	%{name}-emptypass.patch
URL:		http://drupal.org/
BuildRequires:	rpmbuild(macros) >= 1.264
BuildRequires:	sed >= 4.0
Requires:	%{name}(DB_Driver) = %{version}-%{release}
Requires:	apache(mod_access)
Requires:	apache(mod_alias)
Requires:	apache(mod_dir)
Requires:	apache(mod_expires)
Requires:	apache(mod_rewrite)
Requires:	php(mbstring)
Requires:	php(mysql)
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

%package db-mysql
Summary:	Drupal DB Driver for MySQL
Summary(pl):	Sterownik bazy danych MySQL dla Drupala
Group:		Applications/WWW
Requires:	php(mysql)
Provides:	%{name}(DB_Driver) = %{version}-%{release}

%description db-mysql
This virtual package provides MySQL database backend for Drupal.

%description db-mysql -l pl
Ten wirtualny pakiet dostarcza backend bazy danych MySQL dla Drupala.

%package db-pgsql
Summary:	Drupal DB Driver for PostgreSQL
Summary(pl):	Sterownik bazy danych PostgreSQL dla Drupala
Group:		Applications/WWW
Requires:	php(pgsql)
Provides:	%{name}(DB_Driver) = %{version}-%{release}

%description db-pgsql
This virtual package provides PostgreSQL database backend for Drupal.

NOTE: This driver is not tested in PLD, and not all modules have
database schema for PostgreSQL. Use this driver at your own risk!

%description db-pgsql -l pl
Ten wirtualny pakiet dostarcza backend bazy danych PostgreSQL dla
Drupala.

UWAGA: Ten sterownik nie by³ testowany w PLD i nie wszystkie modu³y
maj± schematy bazy danych dla PostgreSQL-a. Mo¿na go u¿ywaæ na w³asne
ryzyko.

%package update
Summary:	Package to perform Drupal database updates
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description update
This package contains scripts needed to do database updates via web.

%package xmlrpc
Summary:	XMLRPC server for Drupal
Summary(pl):	Serwer XMLRPC dla Drupala
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description xmlrpc
XMLRPC server for Drupal allows other Drupals authorize with your
Drupal's user creditentials, this is called Distributed Authentication
in Drupal world.

%description xmlrpc -l pl
Serwer XMLRPC dla Drupala pozwala innym Drupalom autoryzowaæ siê z
danymi uwierzytelniaj±cymi u¿ytkownika danego Drupala - jest to
nazywane rozproszonym uwierzytelnianiem.

%prep
%setup -q %{?_rc:-n %{name}-%{version}-%{_rc}}
#%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
#%patch4 -p1

find -name '*~' | xargs -r rm -v
cp -p %{SOURCE3} README.PLD

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/cron.d,/var/{cache,lib}/%{name}} \
	$RPM_BUILD_ROOT%{_appdir}/{po,database,modules/po,htdocs/modules}

cp -a index.php $RPM_BUILD_ROOT%{_appdir}/htdocs
cp -a misc $RPM_BUILD_ROOT%{_appdir}/htdocs
cp -a install.php update.php xmlrpc.php $RPM_BUILD_ROOT%{_appdir}/htdocs

cp -a cron.php $RPM_BUILD_ROOT%{_appdir}
cp -a modules/* $RPM_BUILD_ROOT%{_appdir}/modules
cp -a includes scripts $RPM_BUILD_ROOT%{_appdir}
cp -a sites $RPM_BUILD_ROOT%{_sysconfdir}
# avoid pulling perl dep
chmod -x $RPM_BUILD_ROOT%{_appdir}/scripts/*

ln -s /var/lib/%{name} $RPM_BUILD_ROOT%{_appdir}/files
# needed for node.module for syndication icon
ln -s htdocs/misc $RPM_BUILD_ROOT%{_appdir}

# install themes
install_theme() {
set -x
	local theme=$1
	local appdir=$RPM_BUILD_ROOT%{_appdir}
	local themedir=$appdir/htdocs/themes
	local themedir_shadow=$appdir/themes

	install -d $themedir/$theme
	cp -a themes/$theme/*.* $themedir/$theme
	if [ -f themes/$theme/*.theme ]; then
		install -d $themedir_shadow/$theme
		mv $themedir/$theme/*.theme $themedir_shadow/$theme
		ln -s ../../htdocs/themes/$theme/screenshot.png $themedir_shadow/$theme
	else
		if [[ $theme = */* ]]; then
			ln -s ../../htdocs/themes/$theme $themedir_shadow/$theme
		else
			ln -s ../htdocs/themes/$theme $themedir_shadow/$theme
		fi
	fi
}

install -d $RPM_BUILD_ROOT%{_appdir}/{themes,htdocs/themes}
install_theme bluemarine
install_theme chameleon
install_theme chameleon/marvin
install_theme pushbutton
cp -a themes/engines $RPM_BUILD_ROOT%{_appdir}/themes

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

%triggerin -- apache1
%webapp_register apache %{_webapp}

%triggerun -- apache1
%webapp_unregister apache %{_webapp}

%triggerin -- apache >= 2.0.0
%webapp_register httpd %{_webapp}

%triggerun -- apache >= 2.0.0
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
%{_appdir}/misc

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
