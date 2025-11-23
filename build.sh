#!/usr/bin/bash
set -e
rm -f *.mmdb
wget https://cdn.jsdelivr.net/npm/@ip-location-db/geolite2-city-mmdb/geolite2-city-ipv4.mmdb
wget https://cdn.jsdelivr.net/npm/@ip-location-db/geolite2-asn-mmdb/geolite2-asn-ipv4.mmdb
git pull
sudo docker compose down
sudo docker compose build
sudo docker compose up -d
