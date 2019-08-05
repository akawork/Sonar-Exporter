## Sonar Exporter

Sonar exporter for Prometheus to deploy on FSOFT environment.
This exporter has written in python3.6.

*Sonar version 6.7.5.38563*

## Usage:

### Step 1: Build image

```sh
docker build -t sonar_exporter .
```

### Step 2: Running Sonar exporter

```sh
docker run -p 9118:9118 --name sonar_exporter -d \
-e "SONAR_SERVER=http://192.168.232.147:8080" \
-e "SONAR_USERNAME=admin" \
-e "SONAR_PASSWORD=123456" sonar_exporter
```

With:

- SONAR_SERVER: is the url of sonar
- SONAR_USERNAME: is the user of sonar who have permission to access sonar resource
- SONAR_PASSWORD: is the password of user.

### Using config file:
```sh
docker run -p 9118:9118 --name sonar_exporter -d \
-v "/link/to/your/config/file.ini:/root/config.ini" \
sonar_exporter
```