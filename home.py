from flask import request
import maxminddb
from template import get_layout


def get_ip():
    if request.headers.get("X-Forwarded-For"):
        return request.headers.get("X-Forwarded-For").split(",")[0].strip()
    return request.remote_addr


def is_local_ip(ip):
    if ip.startswith("127.") or ip == "::1":
        return True
    if ip.startswith("192.168."):
        return True
    if ip.startswith("10."):
        return True
    if ip.startswith("172."):
        second = int(ip.split(".")[1])
        if 16 <= second <= 31:
            return True


@get_layout
def home():
    ip = get_ip()
    if is_local_ip(ip):
        return "You have a local ip, baka"
    db_path = "geolite2-city-ipv4.mmdb"
    if ":" in ip:
        db_path = "geolite2-city-ipv6.mmdb"
    try:
        with maxminddb.open_database(db_path) as reader:
            city = reader.get(ip)

        with maxminddb.open_database("geolite2-asn.mmdb") as reader:
            asn = reader.get(ip)
    except Exception:
        return "Congrat, something is broken, either your ip is not in the database or I fuck up the code"
    return (
        f"Hello {ip}"
        "You are located at"
        f" {city.get('country_code')}"
        f" {city.get('state1')}"
        f" {city.get('postcode')}"
        f" using  {asn.get('autonomous_system_organization')}"
    )
