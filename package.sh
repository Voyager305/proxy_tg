#!/bin/bash
# Упаковка платформенных пакетов для GitHub Releases

VERSION="0.1.1"
DIST_DIR="dist"

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

declare -A ARCH
ARCH[mac]="arm64"
ARCH[linux]="amd64"
ARCH[win]="amd64"

for platform in mac linux win; do
    src="proxy_tg_${platform}_v${VERSION}"
    archive="ProxyTg_v${VERSION}_${platform}_${ARCH[$platform]}.zip"

    if [ ! -d "$src" ]; then
        echo "SKIP: $src not found"
        continue
    fi

    echo "Packaging $src -> $archive"
    zip -r "$DIST_DIR/$archive" "$src" -x "*/__pycache__/*" "*/.DS_Store"
    echo "  Done: $(du -h "$DIST_DIR/$archive" | cut -f1)"
done

echo ""
echo "Release archives:"
ls -lh "$DIST_DIR"/
echo ""
echo "Upload these to GitHub Releases:"
echo "  gh release create v${VERSION} $DIST_DIR/*.zip --title \"ProxyTg v${VERSION}\" --notes-file RELEASE_NOTES.md"
