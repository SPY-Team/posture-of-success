# Client

Build Requirements

* Install CMake Version 3.15+: https://cmake.org/download/

* Install Conan: https://conan.io/downloads.html

## Windows (Visual Studio 2017)

Run the following commands:

```
cd client
mkdir build
cd build
cmake -G "Visual Studio 15 2017 Win64" ..
```

Open the `.sln` file in Visual Studio.

## Mac

Run the following commands:

```
cd client
mkdir build
cd build
cmake -G "Xcode" ..
```

Open the `.xcodeproj` folder in Xcode.

## Linux

Run the following commands:

```
cd client
mkdir build
cd build
cmake ..
make -j
```