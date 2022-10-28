# Server Setup Guide

You can choose to run the server locally or connect with the server all ready running at: <br />
[https://bartender.hopto.org](https://bartender.hopto.org)

These steps are to run the back-end locally.

## 1. Installing Dependencies

### git
```bash
sudo apt-get install git
```

### python3
```bash
sudo apt-get install python3
```

### python3-pip
```bash
sudo apt-get install python3-pip
```

### sqlite3
```bash
sudo apt-get install sqlite3
```

## 2. Installing Python Libraries

### bottle + rich + requests + bs4 + html5lib
```bash
pip3 install -U bottle bottle rich requests bs4 html5lib
```

### bottle-sqlite
The `bottle-sqlite` library does not include `detect_types` which is needed for python `datetime` support.
I copied the source code and added this functionality.

```bash
pip3 install -U git+https://github.com/kkatayama/bottle-sqlite.git@master
```

## 3. Downloading Code Base

```bash
git clone https://gitlab.com/calumsiemer/bartend_backend.git
```

## 4. Running

```bash
cd bartend_backend

python3 server.py
```

# Getting Familiar with the Web Framework

Documentation and Usage Examples are located at the [README.md](README.md).

I recommend completing the [7 Workflows](README.md#getting-started) to get comfortable with using this framework.

