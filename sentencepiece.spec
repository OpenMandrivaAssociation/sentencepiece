%define _disable_ld_no_undefined 1


%define libname %mklibname sentencepiece
%define devname %mklibname -d sentencepiece

Name:		sentencepiece
Version:	0.2.2
Release:	2
Summary:	An unsupervised text tokenizer for Neural Network-based text generation

License:	Apache-2.0
Group:	Development/Other
URL:		https://github.com/google/sentencepiece
Source0:	%{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:		sentencepiece-shared-python.patch

BuildRequires:  make
BuildRequires:	cmake
BuildRequires:	gperftools-devel
BuildRequires:	pkgconfig
BuildRequires:	cmake(absl)
# cmake itself provides cmake(protobuf) via its find module, which does
# not install the library. The pc file is only in the devel package.
BuildRequires:	pkgconfig(protobuf)
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(pybind11)

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
%autosetup -p1
# The release tarball ships an Abseil that does not build with this
# compiler. CMake links third_party/absl to the system headers only when
# that directory is missing, and this tree already contains it.
# The system Abseil aliases std:: ordering types, which exist only in C++20.
rm -rf third_party/absl
ln -s %{_includedir}/absl third_party/absl
sed -i 's/set(CMAKE_CXX_STANDARD 17)/set(CMAKE_CXX_STANDARD 20)/' CMakeLists.txt

%build
%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DSPM_ABSL_PROVIDER=package \
    -DSPM_PROTOBUF_PROVIDER=package \

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
%{python_sitearch}/sentencepiece-%{version}.dist-info
