from pathlib import Path

def generate_badge(score: int, output_path: Path):
    if score >= 80:
        color = "#4c1" # brightgreen
    elif score >= 60:
        color = "#dfb317" # yellow
    else:
        color = "#e05d44" # red
        
    # Basic SVG badge template similar to shields.io
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="130" height="20">
  <linearGradient id="b" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <clipPath id="a">
    <rect width="130" height="20" rx="3" fill="#fff"/>
  </clipPath>
  <g clip-path="url(#a)">
    <path fill="#555" d="M0 0h75v20H0z"/>
    <path fill="{color}" d="M75 0h55v20H75z"/>
    <path fill="url(#b)" d="M0 0h130v20H0z"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
    <text x="37.5" y="15" fill="#010101" fill-opacity=".3">repo-health</text>
    <text x="37.5" y="14">repo-health</text>
    <text x="101.5" y="15" fill="#010101" fill-opacity=".3">{score}/100</text>
    <text x="101.5" y="14">{score}/100</text>
  </g>
</svg>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
