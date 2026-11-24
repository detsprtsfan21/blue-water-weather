# Blue Water & Thumb Weather + Jet Stream Command (PWA)

Deployable web, Android, and iOS Progressive Web App combining:
1. **7-Model + WeatherNext 2 AI Consensus Forecast** anchored around ZIP `48049` (Ruby / North Street, MI) with Lake Huron onshore fetch and 850 hPa $\Delta T$ instability tracking.
2. **Real-Time Surface Telemetry:** Supports NWS/AWOS METAR feeds (`KPHN`, `KMTC`, `KFNT`, `KDTW`, `KPTK`), Weather Underground Personal Weather Stations (PWS), and a zero-dependency Python CWOP/APRS bridge (`cwop_server.py`).
3. **Cloud Base Indicator (LCL) & Surface Frost Risk:** Computes Lifted Condensation Level ceiling in feet AGL (`VFR` / `MVFR` / `IFR`) and bridge-deck radiational frost alerts.
4. **Cross-Border US + Canadian Radar with Animated Scrubber:** Blends Environment Canada MSC GeoMet WMS (`RADAR_1KM_RRAI`, `RADAR_1KM_RSNO`, and `Radar_1km_dBZ-Extrapolation` from Exeter `CASET`) with US NEXRAD/RainViewer tiles and RRFS simulated reflectivity (`dBZ`).
5. **North America Jet Stream & Flight Speed Simulator:** Visualizes 300/250/200 hPa jet stream vectors across North America, samples 3 great-circle waypoints along your route, compares True Airspeed vs. Ground Speed, runs a $\pm 3$-hour departure window optimizer, and projects 7-day daily arrival deltas.

## Quick Deploy to GitHub Pages
1. Upload `index.html`, `manifest.json`, `sw.js`, `cwop_server.py`, and `README.md` to your GitHub repository root.
2. In GitHub, open **Settings → Pages**, select **Deploy from a branch** (`main` / `root`), and save.
3. Open your live `https://<username>.github.io/<repo>/` URL on Android Chrome or iOS Safari and tap **Add to Home Screen** to install as a standalone app.

## Optional Local CWOP / APRS Bridge
Run on your PC or Raspberry Pi to feed raw APRS/CWOP packets into the dashboard:
```bash
python3 cwop_server.py
```
