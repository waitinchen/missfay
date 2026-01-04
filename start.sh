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
fi

# Start the application
exec python3 -m uvicorn voice_bridge:app --host 0.0.0.0 --port ${PORT:-8000}
