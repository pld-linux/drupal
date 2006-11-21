%define		_ver		4.6
%define		_patchlevel	10
Summary:	Open source content management platform
Summary(pl):	Platforma do zarz±dzania tre¶ci± o otwartych ¼ród³ach
Name:		drupal
Version:	%{_ver}.%{_patchlevel}
Release:	2
License:	GPL
Group:		Applications/WWW
Source0:	http://drupal.org/files/projects/%{name}-%{version}.tar.gz
# Source0-md5:	c96eef1d33b5bac9526b3b1d6fc5b556
Source1:	%{name}.conf
Source2:	%{name}.cron
Source3:	%{name}.PLD
Patch0:		%{name}-replication.patch
Patch1:		%{name}-sitesdir.patch
Patch2:		%{name}-topdir.patch
Patch3:		%{name}-themedir2.patch
Patch4:		%{name}-emptypass.patch
Patch5:		%{name}-cron.patch
Patch6:		%{name}-19298-cache.patch
Patch7:		%{name}-update-cli.patch
Patch8:		%{name}-locale-memory.patch
Patch9:		%{name}-comment.patch
URL:		http://drupal.org/
BuildRequires:	rpmbuild(macros) >= 1.264
BuildRequires:	sed >= 4.0
Requires:	%{name}(DB_Driver) = %{version}-%{release}
Requires:	%{name}(theme) = %{_ver}
Requires:	apache(mod_access)
Requires:	apache(mod_alias)
Requires:	apache(mod_dir)
Requires:	apache(mod_expires)
Requires:	apache(mod_rewrite)
Requires:	php(mysql)
Requires:	php(pcre)
Requires:	php(xml)
Requires:	webapps
Requires:	webserver = apache
Requires:	webserver(php) >= 4.3.3
Obsoletes:	drupal-update
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
Requires:	/usr/bin/php
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

%package themes
Summary:	Themes distributed with Drupal
Summary(pl):	Motywy rozprowadzane z Drupalem
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}
Provides:	drupal(theme) = %{_ver}

%description themes
This package contains themes distributed with Drupal.

%description themes -l pl
Ten pakiet zawiera motywy rozprowadzane z Drupalem.

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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p0
%patch7 -p1
%patch8 -p1
%patch9 -p1

cp -p %{SOURCE3} README.PLD

# remove backups from patching as we use globs to package files to buildroot
find '(' -name '*~' -o -name '*.orig' ')' | xargs -r rm -v

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/cron.d,/var/{cache,lib}/%{name}} \
	$RPM_BUILD_ROOT%{_appdir}/{po,database,modules/po,htdocs/modules}

cp -a *.ico index.php $RPM_BUILD_ROOT%{_appdir}/htdocs
cp -a misc $RPM_BUILD_ROOT%{_appdir}/htdocs
cp -a xmlrpc.php $RPM_BUILD_ROOT%{_appdir}/htdocs
cp -a database/updates.inc $RPM_BUILD_ROOT%{_appdir}/database

cp -a cron.php update.php $RPM_BUILD_ROOT%{_appdir}
cp -a modules/* $RPM_BUILD_ROOT%{_appdir}/modules
cp -a includes scripts $RPM_BUILD_ROOT%{_appdir}
cp -a sites $RPM_BUILD_ROOT%{_sysconfdir}

ln -s /var/lib/%{name} $RPM_BUILD_ROOT%{_appdir}/files
# needed for node.module for syndication icon
ln -s htdocs/misc $RPM_BUILD_ROOT%{_appdir}

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
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post db-mysql
if [ "$1" = 1 ]; then
%banner -e %{name}-db-mysql <<EOF
If this is your first install of Drupal, you need to create Drupal database:

mysqladmin create drupal
zcat %{_docdir}/%{name}-db-mysql-%{version}/database.mysql.gz | mysql drupal
mysql -e "GRANT SELECT, INSERT, UPDATE, DELETE ON drupal.* TO 'drupal'@'localhost' IDENTIFIED BY 'PASSWORD'"
mysql -e "GRANT CREATE TEMPORARY TABLES, LOCK TABLES ON *.* TO 'drupal'@'localhost'"

EOF
fi

%post db-pgsql
if [ "$1" = 1 ]; then
%banner -e %{name}-db-pgsql <<EOF
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

%triggerpostun -- %{name} < 4.6.4-0.4
# rescue app configs.
if [ -f /etc/drupal/sites/default/settings.php.rpmsave ]; then
	mv -f %{_sysconfdir}/sites/default/settings.php{,.rpmnew}
	mv -f /etc/drupal/sites/default/settings.php.rpmsave %{_sysconfdir}/sites/default/settings.php
fi
# other configured sites, if any
for i in /etc/drupal/sites/*; do
	d=$(basename $i)
	[ "$d" = "default" ] && continue
	mv -f %{_sysconfdir}/sites/$d{,.rpmnew}
	mv -f $i %{_sysconfdir}/sites/$d
done

# migrate from apache-config macros
if [ -f /etc/drupal/apache.conf.rpmsave ]; then
	if [ -d /etc/apache/webapps.d ]; then
		cp -f %{_sysconfdir}/apache.conf{,.rpmnew}
		cp -f /etc/drupal/apache.conf.rpmsave %{_sysconfdir}/apache.conf
	fi

	if [ -d /etc/httpd/webapps.d ]; then
		cp -f %{_sysconfdir}/httpd.conf{,.rpmnew}
		cp -f /etc/drupal/apache.conf.rpmsave %{_sysconfdir}/httpd.conf
	fi
	rm -f /etc/drupal/apache.conf.rpmsave
fi

# place new config location, as trigger puts config only on first install, do it here.
if [ -L /etc/apache/conf.d/99_%{name}.conf ]; then
	rm -f /etc/apache/conf.d/99_%{name}.conf
	/usr/sbin/webapp register apache %{_webapp}
	apache_reload=1
fi
if [ -L /etc/httpd/httpd.conf/99_%{name}.conf ]; then
	rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	/usr/sbin/webapp register httpd %{_webapp}
	httpd_reload=1
fi

if [ "$httpd_reload" ]; then
	%service -q httpd reload
fi
if [ "$apache_reload" ]; then
	%service -q apache reload
fi

%triggerpostun -- %{name} < 4.6.8-0.5
grep -l 'This_is_a_Drupal_security_line_do_not_remove' \
%{_sysconfdir}/apache.conf %{_sysconfdir}/httpd.conf \
| xargs -r \
sed -i -e '
/This_is_a_Drupal_security_line_do_not_remove/{
	d
	n
	a\	SetHandler Drupal_Security_Do_Not_Remove_See_SA_2006_006
	a\	Options None
	a\	<IfModule mod_rewrite.c>
	a\	\	RewriteEngine off
	a\	</IfModule>
}'
egrep -c 'Drupal_Security_Do_Not_Remove_See_SA_2006_006' \
%{_sysconfdir}/apache.conf %{_sysconfdir}/httpd.conf \
| awk -F: '/:0/{print $1}' | xargs -r \
sed -i -e '
/<Directory \/var\/lib\/drupal>/{
	n
	a\	SetHandler Drupal_Security_Do_Not_Remove_See_SA_2006_006
	a\	Options None
	a\	<IfModule mod_rewrite.c>
	a\	\	RewriteEngine off
	a\	</IfModule>
}'
[ ! -L /etc/httpd/webapps.d/drupal.conf ] || %service -q httpd reload
[ ! -L /etc/apache/webapps.d/drupal.conf ] || %service -q apache reload

%files
%defattr(644,root,root,755)
%doc *.txt README.PLD

%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf

%attr(750,root,http) %dir %{_sysconfdir}/sites
%attr(750,root,http) %dir %{_sysconfdir}/sites/default
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sites/default/*

%dir %{_appdir}
%{_appdir}/database
%{_appdir}/includes
%exclude %{_appdir}/includes/database.mysql.inc
%exclude %{_appdir}/includes/database.pgsql.inc
%{_appdir}/modules
%{_appdir}/scripts
%dir %{_appdir}/themes
%dir %{_appdir}/themes/engines
%{_appdir}/po
%{_appdir}/update.php
# symlinks
%{_appdir}/files
%{_appdir}/misc

%dir %{_appdir}/htdocs
%{_appdir}/htdocs/*.ico
%{_appdir}/htdocs/index.php
%{_appdir}/htdocs/misc
%dir %{_appdir}/htdocs/themes
%{_appdir}/htdocs/modules

%dir %attr(775,root,http) /var/lib/%{name}
%dir %attr(775,root,http) /var/cache/%{name}

%files cron
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/%{name}
%{_appdir}/cron.php

%files db-mysql
%defattr(644,root,root,755)
%doc database/*.mysql
%doc README.replication
%{_appdir}/includes/database.mysql.inc

%files db-pgsql
%defattr(644,root,root,755)
%doc database/*.pgsql
%{_appdir}/includes/database.pgsql.inc

%files themes
%defattr(644,root,root,755)
%{_appdir}/themes/[!e]*
%{_appdir}/themes/engines/*
%{_appdir}/htdocs/themes/*

%files xmlrpc
%defattr(644,root,root,755)
%{_appdir}/htdocs/xmlrpc.php
