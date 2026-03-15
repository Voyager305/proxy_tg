#!/bin/bash
# Упаковка платформенных пакетов для GitHub Releases

VERSION="0.1.2"
DIST_DIR="dist"

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

pack() {
    local platform=$1
    local arch=$2
    local src="proxy_tg_${platform}_v${VERSION}"
    local archive="ProxyTg_v${VERSION}_${platform}_${arch}.zip"

    if [ ! -d "$src" ]; then
        echo "SKIP: $src not found"
        return
    fi

    echo "Packaging $src -> $archive"
    zip -r "$DIST_DIR/$archive" "$src" -x "*/__pycache__/*" "*/.DS_Store"
    echo "  Done: $(du -h "$DIST_DIR/$archive" | cut -f1)"
}

pack mac arm64
pack linux amd64
pack win amd64

echo ""
echo "Release archives:"
ls -lh "$DIST_DIR"/
echo ""
echo "Upload these to GitHub Releases:"
echo "  gh release create v${VERSION} $DIST_DIR/*.zip --title \"ProxyTg v${VERSION}\" --notes-file RELEASE_NOTES.md"
