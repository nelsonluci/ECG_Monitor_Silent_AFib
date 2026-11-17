# How to run plot

```
~/polar-env/bin/python plot.py sample_ecgs/ecg_20261116_191122.jsonl
```
---
# Planned work - Back End
* Need continuing ECG recording: Potentially save off a jsonl or csv file every hour so one data set does not get overwhelmed with data.
* Real time AFib flagging: ECG is runninh AFib algorithm checks in real time. If AFib is detected, the segment of the file is flagged somehow and the filename includes "_AFIB_DETECTED" at the end.
* Do we want post processing AFib detection (once an hour) or real time?
* Signal processing techniques that will reduce noise as much as possible, currently its almost unusable when the wearer is moving. 

# Planned Work - Front End
* The user notifies the backend when they are wearing the device, backend knows to begin recording.
* The application sends a notification when AFib is detected with the file in which the AFib has been detected.
* There is also a history tab with every ECG recording and their timestamps, so the patient has the option of sending any ECG to their provider.
