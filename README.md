Sonar Exporter

Sonar exporter for Prometheus to deploy on FSOFT environment.
This exporter have written in python3.6.

Usage:

1. Download newest version of sonar_exporter-?.tar.gz
2. Build image:
   
   2.1. Install docker:
      - [Install Docker on macOS](https://runnable.com/docker/install-docker-on-macos)
      - [Install Docker on Windows 10](https://runnable.com/docker/install-docker-on-windows-10)
      - [Install Docker on Linux](https://runnable.com/docker/install-docker-on-linux)

   2.2. Load docker image:
      ```sh
      $ docker load -i sonar_exporter-?.tar.gz
      ```
3. Run sonar Exporter by docker:
   ```sh
   $ docker run -p 9119:9119 -d sonar_exporter \
     [-s --server <sonar server url>] \
     [--user <sonar username>] \
     [--passwd <sonar password>] \
     [-p --port <display metrics port>]
   ```

   - docker
      - `-p`: connect docker port to real port
      - `-d`: run as a process
   - sonar_exporter
      - `-s --server`: targer sonar server
      - `--user`: username for authentication
      - `--passwd`: password for authentication
      - `p --port`: port to display metrics