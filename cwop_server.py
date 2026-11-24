import json
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen

# Example APRS weather packet tail: c270s008g014t042r000p000b10142
WX_RE = re.compile(
    r"c(?P<dir>\d{3})s(?P<spd>\d{3})g(?P<gst>\d{3})t(?P<temp>-?\d{3})"
    r"(?:r(?P<rain1h>\d{3}))?.*?(?:b(?P<baro>\d{5}))?"
)

def fetch_cwop(station_id: str) -> dict:
    sid = station_id.strip().upper()
    url = f"https://findu.com/cgi-bin/raw.cgi?call={sid}&length=1"
    with urlopen(url, timeout=10) as resp:
        raw = resp.read().decode("utf-8", errors="ignore")

    m = WX_RE.search(raw)
    if not m:
        return {"station": sid, "error": "No recent APRS/CWOP weather packet found", "raw": raw.strip()}

    temp_f = int(m.group("temp"))
    wind_mph = int(m.group("spd")) * 1.15078
    gust_mph = int(m.group("gst")) * 1.15078
    baro_inhg = round(int(m.group("baro")) / 10.0 * 0.02953, 2) if m.group("baro") else None

    return {
        "station": sid,
        "wind_dir_deg": int(m.group("dir")),
        "wind_mph": round(wind_mph, 1),
        "gust_mph": round(gust_mph, 1),
        "temp_f": temp_f,
        "baro_inhg": baro_inhg,
        "raw": raw.strip()
    }

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/cwop":
            qs = parse_qs(parsed.query)
            sid = qs.get("station", ["EW9999"])[0]
            try:
                payload = fetch_cwop(sid)
            except Exception as exc:
                payload = {"station": sid, "error": str(exc)}
            body = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    print("CWOP bridge running on http://localhost:8085/cwop?station=EW9999")
    HTTPServer(("0.0.0.0", 8085), Handler).serve_forever()
