# libmpv-builds

libmpv (mpv with FFmpeg) for Windows and macOS in the configuration of [media_kit](https://github.com/media-kit/media-kit)'s
video packages, built in GitHub Actions from pinned sources and published with their corresponding source.

* **Windows**: `libmpv-2.dll` for x64 and arm64, in archives laid out like media-kit's (`libmpv-2.dll`, `libmpv.dll.a`,
  `include/mpv`).
* **macOS**: universal xcframeworks (arm64 and x86_64) for macOS 12 and later, like those of media-kit's
  libmpv-darwin-build, with libplacebo added.

The libraries are under the GNU LGPL, version 3 or later as built. Every library is pinned to a commit or to the SHA-256
of its archive, and each release carries the complete source it was built from.

## Who it is for

* media_kit users on Windows and macOS who want a recent mpv and FFmpeg: the versions media_kit downloads today date
  from 2023 and 2024.
* Anyone who redistributes libmpv and must provide its corresponding source: each release has it, next to the binaries.

## What a release holds

Releases are tagged `YYYYMMDD-N` (the date of the run and its number).

| File | What it is |
|---|---|
| `mpv-dev-x86_64-<date>-git-<mpv>.7z`, `mpv-dev-aarch64-<date>-git-<mpv>.7z` | Windows: `libmpv-2.dll`, `libmpv.dll.a`, `include/mpv`, `licenses/` (the licence texts of every library) and `BUILDINFO.txt` |
| `BUILDINFO-x86_64.txt`, `BUILDINFO-aarch64.txt` | the recipe, the container, the compiler, and every library with its repository and commit |
| `libmpv-windows-<tag>-sources.tar.xz` | the corresponding source of both DLLs: the recipe as built, the `windows` folder of this repository, and every library at its commit |
| `libmpv-xcframeworks_<tag>_macos-universal-video-default.tar.gz` | macOS: every xcframework |
| `libmpv-xcframeworks_<tag>_macos-universal-video-default_<Name>.zip` | one xcframework per zip, for Swift Package Manager |
| `BUILDINFO-macos.txt` | the recipe, Xcode, Nix, and every source archive with its SHA-256 |
| `libmpv-macos-<tag>-sources.tar.xz` | the corresponding source: the recipe with the files of `macos/` over it, and every archive it builds from |
| `libmpv-macos-<tag>-licenses.tar.gz` | the licence texts of each macOS library |
| `SHA256SUMS.txt` | the SHA-256 of every file above |

The notes of each release say which systems it holds and link the Actions run that built it.

## Check the files

```sh
sha256sum --ignore-missing -c SHA256SUMS.txt        # Linux
shasum -a 256 --ignore-missing -c SHA256SUMS.txt    # macOS
```

On Windows, `Get-FileHash <file>` in PowerShell prints the SHA-256 to compare with the line of `SHA256SUMS.txt`. The log
of the run linked in the release notes prints the same hashes, computed where the files were built.

## Use them with media_kit

* **Windows**: `media_kit_libs_windows_video` downloads its archive in `windows/CMakeLists.txt`. With a copy of that
  package (`dependency_overrides` with a `path`), point the download at the archive of a release and check it by its
  SHA-256 (`file(SHA256 ...)`) rather than by MD5. My own copy does that and can serve as an example:
  [CMakeLists.txt](https://github.com/freeKC/Immuch360/blob/a0af38a54c78de24601c31ee7979895c0a8c9b6d/mobile/packages/media_kit_libs_windows_video/windows/CMakeLists.txt).
* **macOS**: `media_kit_libs_macos_video` declares its xcframeworks as binary targets in `Package.swift`. A copy of it
  can point those targets at the zips of a release, each with its SHA-256 from `SHA256SUMS.txt`, and add `Placebo`
  (mpv needs libplacebo since 0.37). The summary of each run prints these lines; my own copy is an example:
  [Package.swift](https://github.com/freeKC/Immuch360/blob/a0af38a54c78de24601c31ee7979895c0a8c9b6d/mobile/packages/media_kit_libs_macos_video/macos/media_kit_libs_macos_video/Package.swift).
* **Without media_kit**: the Windows archive has the usual `mpv-dev` layout of mpv's Windows builds, for any program that
  loads `libmpv-2.dll` through mpv's client API.

## Configuration

These builds are made for media_kit's video packages; other configurations are out of scope.

* **Windows**: FFmpeg and mpv as in the video build of media-kit/libmpv-win32-video-cmake, which Predidit's fork keeps
  building, with these differences:
  * none of Predidit's mpv patches: one turns TLS certificate verification off by default, one adds a D3D11 render API
    that media_kit_video does not use;
  * mpv without libarchive (no playback from inside zip, rar or 7z files) and without its Vulkan output;
  * a few more FFmpeg components: the hstack, vstack, crop and pad filters and the converters between them, the ProRes,
    VC-1 and raw video decoders, the yuv4mpegpipe demuxer, the AV1, VP9 and VC-1 parsers.

  FFmpeg has no GPL or nonfree part and is configured with `--enable-version3` (it links OpenSSL 3); mpv is built with
  `-Dgpl=false`.
* **macOS**: the default video flavor of media-kit/libmpv-darwin-build, with:
  * FFmpeg and mpv at the commits of the Windows build, and libplacebo, which mpv needs since 0.37;
  * media-kit's four FFmpeg patches left out: they were written for FFmpeg 6.0 (HLS seek, DASH base URL, iOS HDR
    textures, a separate VP9 decoder) and two of them no longer apply;
  * two mpv patches (`macos/patches/`): with Cocoa on and Swift off, as in this recipe, mpv otherwise calls Swift
    functions that are not built, and libmpv crashes in `mpv_create`;
  * macOS 12 and later instead of 10.9 (libplacebo is C++20);
  * a check after the build that fails when a framework calls a symbol that no framework defines.

  The other libraries keep the recipe's versions.

The first release has mpv from its master branch of 14 September 2026 (`0b7ed670`) and FFmpeg from its master branch
of 15 September 2026 (`5b9a3ad7`). The BUILDINFO files of each release list everything else.

## Limits

* The Windows arm64 DLL has no OpenGL, like media-kit's own arm64 build, so media_kit_video cannot render video with
  it. It is built, not tested.
* The macOS frameworks have run on GitHub's macOS runners only, not on a real Mac yet.
* New releases are made by hand, after security releases of FFmpeg or mpv; nothing updates by itself.

## How it was tested

These recipes and pins also build the libmpv of Immuch360 Desktop, the desktop preview of Immuch360, an unofficial fork
of the Immich mobile app.

* Windows x64: the app played flat and 360° videos with it on a Windows 11 laptop (Intel UHD and NVIDIA RTX 4060
  Laptop).
* macOS: the self check of the app on GitHub's macOS runner played a few seconds of video, drawn in software.
* Every macOS build runs the check for undefined symbols described above.

## How the builds are made

One workflow, [`.github/workflows/build.yml`](.github/workflows/build.yml), run by hand from the Actions tab:

* **Windows**: Predidit/libmpv-win32-video-cmake (a fork of media-kit/libmpv-win32-video-cmake, itself a fork of
  shinchiro/mpv-winbuild-cmake), at a pinned commit, cross-compiles mpv, FFmpeg and their libraries with LLVM and
  mingw-w64 in shinchiro's Arch Linux container, pinned by its digest (a copy is kept at `ghcr.io/freekc/libmpv-build`).
  The two files that set the options of FFmpeg and mpv are fetched by URL and checked by SHA-256
  (`windows/recipe-files.lock`, see [Licence](#licence)); every other library is checked out at its commit in
  `windows/sources.lock`; Meson is installed by hash.
* **macOS**: media-kit/libmpv-darwin-build at a pinned commit, with the files of `macos/` over it (`apply_overlay.sh`),
  built by Nix in its sandbox on GitHub's macos-15 runner with Xcode 16.4; every source archive is pinned by its SHA-256
  in `macos/packages.lock.nix`.
* The last job computes `SHA256SUMS.txt` and publishes the binaries, the BUILDINFO files, the licence texts and the
  sources in one release.
* Every quarter, a scheduled run builds the Windows DLL from the head of every library, publishes nothing, and lists
  the commits it used, to show what a refresh of `windows/sources.lock` would bring.

To rebuild, fork this repository and run the workflow with its inputs (`ffmpeg_ref`, `mpv_ref`, `recipe_ref`,
`macos_recipe_ref`, `systems`, `sources`, `publish`); the steps of the workflow are the exact commands, and the
BUILDINFO files name the container, the compiler and Xcode.

## The LGPL, for those who ship these libraries

This is how I read it, not legal advice.

* A program under any licence may use libmpv through its C API, as long as users can put their own build of the
  library in its place; a separate DLL or framework allows that.
* The licence texts go with the program (the `licenses/` folder of each Windows archive, the macOS licences archive),
  with a notice that it uses libmpv and FFmpeg under the LGPL.
* The corresponding source must be available to those who get the binaries: ship the sources archive of the release
  you use, or point to it. If you point to it, you stay responsible for its availability, so keeping a copy is safer.

How this repository meets these obligations for its own releases: each release holds the source of exactly what it
contains, with the recipe and scripts that built it, and the licence texts; the BUILDINFO files list every library
with its commit or archive hash; the binaries of a release are never online without its sources archive.
[NOTICES.md](NOTICES.md) lists every library and its licence.

## Licence

* My own files (the workflow, the scripts, the lock files, the documentation): MIT, see [LICENSE](LICENSE).
* `macos/*.nix`: derived from media-kit/libmpv-darwin-build, MIT, Copyright (c) 2023 birros
  ([macos/LICENSE-libmpv-darwin-build.txt](macos/LICENSE-libmpv-darwin-build.txt)); my changes are under the same
  licence.
* `macos/patches/*.patch`: changes to mpv, under mpv's licence (LGPL-2.1-or-later).
* The two Windows recipe files, `ffmpeg.cmake` and `mpv.cmake`, are modified copies of files of
  shinchiro/mpv-winbuild-cmake, which has no licence file. I asked under which licence they may be reused
  ([shinchiro/mpv-winbuild-cmake#855](https://github.com/shinchiro/mpv-winbuild-cmake/issues/855)). Until the answer,
  this repository does not copy them: the workflow fetches them from the commit of freeKC/Immuch360 where I wrote them,
  checked by SHA-256 (`windows/recipe-files.lock`). The sources archive of each release holds them with the rest of the
  recipe, since the LGPL asks for the scripts used to build the library. I will update this section when the answer
  comes.
* The binaries: GNU LGPL version 3 or later as built, each library keeping its own licence, see
  [NOTICES.md](NOTICES.md).

## Credits

* [mpv](https://github.com/mpv-player/mpv), [FFmpeg](https://ffmpeg.org) and the authors of every library listed in
  [NOTICES.md](NOTICES.md).
* shinchiro, for [mpv-winbuild-cmake](https://github.com/shinchiro/mpv-winbuild-cmake), the Windows recipe these builds
  come from, and its build container.
* Predidit, for keeping the video recipe building in
  [libmpv-win32-video-cmake](https://github.com/Predidit/libmpv-win32-video-cmake).
* The media-kit authors, for [media_kit](https://github.com/media-kit/media-kit),
  [libmpv-win32-video-cmake](https://github.com/media-kit/libmpv-win32-video-cmake) and
  [libmpv-darwin-build](https://github.com/media-kit/libmpv-darwin-build) (birros).

## Questions and problems

Please open an issue in this repository for anything about these builds. For Immuch360 itself, the place is
[github.com/freeKC/Immuch360/issues](https://github.com/freeKC/Immuch360/issues).

## Earlier builds

The builds made before this repository existed, from the same recipes, stay on the
[release page of freeKC/Immuch360](https://github.com/freeKC/Immuch360/releases) with their sources:
`libmpv-windows-20261009-3`, `libmpv-windows-20261020-10`, `libmpv-macos-20261020-9` and `libmpv-macos-20261020-10`.
`libmpv-macos-20261020-8` crashes in `mpv_create` (the crash the two mpv patches fix); please use a later one.
