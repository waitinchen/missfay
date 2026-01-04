#!/bin/bash
# Start script for Railway deployment
# Sets up library paths for google-generativeai

# Find gcc lib directory and add to LD_LIBRARY_PATH
if [ -d "/nix/store" ]; then
    # Find gcc lib directory in nix store
    GCC_LIB=$(find /nix/store -name "libstdc++.so.6" 2>/dev/null | head -1 | xargs dirname)
    if [ -n "$GCC_LIB" ]; then
        export LD_LIBRARY_PATH="$GCC_LIB:$LD_LIBRARY_PATH"
    fi
    
    # Find Python site-packages and add to PYTHONPATH
    PYTHON_SITE=$(python3 -c "import site; print(site.getsitepackages()[0])" 2>/dev/null)
    if [ -n "$PYTHON_SITE" ] && [ -d "$PYTHON_SITE" ]; then
        export PYTHONPATH="$PYTHON_SITE:$PYTHONPATH"
    fi
fi

# Verify google-generativeai is importable
python3 -c "import google.generativeai" 2>/dev/null || {
    echo "ERROR: google-generativeai not found in Python path"
    echo "Python path: $(python3 -c 'import sys; print(":".join(sys.path))')"
    echo "Trying to find installed packages..."
    python3 -m pip show google-generativeai || echo "Package not found via pip"
    exit 1
}

# Start the application
exec python3 -m uvicorn voice_bridge:app --host 0.0.0.0 --port ${PORT:-8000}
