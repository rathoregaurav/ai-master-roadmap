# Fixing `python3` Version on macOS (Apple Silicon)

## Problem

Running:

```bash
python3 --version
```

returned:

```text
Python 3.9.6
```

Although newer Python versions were already installed using Homebrew.

---

## Investigation

### Check which Python was being used

```bash
which python3
```

Output:

```text
/usr/bin/python3
```

This is the **Apple system Python**, which should **not** be modified or replaced.

---

### Check all available Python installations

```bash
which -a python3
```

Output:

```text
/usr/bin/python3
/opt/homebrew/bin/python3
```

Additional versions installed:

```bash
which -a python3.12
which -a python3.13
which -a python3.14
```

Output:

```text
/opt/homebrew/bin/python3.12
/opt/homebrew/bin/python3.13
/opt/homebrew/bin/python3.14
```

Verify Homebrew Python:

```bash
/opt/homebrew/bin/python3 --version
```

Output:

```text
Python 3.14.0
```

---

## Root Cause

The shell searches executables in the order specified by the `PATH` environment variable.

Current PATH contained:

```text
/usr/bin
...
/opt/homebrew/bin
```

Since `/usr/bin` appeared **before** `/opt/homebrew/bin`, the shell always selected Apple's Python.

---

## Check PATH

```bash
echo $PATH
```

---

## Check Shell Configuration

```bash
cat ~/.zshrc
```

`~/.zprofile` did not exist.

Current PATH configuration:

```bash
export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"
```

Notice that Homebrew's `bin` directory was never added to the beginning of PATH.

---

## Solution

Edit:

```bash
nano ~/.zshrc
```

Add near the top:

```bash
export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:$PATH"
export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"
```

Or combine into one line:

```bash
export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:/opt/homebrew/opt/postgresql@15/bin:$PATH"
```

Reload configuration:

```bash
source ~/.zshrc
hash -r
```

---

## Verify

```bash
which python3
python3 --version
```

Expected output:

```text
/opt/homebrew/bin/python3
Python 3.14.0
```

---

## Useful Commands

### Show current Python

```bash
which python3
python3 --version
```

### Show every installed Python

```bash
which -a python3
```

### Verify Homebrew Python

```bash
/opt/homebrew/bin/python3 --version
```

### Display PATH

```bash
echo $PATH
```

### Reload shell

```bash
source ~/.zshrc
hash -r
```

---

# Best Practice

- Never replace or modify `/usr/bin/python3`.
- Install Python using Homebrew.
- Keep `/opt/homebrew/bin` before `/usr/bin` in PATH.
- Use virtual environments for every project.

Example:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python --version
```