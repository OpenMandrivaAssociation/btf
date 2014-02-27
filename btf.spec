%define NAME	BTF
%define major	%{version}
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname %{name} -d

Name:		btf
Version:	1.2.0
Release:	1
Epoch:		1
Summary:	Routines for permuting a matrix into block upper triangular form
Group:		System/Libraries
License:	LGPL
URL:		http://www.cise.ufl.edu/research/sparse/btf/
Source0:	http://www.cise.ufl.edu/research/sparse/btf/%{NAME}-%{version}.tar.gz
BuildRequires:	suitesparse-common-devel >= 4.0.0

%description
BTF is a software package for permuting a matrix into block upper
triangular form. It includes a maximum transversal algorithm, which
finds a permutation of a square or rectangular matrix so that it has a
zero-free diagonal (if one exists); otherwise, it finds a maximal
matching which maximizes the number of nonzeros on the diagonal.  The
package also includes a method for finding the strongly connected
components of a graph. These two methods together give the
permutation to block upper triangular form.

%package -n %{libname}
Summary:	Library of routines for permuting a matrix into block upper triangular form
Group:		System/Libraries

%description -n %{libname}
BTF is a software package for permuting a matrix into block upper
triangular form. It includes a maximum transversal algorithm, which
finds a permutation of a square or rectangular matrix so that it has a
zero-free diagonal (if one exists); otherwise, it finds a maximal
matching which maximizes the number of nonzeros on the diagonal.  The
package also includes a method for finding the strongly connected
components of a graph. These two methods together give the
permutation to block upper triangular form.

This package contains the library needed to run programs dynamically
linked against %{NAME}.

%package -n %{devname}
Summary:	C routines for permuting a matrix into block upper triangular form
Group:		Development/C
Requires:	suitesparse-common-devel >= 4.0.0
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
BTF is a software package for permuting a matrix into block upper
triangular form. It includes a maximum transversal algorithm, which
finds a permutation of a square or rectangular matrix so that it has a
zero-free diagonal (if one exists); otherwise, it finds a maximal
matching which maximizes the number of nonzeros on the diagonal.  The
package also includes a method for finding the strongly connected
components of a graph. These two methods together give the
permutation to block upper triangular form.

This package contains the files needed to develop applications which
use %{NAME}.

%prep
%setup -q -c -n %{name}-%{version}
cd %{NAME}
find . -perm 640 | xargs chmod 644
mkdir ../SuiteSparse_config
ln -sf %{_includedir}/suitesparse/SuiteSparse_config.* ../SuiteSparse_config

%build
cd %{NAME}
pushd Lib
    %make -f Makefile CC=gcc CFLAGS="%{optflags} -fPIC -I%{_includedir}/suitesparse" INC=
    gcc -shared -Wl,-soname,lib%{name}.so.%{major} -o lib%{name}.so.%{version} *.o
popd

%install
cd %{NAME}

%__install -d -m 755 %{buildroot}%{_libdir}
%__install -d -m 755 %{buildroot}%{_includedir}/suitesparse

for f in Lib/*.so*; do
    %__install -m 755 $f %{buildroot}%{_libdir}/`basename $f`
done
for f in Lib/*.a; do
    %__install -m 644 $f %{buildroot}%{_libdir}/`basename $f`
done
for f in Include/*.h; do
    %__install -m 644 $f %{buildroot}%{_includedir}/suitesparse/`basename $f`
done

%__ln_s lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so

%__install -d -m 755 %{buildroot}%{_docdir}/%{name}
%__install -m 644 README.txt Doc/*.txt Doc/ChangeLog %{buildroot}%{_docdir}/%{name}

%files -n %{libname}
%{_libdir}/*.so.*

%files -n %{devname}
%{_docdir}/%{name}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a

