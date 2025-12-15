%define module wmctrl
%bcond test 1

Name:		python-wmctrl
Version:	0.5
Release:	1
Summary:	A tool to programmatically control windows inside X
URL:		https://pypi.org/project/wmctrl/
License:	MIT
Group:		Development/Python
Source0:	https://files.pythonhosted.org/packages/source/w/wmctrl/%{module}-%{version}.tar.gz
BuildSystem:	python
BuildArch:	noarch

BuildRequires:	openbox
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(obt-3.5)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	python
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(wheel)
BuildRequires:	python%{pyver}dist(attrs)
BuildRequires:	wmctrl
BuildRequires:	xclock
BuildRequires:	xfontsel
BuildRequires:	x11-server-xorg
BuildRequires:	x11-server-xvfb
%if %{with test}
BuildRequires:	python%{pyver}dist(pytest)
%endif
Requires:	python%{pyver}dist(attrs)
Requires:	wmctrl
Requires:	x11-server-xorg

%description
A tool to programmatically control windows inside X

%prep
%autosetup -p1 -n %{module}-%{version}
# Remove bundled egg-info
rm -rf %{module}.egg-info

sed -i 's/\(py$\|py\.test\)/pytest/g' test/test_wmctrl.py

%build
%py_build

%install
%py3_install

%if %{with test}
%check
export CI=true
export PYTHONPATH="%{buildroot}%{python_sitearch}:${PWD}"
cat > /tmp/test_script.sh <<EOF
#!/bin/sh
openbox &
sleep 10
wmctrl -l -G -p -x
%{__python} -m pytest -rs -k 'not (test_activate or test_properties or test_Desktop_active)' test/test_wmctrl.py
EOF
chmod +x /tmp/test_script.sh
xvfb-run /tmp/test_script.sh
%endif

%files
%{py_sitedir}/%{module}.py
%{py_sitedir}/__pycache__/%{module}*
%{py_sitedir}/%{module}-%{version}*.*-info
%license LICENSE
