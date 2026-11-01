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

SERVICE_STYLE = """<style id="gs-service-visuals-css">
.gs-visual-services{position:relative;isolation:isolate;padding:clamp(64px,8vw,112px) max(24px,calc((100vw - 1240px)/2));background:linear-gradient(180deg,rgba(255,255,255,.015),rgba(255,255,255,0));overflow:hidden}
.gs-visual-services:before{content:"";position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at 50% 0%,rgba(65,135,190,.12),transparent 58%);z-index:-1}
.gs-vs-head{max-width:760px;margin:0 0 34px}
.gs-vs-eyebrow{display:block;color:#9edfff;font-size:11px;letter-spacing:.22em;text-transform:uppercase;font-weight:700;margin-bottom:12px}
.gs-vs-title{font-size:clamp(30px,4.3vw,54px);line-height:1.05;letter-spacing:-.045em;color:#f7f7f7;margin:0 0 12px}
.gs-vs-copy{max-width:620px;color:rgba(245,248,250,.68);font-size:16px;line-height:1.65;margin:0}
.gs-vs-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.gs-vs-card{position:relative;min-height:255px;border:1px solid rgba(255,255,255,.22);border-radius:18px;overflow:hidden;background:#111;isolation:isolate;opacity:0;transform:translateY(26px);filter:blur(5px);transition:opacity .85s ease,transform .85s cubic-bezier(.2,.7,.2,1),filter .85s ease,border-color .35s ease,box-shadow .35s ease}
.gs-vs-card.is-visible{opacity:1;transform:translateY(0);filter:blur(0)}
.gs-vs-card:after{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(0,0,0,.04) 8%,rgba(0,0,0,.12) 36%,rgba(0,0,0,.88) 100%)}
.gs-vs-card img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.76;transform:scale(1.025);transition:transform 1.1s cubic-bezier(.2,.7,.2,1),opacity .6s ease}
.gs-vs-card:hover{border-color:rgba(142,213,255,.72);box-shadow:0 18px 55px rgba(0,0,0,.34)}
.gs-vs-card:hover img{transform:scale(1.09);opacity:.94}
.gs-vs-card-content{position:absolute;z-index:2;left:20px;right:20px;bottom:19px}
.gs-vs-card h3{font-size:19px;line-height:1.2;letter-spacing:-.025em;color:#fff;margin:0 0 6px}
.gs-vs-card p{font-size:13px;line-height:1.45;color:rgba(255,255,255,.76);margin:0}
.gs-vs-card .gs-vs-index{display:block;color:#9edfff;font-size:10px;letter-spacing:.18em;margin-bottom:8px}
@media(max-width:900px){.gs-vs-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.gs-vs-card{min-height:230px}.gs-vs-card-content{left:15px;right:15px;bottom:15px}}
@media(max-width:520px){.gs-visual-services{padding:58px 16px}.gs-vs-grid{grid-template-columns:1fr}.gs-vs-card{min-height:245px}.gs-vs-title{font-size:34px}}
@media(prefers-reduced-motion:reduce){.gs-vs-card,.gs-vs-card img{transition:none;filter:none;transform:none}.gs-vs-card{opacity:1}}
</style>"""

SERVICE_SECTION = """<section class="gs-visual-services" id="creative-services-visuals" aria-labelledby="gs-vs-title">
  <div class="gs-vs-head">
    <span class="gs-vs-eyebrow">GREYSTUDIO · CREATIVE & DIGITAL</span>
    <h2 class="gs-vs-title" id="gs-vs-title">Ideas deserve to be seen.</h2>
    <p class="gs-vs-copy">From cinematic brand stories to digital experiences, we create the visuals and tools that help businesses stand out.</p>
  </div>
  <div class="gs-vs-grid">
    <article class="gs-vs-card"><img src="https://images.pexels.com/photos/38059010/pexels-photo-38059010.jpeg" alt="Professional cinema camera for documentary and commercial production" loading="lazy" decoding="async"><div class="gs-vs-card-content"><span class="gs-vs-index">01 / PRODUCTION</span><h3>Cinematic Production</h3><p>Documentaries, brand films and advertisements.</p></div></article>
    <article class="gs-vs-card"><img src="https://images.pexels.com/photos/39598359/pexels-photo-39598359.jpeg" alt="Creative advertising campaign visual" loading="lazy" decoding="async"><div class="gs-vs-card-content"><span class="gs-vs-index">02 / CAMPAIGNS</span><h3>Advertising</h3><p>Campaigns designed to capture attention.</p></div></article>
    <article class="gs-vs-card"><img src="https://images.pexels.com/photos/10142683/pexels-photo-10142683.jpeg" alt="Premium brand identity and printed branding" loading="lazy" decoding="async"><div class="gs-vs-card-content"><span class="gs-vs-index">03 / IDENTITY</span><h3>Branding</h3><p>Build a clear, memorable brand identity.</p></div></article>
    <article class="gs-vs-card"><img src="https://images.pexels.com/photos/18280160/pexels-photo-18280160.jpeg" alt="Woman reading a newspaper, representing media publicity" loading="lazy" decoding="async"><div class="gs-vs-card-content"><span class="gs-vs-index">04 / VISIBILITY</span><h3>Publicity</h3><p>Media presence, PR and brand visibility.</p></div></article>
    <article class="gs-vs-card"><img src="https://images.pexels.com/photos/6168/hands-woman-laptop-notebook.jpg" alt="Digital marketing work on a laptop" loading="lazy" decoding="async"><div class="gs-vs-card-content"><span class="gs-vs-index">05 / GROWTH</span><h3>Digital Marketing</h3><p>Grow reach, engagement and qualified leads.</p></div></article>
    <article class="gs-vs-card"><img src="https://images.pexels.com/photos/1181263/pexels-photo-1181263.jpeg" alt="Website development and digital interface work" loading="lazy" decoding="async"><div class="gs-vs-card-content"><span class="gs-vs-index">06 / DIGITAL</span><h3>Website Development</h3><p>Fast, modern and search-ready websites.</p></div></article>
    <article class="gs-vs-card"><img src="https://images.pexels.com/photos/9040531/pexels-photo-9040531.jpeg" alt="Content creator producing visual content" loading="lazy" decoding="async"><div class="gs-vs-card-content"><span class="gs-vs-index">07 / STORYTELLING</span><h3>Content Creation</h3><p>Photos, videos and social-first content.</p></div></article>
  </div>
</section>"""

REVEAL_SCRIPT = """<script id="gs-service-visuals-js">
(()=>{const cards=document.querySelectorAll('.gs-vs-card');if(!cards.length)return;if(!('IntersectionObserver'in window)){cards.forEach(c=>c.classList.add('is-visible'));return}const io=new IntersectionObserver(entries=>entries.forEach(entry=>{entry.target.classList.toggle('is-visible',entry.isIntersecting)}),{threshold:.14,rootMargin:'0px 0px -5% 0px'});cards.forEach((card,i)=>{card.style.transitionDelay=(i%4)*90+'ms';io.observe(card)})})();
</script>"""

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

    if 'id="gs-service-visuals-css"' not in source:
        source = apply_once(source, "</head>", SERVICE_STYLE + "\n</head>", "service visual styles")
    if 'id="creative-services-visuals"' not in source:
        marker = "</footer>" if "</footer>" in source else "</body>"
        if marker == "</footer>":
            source = source.replace(marker, SERVICE_SECTION + "\n" + marker, 1)
        else:
            source = apply_once(source, marker, SERVICE_SECTION + "\n" + marker, "service visual section")
    if 'id="gs-service-visuals-js"' not in source:
        source = apply_once(source, "</body>", REVEAL_SCRIPT + "\n</body>", "service reveal animation")

    if source != original:
        path.write_text(source, encoding="utf-8")
        changed.append(str(path))

if not changed:
    print("Homepage already contains the 3D, spacing and service visual updates.")
else:
    print("Patched: " + ", ".join(changed))
