# HRV KYTO

Extract HRV data from KYTO device via bluetooth


## Installation
Prerequisites:
- `mamba` (**recommended**) or `conda`
- Tested on Linux. MacOS may require granting permission for bluetooth access

```
mamba env create -f environment.yml
```


## Usage

```bash
# Activate environment
mamba activate hrv-kyto
```

### Discover bluetooth devices for heart rate measurement

```bash
python -m src.discover

# Example output
# [2023-04-15 15:49:31] [INFO] [discover.py:30] [root] 18:45:16:A0:46:36 BT_HRM_9_a04636

```

### Connect and listen to transmitted heart rate measurment data
```bash
python -m src.connect --address 18:45:16:A0:46:36 --duration 300

# Example output:
# [2023-04-15 15:50:58] [INFO] [hrv_data_aggregator.py:33] [root] HRVPacket(timestamp=1681563058988, HR=43, RRs=[1071, 967])
# [2023-04-15 15:51:00] [INFO] [hrv_data_aggregator.py:33] [root] HRVPacket(timestamp=1681563060969, HR=43, RRs=[1395])
```
