from pathlib import Path

FILES = (
    Path("index.html"),
    Path("Greystudio_v4.html"),
    Path("Greystudio_v4_booking_integrated.html"),
)

REPLACEMENTS = (
    (
        "section{padding:clamp(64px,7vw,92px) 0;",
        "section{padding:clamp(54px,5.5vw,76px) 0;",
        "desktop section spacing",
    ),
    ("section{padding:56px 0}", "section{padding:44px 0}", "mobile section spacing"),
    (
        ".stage{position:relative;width:100%;min-height:340px;pointer-events:none}",
        ".stage{position:relative;width:100%;min-height:270px;pointer-events:none}",
        "desktop stage height",
    ),
    (".mkhead .stage{min-height:420px}", ".mkhead .stage{min-height:320px}", "desktop fixer stage"),
    (
        ".cstage{min-height:250px;margin-bottom:34px}",
        ".cstage{min-height:210px;margin-bottom:22px}",
        "desktop contact stage",
    ),
    (
        ".stage{min-height:250px}.story .stage{min-height:250px;margin-top:8px}.cstage{min-height:240px;margin-bottom:24px}",
        ".stage{min-height:200px}.story .stage{min-height:200px;margin-top:8px}.cstage{min-height:190px;margin-bottom:18px}",
        "mobile stages",
    ),
    (".mkhead .stage{min-height:270px}", ".mkhead .stage{min-height:230px}", "mobile fixer stage"),
    (
        "function solve(s){\n  const vh=vh0, m=s+vh/2;",
        "function solve(s){\n  if(!stops.length||!stops[0]){tgt.op=0;return}\n  const vh=vh0, m=s+vh/2;",
        "scroll solver guard",
    ),
    (
        "tgt.op=lerp(A.op,B.op,t)*(1-.85*ss(clamp((raw-.12)/.28,0,1))*ss(clamp((.88-raw)/.28,0,1)))*fin*fout*fnd;",
        "tgt.op=lerp(A.op,B.op,t)*(1-.85*ss(clamp((raw-.12)/.28,0,1))*ss(clamp((.88-raw)/.28,0,1)))*fin*fout*fnd;\n  const activeRange=m>=S.top+vh*.12 && s<footY-vh*.7 && !(fa<vh*.95 && fb>vh*.05);\n  if(activeRange)tgt.op=Math.max(tgt.op,mobile()?.88:1);",
        "character visibility fallback",
    ),
    (
        "document.documentElement.classList.add('has3d');",
        "document.documentElement.classList.add('has3d');\n  window.__greystudio3dReady&&window.__greystudio3dReady();",
        "3D ready signal",
    ),
)

WATCHDOG = """</script>
<script>
(()=>{let ready=false;const fail=()=>{if(!ready)document.documentElement.classList.add("no3d")};window.__greystudio3dReady=()=>{ready=true;document.documentElement.classList.remove("no3d")};window.addEventListener("error",e=>{if(e.target&&e.target.tagName==="SCRIPT"&&e.target.type==="module")fail()},true);window.addEventListener("unhandledrejection",fail);setTimeout(fail,18000)})();
</script>
<script type="application/ld+json">"""

def apply_once(source: str, old: str, new: str, label: str) -> str:
    if new in source:
        return source
    count = source.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return source.replace(old, new, 1)

changed = []
for path in FILES:
    if not path.exists():
        continue
    source = path.read_text(encoding="utf-8")
    original = source
    for old, new, label in REPLACEMENTS:
        source = apply_once(source, old, new, label)

    if "window.__greystudio3dReady=()=>{ready=true;" not in source:
        marker = '</script>\n<script type="application/ld+json">'
        source = apply_once(source, marker, WATCHDOG, "module-load watchdog")

    if source != original:
        path.write_text(source, encoding="utf-8")
        changed.append(str(path))

if not changed:
    print("Homepage already contains the 3D and spacing fixes.")
else:
    print("Patched: " + ", ".join(changed))
