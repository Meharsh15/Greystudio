from pathlib import Path
import re

FILES = (
    Path("index.html"),
    Path("Greystudio_v4.html"),
    Path("Greystudio_v4_booking_integrated.html"),
)

REPLACEMENTS = (
    ("section{padding:clamp(64px,7vw,92px) 0;", "section{padding:clamp(54px,5.5vw,76px) 0;", "desktop section spacing"),
    ("section{padding:56px 0}", "section{padding:44px 0}", "mobile section spacing"),
    (".stage{position:relative;width:100%;min-height:340px;pointer-events:none}", ".stage{position:relative;width:100%;min-height:270px;pointer-events:none}", "desktop stage height"),
    (".mkhead .stage{min-height:420px}", ".mkhead .stage{min-height:320px}", "desktop fixer stage"),
    (".cstage{min-height:250px;margin-bottom:34px}", ".cstage{min-height:210px;margin-bottom:22px}", "desktop contact stage"),
    (".stage{min-height:250px}.story .stage{min-height:250px;margin-top:8px}.cstage{min-height:240px;margin-bottom:24px}", ".stage{min-height:200px}.story .stage{min-height:200px;margin-top:8px}.cstage{min-height:190px;margin-bottom:18px}", "mobile stages"),
    (".mkhead .stage{min-height:270px}", ".mkhead .stage{min-height:230px}", "mobile fixer stage"),
    ("function solve(s){\n  const vh=vh0, m=s+vh/2;", "function solve(s){\n  if(!stops.length||!stops[0]){tgt.op=0;return}\n  const vh=vh0, m=s+vh/2;", "scroll solver guard"),
    ("document.documentElement.classList.add('has3d');", "document.documentElement.classList.add('has3d');\n  window.__greystudio3dReady&&window.__greystudio3dReady();", "3D ready signal"),
    ("tgt.op=lerp(A.op,B.op,t)*(1-.85*ss(clamp((raw-.12)/.28,0,1))*ss(clamp((.88-raw)/.28,0,1)))*fin*fout*fnd;\n  const activeRange=m>=S.top+vh*.12 && s<footY-vh*.7 && !(fa<vh*.95 && fb>vh*.05);\n  if(activeRange)tgt.op=Math.max(tgt.op,mobile()?.88:1);",
     "tgt.op=lerp(A.op,B.op,t)*(1-.85*ss(clamp((raw-.12)/.28,0,1))*ss(clamp((.88-raw)/.28,0,1)))*fin*fout*fnd;",
     "remove forced 3D character visibility"),
)

WATCHDOG = """</script>
<script>
(()=>{let ready=false;const fail=()=>{if(!ready)document.documentElement.classList.add("no3d")};window.__greystudio3dReady=()=>{ready=true;document.documentElement.classList.remove("no3d")};window.addEventListener("error",e=>{if(e.target&&e.target.tagName==="SCRIPT"&&e.target.type==="module")fail()},true);window.addEventListener("unhandledrejection",fail);setTimeout(fail,18000)})();
</script>
<script type="application/ld+json">"""

SERVICE_CSS = """
/* Integrated service photography — kept inside the original Services section */
#services{position:relative;isolation:isolate;background:#050505}
#services .sv-media{height:104px;margin:0 0 20px;position:relative;overflow:hidden;border:1px solid rgba(255,255,255,.17);border-radius:10px;background:#0b0c0d}
#services .sv-media:after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,rgba(0,0,0,0) 48%,rgba(5,5,5,.42) 100%);box-shadow:inset 0 0 22px rgba(255,255,255,.035)}
#services .sv-media img{display:block;width:100%;height:100%;object-fit:cover;opacity:0;filter:saturate(.78) contrast(.96);transform:scale(1.045);transition:opacity .9s ease,transform 1.1s cubic-bezier(.2,.7,.2,1),filter .6s ease}
#services .sv.in .sv-media img{opacity:.78;transform:scale(1);filter:saturate(.84) contrast(1)}
#services .sv:hover .sv-media img{opacity:.98;transform:scale(1.07);filter:saturate(1) contrast(1.02)}
#services .sv-media img:focus{outline:2px solid #9edfff;outline-offset:-3px}
@media(max-width:560px){#services .sv-media{height:132px;margin-bottom:16px}}
@media(prefers-reduced-motion:reduce){#services .sv-media img{opacity:.82;transform:none;transition:none}}
"""

IMAGES = {
    "01": ('https://images.pexels.com/photos/39598359/pexels-photo-39598359.jpeg', "Advertising campaign creative"),
    "02": ('https://images.pexels.com/photos/10142683/pexels-photo-10142683.jpeg', "Brand identity and visual branding"),
    "04": ('https://images.pexels.com/photos/38059010/pexels-photo-38059010.jpeg', "Cinema camera for documentaries, brand films and advertisements"),
    "05": ('https://images.pexels.com/photos/18280160/pexels-photo-18280160.jpeg', "Newspaper publicity and media coverage"),
    "06": ('https://images.pexels.com/photos/6168/hands-woman-laptop-notebook.jpg', "Digital marketing and online campaign planning"),
    "07": ('https://images.pexels.com/photos/1181263/pexels-photo-1181263.jpeg', "Website development and digital experience"),
    "08": ('https://images.pexels.com/photos/9040531/pexels-photo-9040531.jpeg', "Content creation and production"),
}

def replace_once(source, old, new, label):
    if new in source:
        return source
    count = source.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return source.replace(old, new, 1)

def patch(path):
    source = path.read_text(encoding="utf-8")
    original = source

    # Undo the previous misplaced, duplicate service block and its standalone styling/script.
    source = re.sub(r'\s*<section class="gs-visual-services" id="creative-services-visuals".*?</section>\s*', '\n', source, count=1, flags=re.S)
    source = re.sub(r'\s*<style id="gs-service-visuals-css">.*?</style>\s*', '\n', source, count=1, flags=re.S)
    source = re.sub(r'\s*<script id="gs-service-visuals-js">.*?</script>\s*', '\n', source, count=1, flags=re.S)

    for old, new, label in REPLACEMENTS:
        if old in source:
            source = source.replace(old, new, 1)
        elif new not in source:
            raise RuntimeError(f"{path}: {label}: neither old nor new source found")

    # Keep the existing 3D error fallback, but do not force the character over service content.
    if "window.__greystudio3dReady=()=>{ready=true;" not in source:
        marker = '</script>\n<script type="application/ld+json">'
        source = replace_once(source, marker, WATCHDOG, "3D load watchdog")

    # Put the photo treatment into the site's original stylesheet.
    if "Integrated service photography" not in source:
        source = replace_once(source, "</style>", SERVICE_CSS + "\n</style>", "service image CSS")

    # Attach each supplied image to its matching existing service card, not to a new section.
    for number, (url, alt) in IMAGES.items():
        marker = f'<article class="sv rv'
        # Identify the exact existing card by its number marker.
        nmarker = f'<div class="n">{number}</div>'
        idx = source.find(nmarker)
        if idx < 0:
            if f'data-service-image="{number}"' in source:
                continue
            raise RuntimeError(f"{path}: service card {number} not found")
        card_start = source.rfind("<article", 0, idx)
        if card_start < 0:
            raise RuntimeError(f"{path}: article start for card {number} not found")
        open_end = source.find(">", card_start) + 1
        card_open = source[card_start:open_end]
        if f'data-service-image="{number}"' not in card_open:
            media = f'<div class="sv-media" data-service-image="{number}"><img src="{url}" alt="{alt}" loading="lazy" decoding="async"></div>'
            source = source[:open_end] + media + source[open_end:]

    # Make the photography card accurately communicate documentary and advertising production.
    source = source.replace("<h3>Photography</h3><p>Product, brand, business and campaign photography with a creative eye.</p>",
                            "<h3>Photography &amp; Cinematic Production</h3><p>Documentaries, brand films, advertisements and campaign photography.</p>", 1)

    # SEO metadata and machine-readable agency/service context for search and answer engines.
    description = "Greystudio is a Hyderabad creative and digital agency delivering cinematic documentaries, advertising, branding, photography, publicity, digital marketing, website development and content creation."
    if '<meta name="description"' in source:
        source = re.sub(r'<meta\\s+name=["\\']description["\\'][^>]*>', '<meta name="description" content="' + description + '">', source, count=1, flags=re.I)
    else:
        source = replace_once(source, "</head>", '<meta name="description" content="' + description + '">\\n</head>', "SEO meta description")
    canonical = '<link rel="canonical" href="https://www.greystudio.online/">'
    if 'rel="canonical"' not in source:
        source = replace_once(source, "</head>", canonical + "\\n</head>", "canonical URL")
    og = """<meta property="og:type" content="website">
<meta property="og:site_name" content="Greystudio.">
<meta property="og:title" content="Greystudio. | Creative &amp; Digital Agency in Hyderabad">
<meta property="og:description" content="Cinematic production, advertising, branding and digital growth for ambitious businesses.">
<meta property="og:url" content="https://www.greystudio.online/">
<meta name="twitter:card" content="summary_large_image">"""
    if 'property="og:title"' not in source:
        source = replace_once(source, "</head>", og + "\\n</head>", "Open Graph and social metadata")
    schema = """<script type="application/ld+json" id="greystudio-agency-schema">
{
  "@context": "https://schema.org",
  "@type": ["ProfessionalService", "AdvertisingAgency"],
  "name": "Greystudio.",
  "url": "https://www.greystudio.online/",
  "description": "Greystudio is a creative and digital agency in Hyderabad, India, offering cinematic documentary and advertising production, branding, photography, publicity and PR, digital marketing, website and app development, and content creation.",
  "areaServed": [{"@type":"City","name":"Hyderabad"},{"@type":"AdministrativeArea","name":"Telangana"}],
  "address": {"@type":"PostalAddress","addressLocality":"Hyderabad","addressRegion":"Telangana","postalCode":"500077","addressCountry":"IN"},
  "knowsAbout": ["Cinematic documentary production","Advertising campaigns","Brand identity and branding","Commercial photography","Publicity and public relations","Digital marketing","Website development","App development","Content creation"],
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Creative and digital agency services",
    "itemListElement": [
      {"@type":"OfferCatalog","name":"Cinematic production and documentaries"},
      {"@type":"OfferCatalog","name":"Advertising and campaign creative"},
      {"@type":"OfferCatalog","name":"Branding and graphic design"},
      {"@type":"OfferCatalog","name":"Photography and content creation"},
      {"@type":"OfferCatalog","name":"Publicity and public relations"},
      {"@type":"OfferCatalog","name":"Digital marketing"},
      {"@type":"OfferCatalog","name":"Website and app development"}
    ]
  }
}
</script>"""
    if 'id="greystudio-agency-schema"' not in source:
        source = replace_once(source, "</head>", schema + "\\n</head>", "agency structured data")

    # Keep the cinematic character visible on the opening view, then soften it behind the Services cards.
    opacity_marker = "tgt.op=lerp(A.op,B.op,t)*(1-.85*ss(clamp((raw-.12)/.28,0,1))*ss(clamp((.88-raw)/.28,0,1)))*fin*fout*fnd;"
    opacity_logic = opacity_marker + "\\n  // Hero: keep the character present from the first screen. Services: retain it as a subdued background layer.\\n  if(s < svcTop && s+vh>0) tgt.op=Math.max(tgt.op,.92);\\n  if(s+vh>svcTop && s<svcBot) tgt.op=Math.max(tgt.op,.34);"
    if "retain it as a subdued background layer" not in source:
        source = replace_once(source, opacity_marker, opacity_logic, "3D character hero and services visibility")
    # Ensure service content sits above the softened character, without hiding the character entirely.
    if "#services .wrap{position:relative;z-index:2}" not in source:
        source = replace_once(source, "/* Integrated service photography — kept inside the original Services section */", "/* Integrated service photography — kept inside the original Services section */\\n#services .wrap{position:relative;z-index:2}\\n.stage{z-index:0}", "service foreground layering")
    # Avoid duplicate 3D-ready callback calls from earlier patch passes.
    ready_call = "window.__greystudio3dReady&&window.__greystudio3dReady();"
    source = source.replace(ready_call + "\\n  " + ready_call, ready_call)

    if source != original:
        path.write_text(source, encoding="utf-8")
        return True
    return False

changed = []
for path in FILES:
    if path.exists() and patch(path):
        changed.append(str(path))

if changed:
    print("Integrated images into existing Services cards and removed misplaced section: " + ", ".join(changed))
else:
    print("Integrated service image layout is already present.")
