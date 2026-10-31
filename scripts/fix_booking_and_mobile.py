# Apply responsive CTA and booking-resilience fixes to the current production HTML.
from pathlib import Path

MAIN = Path("index.html")
BOOK = Path("book/index.html")
CALENDLY = "https://calendly.com/greystudio-crew/30-min-meeting"
WA = "https://wa.me/916281256601?text=Hi%20Greystudio%2C%20I%27d%20like%20to%20start%20a%20project."

def once(source, old, new, label):
    n = source.count(old)
    if n != 1:
        raise RuntimeError(f"{label}: expected one match, got {n}")
    return source.replace(old, new, 1)

# Homepage: order actions so call booking sits left and WhatsApp right on mobile.
html = MAIN.read_text(encoding="utf-8")
html = once(
    html,
    '<a class="btn o nav-whatsapp" href="' + WA + '" target="_blank" rel="noopener">WhatsApp Us</a><a class="btn p nav-book" href="/book" aria-label="Book a free 30-minute consultation">Book a Call <span aria-hidden="true">↗</span></a>',
    '<a class="btn p nav-book" href="/book" aria-label="Book a free 30-minute consultation">Book a Call <span aria-hidden="true">↗</span></a><a class="btn o nav-whatsapp" href="' + WA + '" target="_blank" rel="noopener">WhatsApp Us</a>',
    "header CTA order",
)
html = once(
    html,
    '@media(max-width:560px){.nav-book{padding:10px 13px;font-size:13px}.book-strip{padding:18px}.book-strip .btn{width:100%;justify-content:center}.book-float{right:14px;bottom:calc(84px + env(safe-area-inset-bottom,0px))}}',
    '@media(max-width:560px){nav{gap:8px}.logo{font-size:26px;letter-spacing:-2px}.nav-book,.nav-whatsapp{display:inline-flex;padding:9px 10px;font-size:12px;white-space:nowrap}.nav-book{order:2}.nav-whatsapp{order:3}.book-strip{padding:18px}.book-strip .btn{width:100%;justify-content:center}.book-float{right:14px;bottom:calc(84px + env(safe-area-inset-bottom,0px))}}\n@media(max-width:380px){nav{gap:6px}.logo{font-size:23px}.nav-book,.nav-whatsapp{padding:8px 7px;font-size:11px}}',
    "mobile header sizing",
)
MAIN.write_text(html, encoding="utf-8")

# Booking page: make Calendly fail gracefully and always expose a direct booking link.
book = BOOK.read_text(encoding="utf-8")
book = once(
    book,
    '.bookfb a{color:var(--c2);text-decoration:underline}',
    '.bookfb a{color:var(--c2);text-decoration:underline}\n.bookfallback{display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap;padding:22px 26px;border-top:1px solid var(--line);background:rgba(53,201,255,.06)}\n.bookfallback p{color:var(--muted);margin:0}\n.bookfallback .btn{white-space:nowrap}\n.bookstatus{padding:12px 26px;color:var(--muted);font-size:13px}\n.bookstatus[hidden]{display:none}',
    "booking fallback styles",
)
book = once(
    book,
    '<div class="calendly-inline-widget" data-url="https://calendly.com/greystudio-crew/30-min-meeting?hide_gdpr_banner=1&amp;background_color=0b0c0d&amp;text_color=f7f7f7&amp;primary_color=35c9ff" style="min-width:320px;height:700px;"></div>\n<script type="text/javascript" src="https://assets.calendly.com/assets/external/widget.js" async></script>\n<!-- Calendly inline widget end -->\n<noscript><p class="bookfb">Please <a href="https://calendly.com/greystudio-crew/30-min-meeting" target="_blank" rel="noopener">open the booking page</a> to choose a time.</p></noscript>',
    '<div class="calendly-inline-widget" data-url="' + CALENDLY + '?hide_gdpr_banner=1&amp;background_color=0b0c0d&amp;text_color=f7f7f7&amp;primary_color=35c9ff" style="min-width:320px;height:700px;"></div>\n<div class="bookstatus" id="bookstatus" role="status" aria-live="polite">Loading available appointment times…</div>\n<script>\n(()=>{const status=document.getElementById("bookstatus");let loaded=false;const markLoaded=()=>{loaded=true;if(status){status.hidden=true}};window.addEventListener("message",event=>{if(event.origin==="https://calendly.com"&&event.data&&String(event.data.event||"").startsWith("calendly."))markLoaded()});const script=document.createElement("script");script.src="https://assets.calendly.com/assets/external/widget.js";script.async=true;script.onload=()=>{setTimeout(()=>{if(!loaded&&status)status.textContent="Calendar taking longer than expected? Use the direct booking link below.";},9000)};script.onerror=()=>{if(status)status.textContent="The embedded calendar could not load. Please use the direct booking link below."};document.head.appendChild(script);setTimeout(()=>{if(!loaded&&status)status.textContent="Having trouble viewing appointment times? Use the direct booking link below.";},12000)})();\n</script>\n<!-- Calendly inline widget end -->',
    "Calendly resilient loader",
)
book = once(
    book,
    '</div>\n<div class="acts">',
    '</div>\n<div class="bookfallback"><p>Calendar not appearing? Open Calendly directly to see live availability.</p><a class="btn w" href="' + CALENDLY + '" target="_blank" rel="noopener">Open booking calendar ↗</a></div>\n<div class="acts">',
    "direct Calendly fallback",
)
# Ensure the direct link remains visible and easy to use on phones.
book = once(
    book,
    '@media(max-width:900px){.wrap{padding:0 16px}.logo{font-size:30px}.bookbox,.bookbox .calendly-inline-widget{min-height:760px}.bookbox .calendly-inline-widget{height:760px!important}}',
    '@media(max-width:900px){.wrap{padding:0 16px}.logo{font-size:30px}.bookbox,.bookbox .calendly-inline-widget{min-height:760px}.bookbox .calendly-inline-widget{height:760px!important}.bookfallback{align-items:flex-start;flex-direction:column}.bookfallback .btn{width:100%;justify-content:center}}',
    "booking mobile fallback",
)
BOOK.write_text(book, encoding="utf-8")
print("Updated homepage mobile CTA order and resilient Calendly booking fallback.")
