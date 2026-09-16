# -*- coding: utf-8 -*-
"""Small static decay map for the intro gutter.
Same toy MC as the explorer: two-body decay, Lorentz boost, exponential decay law.
Transparent background and mid-tone colours so one file reads on light and dark."""
import math, os, random
random.seed(11235)

Z_MAX, R_MAX = 11.0, 7.6
CTAU, M_LLP, M_PARENT, PT_MEAN, Y_MAX = 1.0, 15.0, 125.25, 35.0, 2.0
N = 300

VOLUMES = [("tracker",(0,2.70),(0,1.10)), ("calo",(0,4.00),(1.29,2.95)),
           ("calo",(3.15,5.70),(0.30,2.95)), ("muon",(0,6.60),(4.00,7.38)),
           ("muon",(5.70,10.90),(0.90,7.00))]

# mid-tone hues: legible on white and on #12141a alike
COLOR = {"prompt":"#64748b","tracker":"#0284c7","calo":"#c2740a","muon":"#db2777","none":"#94a3b8"}
BANDS = [  # (z range, r range, hue, label)
    ((0,2.70),(0,1.10),   "#0284c7", "tracker"),
    ((0,4.00),(1.29,2.95),"#c2740a", "calo"),
    ((3.15,5.70),(0.30,2.95),"#c2740a", None),
    ((0,6.60),(4.00,7.38),"#db2777", "muon"),
    ((5.70,10.90),(0.90,7.00),"#db2777", None),
]

def boost(v,bx,by,bz):
    b2=bx*bx+by*by+bz*bz
    if b2<=0: return list(v)
    g=1/math.sqrt(1-b2); bp=bx*v[1]+by*v[2]+bz*v[3]; g2=(g-1)/b2
    return [g*(v[0]+bp), v[1]+g2*bp*bx+g*bx*v[0], v[2]+g2*bp*by+g*by*v[0], v[3]+g2*bp*bz+g*bz*v[0]]

def classify(x,y,z):
    if math.sqrt(x*x+y*y+z*z) < 5e-4: return "prompt"
    r,az = math.sqrt(x*x+y*y), abs(z)
    for vid,(z0,z1),(r0,r1) in VOLUMES:
        if z0<=az<=z1 and r0<=r<=r1: return vid
    return "none"

pStar = math.sqrt(M_PARENT**2/4 - M_LLP**2); eStar = M_PARENT/2
pts, tally = [], {}
for _ in range(N):
    pt = -PT_MEAN*math.log(1-random.random()*0.999)
    y  = (random.random()*2-1)*Y_MAX; phiP = random.random()*2*math.pi
    mt = math.sqrt(M_PARENT**2+pt*pt)
    P  = [mt*math.cosh(y), pt*math.cos(phiP), pt*math.sin(phiP), mt*math.sinh(y)]
    cth = random.random()*2-1; sth = math.sqrt(1-cth*cth); ph = random.random()*2*math.pi
    lab = boost([eStar, pStar*sth*math.cos(ph), pStar*sth*math.sin(ph), pStar*cth],
                P[1]/P[0], P[2]/P[0], P[3]/P[0])
    p = math.sqrt(lab[1]**2+lab[2]**2+lab[3]**2)
    L = (p/M_LLP)*CTAU*-math.log(1-random.random()*0.999999)
    x,yy,z = lab[1]/p*L, lab[2]/p*L, lab[3]/p*L
    reg = classify(x,yy,z)
    tally[reg] = tally.get(reg,0)+1
    pts.append((abs(z), math.sqrt(x*x+yy*yy), reg))

W,H = 360, 250
PADL, PADR, PADT, PADB = 22, 6, 8, 20
s = min((W-PADL-PADR)/Z_MAX, (H-PADT-PADB)/R_MAX)
X = lambda z: PADL + z*s
Y = lambda r: H - PADB - r*s

o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
     f'role="img" aria-label="Cross-section of one quadrant of the CMS detector with {N} simulated '
     f'long-lived particle decays at a proper lifetime of one metre, coloured by the detector region '
     f'that could observe them.">']

for (z0,z1),(r0,r1),hue,_ in BANDS:
    o.append(f'<rect x="{X(z0):.1f}" y="{Y(r1):.1f}" width="{(z1-z0)*s:.1f}" height="{(r1-r0)*s:.1f}" '
             f'fill="{hue}" fill-opacity="0.045" stroke="{hue}" stroke-opacity="0.42" stroke-width="0.9"/>')

# beam axis
o.append(f'<line x1="{X(0):.1f}" y1="{Y(0):.1f}" x2="{X(Z_MAX):.1f}" y2="{Y(0):.1f}" '
         f'stroke="#94a3b8" stroke-opacity="0.5" stroke-width="1" stroke-dasharray="3 3"/>')

# flight paths then vertices, batched per region
for grp in ("none","prompt","tracker","calo","muon"):
    sel = [q for q in pts if q[2]==grp and q[0]<=Z_MAX and q[1]<=R_MAX]
    if not sel: continue
    if grp != "none":
        d = "".join(f'M{X(0):.1f},{Y(0):.1f}L{X(z):.1f},{Y(r):.1f}' for z,r,_ in sel)
        o.append(f'<path d="{d}" stroke="{COLOR[grp]}" stroke-opacity="0.085" stroke-width="0.5" fill="none"/>')
    for z,r,_ in sel:
        rad = 1.7 if grp!="none" else 1.15
        op  = 0.95 if grp!="none" else 0.32
        o.append(f'<circle cx="{X(z):.1f}" cy="{Y(r):.1f}" r="{rad}" fill="{COLOR[grp]}" fill-opacity="{op}"/>')

o.append(f'<circle cx="{X(0):.1f}" cy="{Y(0):.1f}" r="2.6" fill="#0f172a" fill-opacity="0.75"/>')
o.append(f'<circle cx="{X(0):.1f}" cy="{Y(0):.1f}" r="2.6" fill="none" stroke="#94a3b8" stroke-width="0.8"/>')

F = 'font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="7.5" fill="#94a3b8"'
for rr in (0,2,4,6):
    o.append(f'<text x="{PADL-4:.1f}" y="{Y(rr)+2.6:.1f}" text-anchor="end" {F}>{rr}</text>')
o.append(f'<text x="{PADL-4:.1f}" y="{Y(R_MAX)+6:.1f}" text-anchor="end" {F}>r, m</text>')
for zz in (0,4,8):
    o.append(f'<text x="{X(zz):.1f}" y="{H-PADB+11:.1f}" text-anchor="middle" {F}>{zz}</text>')
o.append(f'<text x="{X(Z_MAX):.1f}" y="{H-PADB+11:.1f}" text-anchor="end" {F}>beam axis, m</text>')
o.append('</svg>')

open(os.path.join(os.path.dirname(__file__), "..", "assets", "img", "decay-map.svg"), "w").write("\n".join(o))
tot = sum(tally.values())
print("fractions:", {k: f"{v/tot*100:.0f}%" for k,v in sorted(tally.items())})
