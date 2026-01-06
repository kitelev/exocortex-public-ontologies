#!/bin/bash
# Generate WebVOWL JSON from TTL files
# Requires: Java, OWL2VOWL JAR (built from source)
#
# Usage:
#   ./scripts/generate_webvowl.sh           # Generate for all exo/ems
#   ./scripts/generate_webvowl.sh exo       # Generate for specific ontology
#   ./scripts/generate_webvowl.sh exo ems   # Generate for multiple

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
OWL2VOWL_JAR="$REPO_ROOT/tools/OWL2VOWL/target/OWL2VOWL-0.3.7-shaded.jar"
EXPORTS_DIR="$REPO_ROOT/docs/exports"
WEBVOWL_DATA_DIR="$REPO_ROOT/docs/webvowl/data"

# Java flags for module system compatibility
JAVA_FLAGS="--add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/java.lang.reflect=ALL-UNNAMED"

# Check if OWL2VOWL JAR exists
if [ ! -f "$OWL2VOWL_JAR" ]; then
    echo "Error: OWL2VOWL JAR not found at $OWL2VOWL_JAR"
    echo ""
    echo "To build OWL2VOWL from source:"
    echo "  cd $REPO_ROOT/tools"
    echo "  git clone https://github.com/VisualDataWeb/OWL2VOWL.git"
    echo "  cd OWL2VOWL"
    echo "  mvn package -Denv=standalone -DskipTests"
    exit 1
fi

# Default ontologies to process
if [ $# -eq 0 ]; then
    ONTOLOGIES="exo ems"
else
    ONTOLOGIES="$*"
fi

echo "Generating WebVOWL JSON..."
echo ""

for ont in $ONTOLOGIES; do
    TTL_FILE="$EXPORTS_DIR/$ont.ttl"
    JSON_FILE="$WEBVOWL_DATA_DIR/$ont.json"
    ONT_JSON_FILE="$REPO_ROOT/docs/ontology/$ont/webvowl.json"

    if [ ! -f "$TTL_FILE" ]; then
        echo "Warning: $TTL_FILE not found, skipping"
        continue
    fi

    echo "Converting $ont.ttl -> $ont.json"

    java $JAVA_FLAGS -jar "$OWL2VOWL_JAR" \
        -file "$TTL_FILE" \
        -output "$JSON_FILE" 2>/dev/null

    # Also copy to ontology-specific directory
    if [ -d "$(dirname "$ONT_JSON_FILE")" ]; then
        cp "$JSON_FILE" "$ONT_JSON_FILE"
        echo "  -> Copied to docs/ontology/$ont/webvowl.json"
    fi

    echo "  -> Done: $(wc -c < "$JSON_FILE" | tr -d ' ') bytes"
done

echo ""
echo "WebVOWL JSON generation complete!"
