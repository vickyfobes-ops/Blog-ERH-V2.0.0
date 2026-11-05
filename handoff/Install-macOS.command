#!/bin/bash
set -e
package_dir="$(cd -- "$(dirname -- "$0")" && pwd)"
bundled_python="${HOME}/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
if [ -x "$bundled_python" ]; then
  runner="$bundled_python"
elif command -v python3 >/dev/null 2>&1; then
  runner="$(command -v python3)"
else
  echo 'Python not found. Open this folder in Codex and use the installation prompt.'
  exit 1
fi
"$runner" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else "Python 3.10+ required; ask Codex to use its bundled Python.")'
"$runner" "$package_dir/verify_package.py"
"$runner" "$package_dir/blog-erh-v2-0-0/scripts/install_local.py" --replace "$@"
echo 'Installation complete. Send your topic to Codex in the next message.'
if [ -t 0 ]; then read -r -p 'Press Enter to close.'; fi
