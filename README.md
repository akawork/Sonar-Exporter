## Sonar Exporter

Sonar exporter is a exporter to get metrics of Sonar server, deployed on FSOFT environment.

Sonar exporter has written in python3. It's tested in Sonar version 	6.7.5.38563

*Note: We used **timestamp()** in **datetime** library not supported by python2, so make sure running Sonar exporter in python3 or newer*

## Usage:

### Step 1: Build image

```sh
docker build -t sonar_exporter .
```

### Step 2: Running Sonar exporter

```sh
docker run -p 9119:9119 --name sonar_exporter -d \
-e "SONAR_SERVER=http://sonar_server" \
-e "SONAR_USERNAME=example" \
-e "SONAR_PASSWORD=123456" sonar_exporter
```

With:

- SONAR_SERVER: is the url of sonar
- SONAR_USERNAME: is the user of sonar who have permission to access sonar resource
- SONAR_PASSWORD: is the password of user.

### *Or using config file:*
```sh
docker run -p 9119:9119 --name sonar_exporter -d \
-v "/link/to/your/config/file.ini:/root/config.ini" \
sonar_exporter
```

with ***config.ini:***
```ini
SONAR_SERVER=http://sonar_server
SONAR_USERNAME=example
SONAR_PASSWORD=123456
```