# ECG_Monitor_Silent_AFib

## 1. One-time setup
 
### macOS
 
**1. Check your Python version.**
```bash
python3 --version
```
If it says 3.9 or lower (the Python that ships with macOS is 3.9), install a newer one:
```bash
brew install python
```
(or download it from [python.org](https://www.python.org/downloads/)).
 
**2. Create a virtual environment and install the Polar library.**
```bash
python3 -m venv ~/polar-env
~/polar-env/bin/python -m pip install "polar-python[cli]==1.1.1"
```
This creates a self-contained Python in `~/polar-env`. Every command in this README runs it by its full path (`~/polar-env/bin/python`), so it works even if you use Anaconda (see Troubleshooting).
 
**3. Give your terminal Bluetooth access.**
Go to **System Settings → Privacy & Security → Bluetooth** and turn it on for the app you run commands from (Terminal, iTerm, VS Code, etc.). Quit and reopen that app afterward.
 
### Windows
 
Install Python 3.10+ from [python.org](https://www.python.org/downloads/) and check **"Add python.exe to PATH"** during setup. Then, in **Command Prompt**:
```bat
py -3 -m venv %USERPROFILE%\polar-env
%USERPROFILE%\polar-env\Scripts\python -m pip install "polar-python[cli]==1.1.1"
```
In the commands below, replace `~/polar-env/bin/python` with `%USERPROFILE%\polar-env\Scripts\python` and put each command on one line. Windows uses `^` instead of `\` to continue a line.
 
> Record from **Command Prompt**, not Windows PowerShell. PowerShell 5's `>` saves files as UTF-16, which the analysis scripts can't read.
 
---

 
## 2. Find the strap
 
```bash
~/polar-env/bin/python -m polar_python scan --timeout 20
```
You should see something like `Polar H10 E1056921`. The 8 characters at the end are that strap's ID, printed on the sensor.
 
---
 
## 3. Record
 
```bash
~/polar-env/bin/python -m polar_python stream --name-contains "H10" \
  --stream ecg:sample_rate=130,resolution=14 \
  --stream acc:sample_rate=25,resolution=16,range=8 --duration 60 --json > ecg.jsonl
```
 
| Part | Meaning |
|---|---|
| `--stream ecg:sample_rate=130,resolution=14` | Raw ECG at 130 Hz (the H10's only ECG rate) |
| `--stream acc:sample_rate=25,resolution=16,range=8` | Accelerometer at 25 Hz, ±8 g. Used to flag movement |
| `--duration 60` | Record 60 seconds (`-1` = until you press Ctrl+C) |
| `--json > ecg.jsonl` | Save the output to `ecg.jsonl` |
 
**`>` overwrites the file.** Give each recording its own descriptive name, for example:
```bash
... --json > ecg_11172026_1734.jsonl
```
 
---
 
## What's in the file
 
One JSON object per line (JSON Lines):
 
- **Event lines:** `device_selected`, `connected`, `stream_config`, `streaming_started`, `streaming_completed`, `disconnected`.
- **ECG lines:** `{"type": "ECG", "data": {"timestamp": <ns>, "data": [<µV>, ...]}}`
  - About 73 samples per line (about 0.56 s), in **microvolts**, at about 130 Hz (the real rate varies by about ±2%).
  - `timestamp` is in nanoseconds and belongs to the **last** sample in the line.
- **ACC lines:** `{"type": "ACC", "data": {"timestamp": <ns>, "data": [[x, y, z], ...]}}`, in **milli-g**, 36 samples per line.
 
---
 
## Troubleshooting
 
| Problem | Fix |
|---|---|
| `No devices found matching 'polar'` | Disconnect the strap in Bluetooth settings, close Polar apps on phones, wet the electrodes and wear it, then scan again with `--timeout 20`. If **no** devices show up at all, your terminal doesn't have Bluetooth permission (see setup step 2). |
| `No module named polar_python` | You ran a different Python (usually Anaconda's `(base)`). Use the full path `~/polar-env/bin/python`, or run `conda deactivate` first. |
| `ModuleNotFoundError` for other packages | Install it into the same environment: `~/polar-env/bin/python -m pip install <package>` |
 
---

