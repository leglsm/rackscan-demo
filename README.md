# RackScan

**Live demo:** https://leglsm.github.io/rackscan-demo/ · no login, opens with sample data

A rack-damage inspection tool that places every finding **on a 3D model of the warehouse racks**. You can see which upright or beam is damaged, how urgent it is and whether it has been fixed at a glance.

![RackScan screenshot](docs/screenshot.png)

> All data in this demo is fictional (site, rows, inspectors, issues). It is generated with a fixed seed by `scripts/generate_sample.py`. Photos are illustrations. The tool was inspired by real warehouse work. No company data is included.

---

## Problem

Rack damage came in as **photos**. The hard part was not taking the picture. It was knowing exactly where the damage was, and making sure it got tracked until it was repaired.

We benchmarked a commercial rack-inspection subscription, and it did not fit how the site worked:

- **Cost and speed:** about **$15,000 per year**. Adding a plant meant the vendor had to come on site to survey it first. App updates, support requests and even new user accounts were slow.
- **Abstract layout:** the vendor drew its own generic layout and used its own labels (row/bay tags such as `W-03`). Our people think in **SAP storage-bin codes**, so a vendor label did not tell anyone where to walk.
- **Real layouts are not uniform:** row lengths, bay counts and orientation change from row to row. A generic grid hides that.

## Approach

- **Built on the real floor plan:** in the original tool, racks are drawn over the plant's 2D CAD drawing row by row, irregularities included, and rendered as 3D racks.
- **Point, don't describe:** a damage report becomes a marker on the exact upright or beam. Urgent items blink, so the problem is visible before you read a single code.
- **Data entry at the location:** tap the component, then pick the component type and priority, add a note and attach a photo.
- **Priority with an action rule:** `Unload` (unload and isolate now), `High` (7 days), `Medium` (30 days), `Low` (monitor, 90 days). Due dates are computed automatically and overdue items are flagged. The rules are config values at the top of the script.
- **Close the loop:** status goes from Open to Scheduled to Repaired. The dashboard shows open issues, overdue items, repairs in the last 30 days and average days to repair.

## Result

- **Demonstrated to the site director** with a mock inspection case. The layout matches the actual plant and its location codes, so a blinking point on the 3D rack shows **where the problem is right away**, with no code lookup.
- **Positioned as an in-house replacement for a ~$15,000/year subscription.** Replacement is on hold until the current contract ends. Once it is replaced, a new site needs only a new layout drawing: no vendor survey, no per-site fee, and updates and user accounts are handled in-house.
- The original version was built with Next.js, TypeScript, Supabase (auth and data), Chart.js and PDF export, and hosted on Vercel.

## What this demo includes

| Area | Demo |
|---|---|
| Views | 3D isometric rack layout, front elevation per row (default on phones) |
| Issues | 46 fictional findings across 6 rows × 12 bays × 4 levels |
| Actions | Report damage on any upright or beam, attach a photo, schedule or mark repaired |
| Analytics | KPI cards, open issues by row and by component, filterable issue log |

**Simplifications compared with the original:** the demo uses a uniform grid instead of an irregular CAD-based layout, it has no login or database, and your edits reset when you reload the page. It is a single HTML file with no server, so it stays free to host.

## Repository

```
index.html                  # the demo (data embedded)
template.html               # same page with a __DATA__ placeholder
data/sample.json            # fictional inspection records
scripts/generate_sample.py  # fixed-seed sample generator
scripts/build_demo.py       # embeds data/sample.json into template.html -> index.html
docs/screenshot.png
```

Rebuild: `python scripts/generate_sample.py && python scripts/build_demo.py`

## Author

Daniel Eunggu Lee · Warehouse & Material Flow Optimization Engineer · [github.com/leglsm](https://github.com/leglsm)
