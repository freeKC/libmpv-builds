# Notices

## Files of this repository

| Files | Licence | Copyright |
|---|---|---|
| `.github/workflows/build.yml`, `windows/*` (`pin_sources.sh`, `fetch_recipe_files.py`, `sources.lock`, `recipe-files.lock`, `meson-requirements.txt`), `macos/apply_overlay.sh`, `macos/check_undefined.py`, `README.md`, `NOTICES.md` | MIT ([LICENSE](LICENSE)) | 2026 FreeKC |
| `macos/*.nix` | MIT ([macos/LICENSE-libmpv-darwin-build.txt](macos/LICENSE-libmpv-darwin-build.txt)) | 2023 birros (media-kit/libmpv-darwin-build), changes 2026 FreeKC |
| `macos/patches/*.patch` | LGPL-2.1-or-later, as mpv | changes to mpv by FreeKC |

Not in this repository: `ffmpeg.cmake` and `mpv.cmake` of the Windows recipe, modified copies of files of
shinchiro/mpv-winbuild-cmake (no licence file). The workflow fetches them by URL and SHA-256 from freeKC/Immuch360
(`windows/recipe-files.lock`), pending the answer to
[shinchiro/mpv-winbuild-cmake#855](https://github.com/shinchiro/mpv-winbuild-cmake/issues/855).

## The libraries of the releases

### Licence

* **mpv** is built with `-Dgpl=false`, which leaves out the files that are GPL only: the library is under the GNU
  Lesser General Public License version 2.1 or later (mpv's `Copyright` file).
* **FFmpeg** is configured without `--enable-gpl` or `--enable-nonfree`, and with `--enable-version3`. Its code is LGPL
  version 2.1 or later; `--enable-version3` makes FFmpeg as built "LGPL version 3 or later", the version of the LGPL
  that can be combined with the Apache-2.0 TLS library linked with it (OpenSSL 3 on Windows, Mbed TLS on macOS).
* **The other libraries** are under the LGPL 2.1 or later or under permissive licences, all of which can be combined
  under version 3 of the LGPL.

So `libmpv-2.dll` as a whole, and the macOS libmpv and FFmpeg frameworks, are distributed under the GNU Lesser General
Public License version 3 or later (https://www.gnu.org/licenses/lgpl-3.0.html, which adds to the GPL version 3,
https://www.gnu.org/licenses/gpl-3.0.html), each part keeping its own licence and copyright. The full licence texts are
in the `licenses/` folder of each Windows archive and in the `libmpv-macos-<tag>-licenses.tar.gz` file of each release.
The corresponding source is the `*-sources.tar.xz` file of the same release.

### Windows: libraries built into `libmpv-2.dll`

The list is that of the x64 build; arm64 has the same without the NVIDIA headers. The linker keeps only the code that
mpv and the enabled FFmpeg components reach, so some of them (marked "build only") contribute nothing to the file; they
are listed because their sources are part of the sources archive. `BUILDINFO-<arch>.txt` gives the commit of each.

| Project | Licence (SPDX) | Used for |
|---|---|---|
| mpv | LGPL-2.1-or-later (built with `-Dgpl=false`) | the player |
| FFmpeg | LGPL-2.1-or-later code, LGPL-3.0-or-later as configured | demuxing, decoding, network protocols, filters |
| libplacebo | LGPL-2.1-or-later | mpv's video renderer |
| FriBidi | LGPL-2.1-or-later | subtitle text direction |
| libsoxr | LGPL-2.1-or-later | audio resampling |
| libssh | LGPL-2.1-or-later | build only (SFTP protocol not enabled) |
| GNU libiconv | LGPL-2.1-or-later | character sets of subtitles |
| uchardet | MPL-1.1 OR GPL-2.0-or-later OR LGPL-2.1-or-later | subtitle encoding detection |
| libass | ISC | subtitles |
| FreeType | FTL OR GPL-2.0-or-later (used under the FTL) | fonts of subtitles |
| HarfBuzz | MIT | text shaping of subtitles |
| Fontconfig | MIT-style (Fontconfig `COPYING`) | font lookup |
| libunibreak | Zlib | line breaking of subtitles |
| Expat | MIT | Fontconfig configuration |
| Brotli | MIT | WOFF2 fonts, compression in OpenSSL |
| zlib-ng | Zlib | compression |
| bzip2 | bzip2-1.0.6 | compressed fonts in FreeType |
| Zstandard | BSD-3-Clause OR GPL-2.0-only (used under BSD-3-Clause) | compression in OpenSSL |
| libpng | libpng-2.0 | PNG glyphs of fonts |
| libjpeg-turbo | IJG AND BSD-3-Clause AND Zlib | JPEG screenshots |
| Little CMS 2 | MIT | colour management |
| OpenSSL | Apache-2.0 | HTTPS and TLS |
| dav1d | BSD-2-Clause | AV1 decoding |
| libxml2 | MIT | DASH manifests |
| Intel libvpl | MIT | Intel Quick Sync dispatch |
| libjxl | BSD-3-Clause | build only (JPEG XL not enabled) |
| Highway | Apache-2.0 OR BSD-3-Clause | build only (used by libjxl) |
| libwebp | BSD-3-Clause | build only (FFmpeg's own WebP decoder is used) |
| zimg, graphengine | WTFPL | build only (zscale filter not enabled) |
| libbs2b | MIT | build only (filter not enabled) |
| libmysofa | BSD-3-Clause | build only (filter not enabled) |
| Speex | BSD-3-Clause | build only (decoder not enabled) |
| Ogg, Vorbis, Opus (and its model data) | BSD-3-Clause | build only (FFmpeg's own decoders are used) |
| libmodplug | public domain | build only |
| SRT | MPL-2.0 | build only (protocol not enabled) |
| OpenAL Soft | LGPL-2.0-or-later | build only (OpenAL output disabled in mpv) |
| SDL2 | Zlib | FFmpeg's SDL output device |
| shaderc | Apache-2.0 | shader compilation for libplacebo |
| glslang | BSD-3-Clause, BSD-2-Clause, MIT, Apache-2.0 (glslang `LICENSE.txt`) | shader compilation |
| SPIRV-Tools | Apache-2.0 | shader compilation |
| SPIRV-Cross | Apache-2.0 | shader translation for Direct3D 11 |
| SPIRV-Headers | MIT | headers |
| Vulkan-Loader, Vulkan-Headers | Apache-2.0 | libplacebo's Vulkan support (mpv's Vulkan output disabled) |
| glad | MIT (generator) and Apache-2.0 (Khronos registry) | OpenGL loader of libplacebo |
| fast_float | Apache-2.0 OR BSL-1.0 OR MIT | number parsing in libplacebo |
| xxHash | BSD-2-Clause | hashing in libplacebo |
| ANGLE headers | BSD-3-Clause | EGL headers |
| AMF headers | MIT | AMD AMF, loaded at run time when present |
| nv-codec-headers | MIT | NVIDIA decoding, loaded at run time when present (x64) |
| AviSynth+ headers | GPL-2.0-or-later with a linking exception | build only (AviSynth not enabled) |
| mingw-w64 runtime and winpthreads | ZPL-2.1, MIT, BSD-3-Clause and public domain parts | C runtime start-up, threads |
| LLVM libc++, libunwind, compiler-rt | Apache-2.0 WITH LLVM-exception | C++ runtime |

### macOS: frameworks

`BUILDINFO-macos.txt` gives the version, URL and SHA-256 of the source archive of each.

| Framework | Project | Licence (SPDX) | Used for |
|---|---|---|---|
| `Mpv` | mpv | LGPL-2.1-or-later (built with `-Dgpl=false`) | the player |
| `Avcodec`, `Avfilter`, `Avformat`, `Avutil`, `Swresample`, `Swscale` | FFmpeg | LGPL-2.1-or-later code, LGPL-3.0-or-later as configured | demuxing, decoding (VideoToolbox), network protocols, filters |
| `Placebo` | libplacebo | LGPL-2.1-or-later | mpv's video renderer |
| `Fribidi` | GNU FriBidi | LGPL-2.1-or-later | subtitle text direction |
| `Uchardet` | uchardet | MPL-1.1 OR GPL-2.0-or-later OR LGPL-2.1-or-later | subtitle encoding detection |
| `Ass` | libass | ISC | subtitles |
| `Freetype` | FreeType | FTL OR GPL-2.0-or-later (used under the FTL) | fonts of subtitles |
| `Harfbuzz` | HarfBuzz | MIT | text shaping of subtitles |
| `Png16` | libpng | libpng-2.0 | PNG glyphs of fonts |
| `Dav1d` | dav1d | BSD-2-Clause | AV1 decoding |
| `Xml2` | libxml2 | MIT | DASH manifests |
| `Mbedtls`, `Mbedx509`, `Mbedcrypto` | Mbed TLS | Apache-2.0 | HTTPS and TLS |
| none (built in) | fast_float | Apache-2.0 OR BSL-1.0 OR MIT | number parsing in libplacebo (header only) |
| none (built in) | Vulkan-Headers | Apache-2.0 OR MIT | headers of libplacebo's Vulkan stubs (Vulkan is off) |

### Credits some of these licences ask for

* Portions of this software are copyright © The FreeType Project (https://freetype.org). All rights reserved.
* This software is based in part on the work of the Independent JPEG Group (Windows build).

## Recipes and tools used to build, not distributed in this repository

* [Predidit/libmpv-win32-video-cmake](https://github.com/Predidit/libmpv-win32-video-cmake), a fork of
  [media-kit/libmpv-win32-video-cmake](https://github.com/media-kit/libmpv-win32-video-cmake), itself a fork of
  [shinchiro/mpv-winbuild-cmake](https://github.com/shinchiro/mpv-winbuild-cmake): no licence file. The sources archive
  of each Windows release holds the recipe as it built the DLL.
* shinchiro's Arch Linux build container (`ghcr.io/shinchiro/archlinux`, a copy by digest at
  `ghcr.io/freekc/libmpv-build`), with LLVM and mingw-w64 built from the commits of `windows/sources.lock`.
* [media-kit/libmpv-darwin-build](https://github.com/media-kit/libmpv-darwin-build): MIT for its default and full
  flavors, Copyright (c) 2023 birros. The sources archive of each macOS release holds the recipe with the overlay.
* Nix, Xcode and GitHub's hosted runners.
