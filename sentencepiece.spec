%define _disable_ld_no_undefined 1


%define libname %mklibname sentencepiece
%define devname %mklibname -d sentencepiece

Name:		sentencepiece
Version:	0.2.0
Release:	1
Summary:	An unsupervised text tokenizer for Neural Network-based text generation

License:	Apache-2.0
URL:		https://github.com/google/sentencepiece
Source0:	%{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:	cmake
BuildRequires:	gperftools-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	python-setuptools

%description
The SentencePiece is an unsupervised text tokenizer for Neural Network-based
text generation.
It is an unsupervised text tokenizer and detokenizer mainly for
Neural Network-based text generation systems where the vocabulary size is
predetermined prior to the neural model training.
SentencePiece implements subword units and unigram language model with the
extension of direct training from raw sentences.
SentencePiece allows us to make a purely end-to-end system that does not
depend on language-specific pre/post-processing.

%package -n %{libname}
Summary:	Runtime libraries for SentencePiece

%description -n %{libname}
This package contains the libraries for SentencePiece.

%package tools
Summary:	Tools for SentencePiece
Requires:	%{libname} = %{EVRD}

%description tools
This package contains tools for manipulate models for SentencePiece.

%package -n %{devname}
Summary:	Libraries and header files for SentencePiece
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
This package contains header files to develop a software using SentencePiece.

%package        -n python-%{name}
Summary:	Python module for SentencePiece
Requires:	%{libname} = %{EVRD}
%{?python_provide:%python_provide python3-%{name}}

%description -n python-%{name}
This package contains Python3 module file for SentencePiece.

%prep
%autosetup

%build
%cmake \
    -DCMAKE_BUILD_TYPE=Release \

%make_build
cd ..
cd python
%py_build
cd ..

%install
%make_install -C build
cd python
%py_install
cd ..

# remove static
rm %{buildroot}%{_libdir}/libsentencepiece*.a

%files -n %{libname}
%doc README.md
%license LICENSE
%{_libdir}/libsentencepiece*.so.0*

%files -n %{devname}
%{_includedir}/sentencepiece*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/sentencepiece*.pc

%files tools
%{_bindir}/spm*

%files -n python-%{name}
%{python_sitearch}/%{name}/
%{python_sitearch}/%{name}-*.egg-info/
