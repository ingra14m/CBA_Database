# CBA_Database
A web application for query CBA data

Final Project for the class in SJTU



## Environment

### python

```shell
conda create -n CBA-env python=3.7
conda activate CBA-env

git clone https://github.com/ingra14m/CBA_Database
cd CBA-Database
pip install -r requirements.txt
```

### mysql

```shell
CREATE USER 'cba2020'@'localhost' IDENTIFIED BY 'cba2020';
GRANT ALL ON *.* TO 'cba2020'@'localhost';
```

