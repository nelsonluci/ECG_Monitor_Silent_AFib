import json
import sys
 
import matplotlib.pyplot as plt

ecg, acc = [], []
with open(sys.argv[1]) as f:
    for line in f:
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get("type") == "ECG":
            ecg.extend(rec["data"]["data"])
        elif rec.get("type") == "ACC":
            acc.extend(rec["data"]["data"])

rows = 2 if acc else 1
fig, axes = plt.subplots(rows, 1, figsize=(13, 3.5 * rows), squeeze=False)

ax = axes[0][0]
ax.plot([i / 130 for i in range(len(ecg))], ecg, linewidth=0.7)
ax.set_title(f"Raw ECG ({len(ecg)} samples, 130 Hz)")
ax.set_xlabel("time (s)")
ax.set_ylabel("µV")

if acc:
    ax = axes[1][0]
    t = [i / 25 for i in range(len(acc))]
    for k, name in enumerate("xyz"):
        ax.plot(t, [s[k] for s in acc], linewidth=0.7, label=name)
    ax.set_title(f"Raw accelerometer ({len(acc)} samples, 25 Hz)")
    ax.set_xlabel("time (s)")
    ax.set_ylabel("mG")
    ax.legend()

fig.tight_layout()
plt.show()