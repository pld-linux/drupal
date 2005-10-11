Summary:	Open source content management platform
Summary(pl):	Platforma do zarz±dzania tre¶ci± o otwartych ¼ród³ach
Name:		drupal
Version:	4.6.3
Release:	0.25
License:	GPL
Group:		Applications/WWW
Source0:	http://drupal.org/files/projects/%{name}-%{version}.tar.gz
# Source0-md5:	f436973f02aa2cea15ef1ca90223082b
Source1:	%{name}.conf
Source2:	%{name}.cron
Source3:	%{name}.PLD
Patch3:		%{name}-replication.patch
Patch5:		%{name}-sitesdir.patch
Patch6:		%{name}-topdir.patch
Patch7:		%{name}-themedir2.patch
Patch8:		%{name}-emptypass.patch
Patch9:		%{name}-cron.patch
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
Requires:	%{name}(DB_Driver) = %{version}-%{release}
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

%package db-mysql
Summary:	Drupal DB Driver for MySQL
Summary(pl):	Sterownik bazy danych MySQL dla Drupala
Group:		Applications/WWW
Requires:	php-mysql
Provides:	%{name}(DB_Driver) = %{version}-%{release}

%description db-mysql
This virtual package provides MySQL database backend for Drupal.

%description db-mysql -l pl
Ten wirtualny pakiet dostarcza backend bazy danych MySQL dla
Drupala.

%package db-pgsql
Summary:	Drupal DB Driver for PostgreSQL
Summary(pl):	Sterownik bazy danych PostgreSQL dla Drupala
Group:		Applications/WWW
Requires:	php-pgsql
Provides:	%{name}(DB_Driver) = %{version}-%{release}

%description db-pgsql
This virtual package provides PostgreSQL database backend for
Drupal.

NOTE: This driver is not tested in PLD, and not all modules have
database schema for PostgreSQL. Use this driver at your own risk!

%description db-pgsql -l pl
Ten wirtualny pakiet dostarcza backend bazy danych PostgreSQL dla
Drupala.

UWAGA: Ten sterownik nie by³ testowany w PLD i nie wszystkie modu³y
maj± schematy bazy danych dla PostgreSQL-a. Mo¿na go u¿ywaæ na w³asne
ryzyko.

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
%setup -q
%patch3 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

find -name '*~' | xargs -r rm -v
cp %{SOURCE3} README.PLD

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/cron.d,/var/{cache,lib}/%{name}} \
	$RPM_BUILD_ROOT%{_appdir}/{po,modules/po,htdocs/modules}

cp -a *.ico index.php $RPM_BUILD_ROOT%{_appdir}/htdocs
cp -a misc $RPM_BUILD_ROOT%{_appdir}/htdocs
cp -a xmlrpc.php $RPM_BUILD_ROOT%{_appdir}/htdocs

cp -a cron.php $RPM_BUILD_ROOT%{_appdir}
cp -a modules/* $RPM_BUILD_ROOT%{_appdir}/modules
cp -a includes scripts $RPM_BUILD_ROOT%{_appdir}
cp -a sites $RPM_BUILD_ROOT%{_sysconfdir}

ln -s /var/lib/%{name} $RPM_BUILD_ROOT%{_appdir}/files

# install themes
cp -a themes $RPM_BUILD_ROOT%{_appdir}/htdocs
# move .xtmpl/.theme out of htdocs
(cd $RPM_BUILD_ROOT%{_appdir}/htdocs && tar cf - --remove-files themes/*/*.{xtmpl,theme}) | tar -xf - -C $RPM_BUILD_ROOT%{_appdir}
mv $RPM_BUILD_ROOT%{_appdir}/{htdocs/,}themes/engines
# make screenshot.png available in appdir
for a in $RPM_BUILD_ROOT%{_appdir}/htdocs/themes/*; do
	t=$(basename $a)
	ln -s ../../htdocs/themes/$t/screenshot.png $RPM_BUILD_ROOT%{_appdir}/themes/$t
done

# a hack
s=themes/chameleon/marvin
ln -s ../../htdocs/$s $RPM_BUILD_ROOT%{_appdir}/$s

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 1 ]; then
%banner -e %{name} <<EOF
If this is your first install of Drupal, you need to create drupal database:
mysqladmin create drupal

and import initial schema:
zcat %{_docdir}/%{name}-%{version}/database/database.mysql.gz | mysql drupal

Also read INSTALL from documentation!

EOF
fi

%triggerin -- apache1 >= 1.3.33-2
%apache_config_install -v 1 -c %{_sysconfdir}/apache.conf

%triggerun -- apache1 >= 1.3.33-2
%apache_config_uninstall -v 1

%triggerin -- apache >= 2.0.0
%apache_config_install -v 2 -c %{_sysconfdir}/apache.conf

%triggerun -- apache >= 2.0.0
%apache_config_uninstall -v 2

%files
%defattr(644,root,root,755)
%doc *.txt database README.replication README.PLD

%attr(750,root,http) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf

%attr(750,root,http) %dir %{_sysconfdir}/sites
%attr(750,root,http) %dir %{_sysconfdir}/sites/default
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sites/default/*

%dir %{_appdir}
%{_appdir}/includes
%{_appdir}/modules
%{_appdir}/scripts
%{_appdir}/themes
%{_appdir}/po
# symlink
%{_appdir}/files

%dir %{_appdir}/htdocs
%{_appdir}/htdocs/*.ico
%{_appdir}/htdocs/index.php
%{_appdir}/htdocs/misc
%{_appdir}/htdocs/themes
%{_appdir}/htdocs/modules

%dir %attr(775,root,http) /var/lib/%{name}
%dir %attr(775,root,http) /var/cache/%{name}

%files cron
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/%{name}
%{_appdir}/cron.php

%files db-mysql
%defattr(644,root,root,755)

%files db-pgsql
%defattr(644,root,root,755)

%files xmlrpc
%defattr(644,root,root,755)
%{_appdir}/htdocs/xmlrpc.php
