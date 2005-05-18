Summary:	Open source content management platform
Name:		drupal
Version:	4.6.0
Release:	0.1
Epoch:		0
License:	GPL
Group:		Applications/WWW
Source0:	http://drupal.org/files/projects/%{name}-%{version}.tar.gz
# Source0-md5:	cba80c4f511284b09d6a0a2def5cb250
URL:		http://drupal.org/
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

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir}/htdocs,%{_sysconfdir}}

cp -a *.ico index.php $RPM_BUILD_ROOT%{_appdir}/htdocs
cp -a themes misc $RPM_BUILD_ROOT%{_appdir}/htdocs

cp -a cron.php $RPM_BUILD_ROOT%{_appdir}
cp -a includes modules scripts sites $RPM_BUILD_ROOT%{_appdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.txt database
%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/htdocs
%{_appdir}/includes
%{_appdir}/modules
%{_appdir}/scripts
%{_appdir}/sites
