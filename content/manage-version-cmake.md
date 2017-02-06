Title: Cmake를 이용한 version 관리
Date: 2013-09-14 18:01
Category: Blog
Tags: cmake, library_version
Slug: manage-version-cmake
Authors: Wonseok Choi

[cmake](http://www.cmake.org)는 요즘 오픈소스 프로젝트에서 많이 사용되는
build system이다. autotools를 이용해서 배포하는 경우에는 UNIX에 기본적으로
설치되어있는 도구들을 이용하기 때문에 autotools 자체가 필요하지 않다는 장점이
있지만, 사용하기가 어려워 사람들이 꺼려하는 것 같다. 뿐만아니라 다양한 platform
에서 사용할 수 없다.

python으로 작성된 Scons, waf 등 도 있는데, 사용해보지 않아서 할 말은 없지만
cross platform 지원 및 유연함 확장성 등 이 좋을 것 같다. 다만 python이 설치된
시스템에서만 사용할 수 있다. 큰 프로젝트에서는 속도도 문제가 된다고 한다.

cmake는 Scons와는 다르게 실행파일 (executable)을 만들어내지 않고 makefile (Linux
등), solution file (Windows)를 만들어준다. 그렇기 때문에 IDE 또는 다른 build
system과 독립적으로 사용될 수 있다. Qt library를 이용하는 경우에 qmake 대신에
cmake를 이용할 수 있어서 프로젝트에 포함시키기가 쉽다.
google test (gtest)를 이용할 때도 프로젝트에 포함시킨 후 `add_subdirectory`
명령만 사용하면 된다 (gtest에 CMakeLists.txt 파일이 있기 때문에 가능하다).[1]

cmake는 상당히 많은 platform을 지원하는데, real time OS 중에 하나인 QNX에서도
사용할 수 있다. 지금 일하는 회사에서 개인적으로 vim과 terminal에서 작업하는
것을 선호해서 cmake를 사용해왔는데, 최근에 기본 build system으로 선정해서
사용하기로 했다. cross compile이 가능하도록 option을 만들 수도 있고, 기본적으로
terminal에서 command로 build 및 test를 실행할 수 있어야 일일빌드 등 도 할 수
있다.

프로그램을 만들 때 (특히 library) versioning 하는 것은 상당히 중요하다.
cmake를 이용한다면 오늘 소개하는 방식으로 version 관리를 할 수 있을 것이다.
여러가지 방법이 있겠지만 다음과 같이 version number를 정한다:

* major: 호환성을 보장하지 않는 큰 변화.
* minor: 호환성을 (거의) 보장하는 변화 (기능 추가, 개선 등).
* patch: 호환성을 완벽히 보장 (bug fix, 긴급한 수정 등).

build 시 자동으로 위에 정의한 version number를 적용시키기 위해 다음과 같이
CMakeLists.txt 파일을 작성한다.

    :::cmake
    set (MYPROJECT_VERSION_MAJOR 0)
    set (MYPROJECT_VERSION_MINOR 1)
    set (MYPROJECT_VERSION_PATCH 0)
    set (MYPROJECT_VERSION_STRING "0.1.0")
    set (MYPROJECT_FEATURES
        "feature_a",
        "feature_b"
        )

    configure_file (
        "${version_SOURCE_DIR}/version.h.in"
        "${CMAKE_BINARY_DIR}/include/version.h"
        )

`myproject`라는 프로젝트를 하고 있다면 root directory에 version이라는 폴더를
만든다 (어떻게 하든 상관없지만..). 위의 내용은 version 폴더에 위치한 
CMakeLists.txt에 포함된다. 만약 위의 내용대로라면 `version.h.in` 파일로 부터
`${CMAKE_BINARY_DIR}/include/version.h` 를 만들기 때문에, 상위 폴더에 있는
CMakeLists.txt에는 다음 명령이 포함되어 있어야 한다.

    :::cmake
    include_directories (
        "${CMAKE_BINARY_DIR}/include"
        )

`CMAKE_BINARY_DIR` 은 cmake를 실행한 경로를 의미한다.

`version.h.in` 의 내용은 다음과 같다:

    :::cpp
    #ifndef MYPROJECT_VERSION_H_
    #define MYPROJECT_VERSION_H_

    #include <string>

    #define MYPROJECT_VERSION_MAJOR @MYPROJECT_VERSION_MAJOR@
    #define MYPROJECT_VERSION_MINOR @MYPROJECT_VERSION_MINOR@
    #define MYPROJECT_VERSION_PATCH @MYPROJECT_VERSION_PATCH@
    #define MYPROJECT_VERSION_STRING "@MYPROJECT_VERSION_STRING@
    #define MYPROJECT_FEATURES "@MYPROJECT_FEATURES@;" // do not delete last ;

    class myproject_version
    {
        static int major();
        static int minor();
        static int patch();
        static std::string version();
        static bool atLeast(int major, int minor, int patch);
        static bool hasFeature(const std::string &name);
    };

    #endif // !MYPROJECT_VERSION_H_

`@`로 감싼 cmake variable이 치환되어 `version.h` 파일이 된다.

`myproject_version` class의 기능을 구현하기 위해 cpp 파일에 다음의 내용이
포함되면 된다.

    :::cpp
    #ifndef MYPROJECT_VERSION_H_
    #include "version.h"
    #include <cstring>

    int myproject_version::major()
    {
            return MYPROJECT_VERSION_MAJOR;
    }

    int myproject_version::minor()
    {
            return MYPROJECT_VERSION_MINOR;
    }

    int myproject_version::patch()
    {
            return MYPROJECT_VERSION_PATCH;
    }

    std::string myproject_version::version()
    {
            return std::string(MYPROJECT_VERSION_STRING);
    }

    bool myproject_version::atLeast(int major, int minor, int patch)
    {
        if (major < MYPROJECT_VERSION_MAJOR) {
            return false;
        }
        if (minor < MYPROJECT_VERSION_MINOR) {
            return false;
        }
        if (patch < MYPROJECT_VERSION_PATCH) {
            return false;
        }
        return true;
    }

    bool myproject_version::hasFeature(const std::string& name)
    {
        const char* pch;
        const char* start;
        const char* features = MYPROJECT_FEATURES;

        start = features;
        pch = strchr(features, ';');

        while (pch != NULL) {
            std::string feature(start, pch - start);
            if (feature == name) {
                return true;
            }
            start = pch + 1;
            pch = strchr(start, ';');
        }
        return false;
    }

version number 정하는 것과 version 정보를 제공하는 class 등 에 대한 내용은
API design for C++ [2] 에서 다루고 있으니 참고하기 바란다.

그러면 version 정보를 활용하는 방법에 대해서 알아보자.

Compile time에 확인하는 방법은 다음과 같다:

    :::cpp
    #ifndef MYPROJECT_VERSION_H_
    #include "version.h"
    ...
    #if ((MYPROJECT_VERSION_MAJOR < 1) ||\
         (MYPROJECT_VERSION_MINOR < 0) ||\
         (MYPROJECT_VERSION_PATCH < 1))
    #error "version >= v1.0.1 required."
    #endif

Runtime에서 확인하는 방법은 다음과 같다:

    :::cpp
    #ifndef MYPROJECT_VERSION_H_
    #include "version.h"

    // get version numbers
    int major = myproject_version::major();
    int minor = myproject_version::minor();
    int patch = myproject_version::patch();

    // get version string
    std::cout << "myproject version: " << myproject_version::version() << "\n";

    // at least v1.0.0
    if (myproject_versioin::atLeast(1, 0, 0)) {
        ...
    }

    // has feature XXX?
    if (myproject_version::hasFeature("XXX")) {
        // use XXX
    }

version 정보 관리를 굳이 cmake를 이용해서 할 필요는 없다.
그렇다 하더라도 `myproject_version` class가 도움이 될 수 있을 것이다.
cmake를 프로젝트의 기본 build system으로 쓰고 있다면 참고해보길 바란다.

[1] 참고로, google test를 사용할 때 프로젝트에 포함시켜서 같이 컴파일할 것을
추천하고 있다. [google test FAQ](http://code.google.com/p/googletest/wiki/V1_6_FAQ#Why_is_it_not_recommended_to_install_a_pre-compiled_copy_of_Goog)

[2]  [API design for C++](http://www.apibook.com/blog)
