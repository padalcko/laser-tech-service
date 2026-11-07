#!/usr/bin/env python3
"""Render the single corporate page in three languages from approved copy."""
import json, re
from html import escape as e
from pathlib import Path
import site_locales as locales
ROOT=locales.ROOT
COPY=json.loads((ROOT/'content/about.json').read_text())
IMAGES=json.loads((ROOT/'content/about-images.json').read_text())
ROUTES={'pl':'/o-nas/','ru':'/ru/o-nas/','en':'/en/about-us/'}
LABELS={'pl':('O nas','Strona główna','Wyróżnienie Laser Tech Service — 2026','Dla sieci i salonów','Blog'),'ru':('О нас','Главная','Награда Laser Tech Service — 2026','Для сетей и салонов','Блог'),'en':('About Us','Home','Laser Tech Service Recognition — 2026','For Chains & Salons','Blog')}
META={
 'pl':('O nas | Laser Tech Service – serwis laserów Wrocław','Poznaj Laser Tech Service, nasz zespół i historię. Serwis laserów, naprawa laserów i regeneracja laserów we Wrocławiu i całej Polsce.'),
 'ru':('О компании | Laser Tech Service — ремонт лазеров во Вроцлаве','Узнайте историю Laser Tech Service, познакомьтесь с командой и нашим подходом к ремонту лазерного и косметологического оборудования в Польше.'),
 'en':('About Us | Laser Tech Service – Laser Repair in Poland','Meet the Laser Tech Service team and discover our story, mission and approach to professional laser equipment repair in Wrocław and across Poland.')}
REG=locales.load(); GROUPS={g['id']:g for g in REG['pages']}
def route(key,lang):return GROUPS[key]['routes'][lang]['url']
def link(url,text,cls=''):
 ext=' target="_blank" rel="noopener noreferrer"' if url.startswith('https://wa.me/') else ''
 return f'<a href="{e(url)}"'+(f' class="{cls}"' if cls else '')+ext+f'>{e(text)}</a>'
def paras(blocks):return '\n'.join(f'<p>{e(b)}</p>' for b in blocks)
def field(blocks,name):
 for i,b in enumerate(blocks):
  if b.startswith(name+':'):
   rest=b[len(name)+1:].strip()
   return rest or blocks[i+1]
 raise ValueError(name)
def photo(asset,name):
 v=asset['variants'];src=v[1]
 return f'<img src="/{src["file"]}" srcset="'+', '.join(f'/{x["file"]} {x["width"]}w' for x in v)+f'" sizes="(max-width: 767px) calc(100vw - 40px), (max-width: 1023px) 44vw, 360px" width="{src["width"]}" height="{src["height"]}" alt="{e(name)}" loading="lazy" decoding="async" />'
def render_main(lang):
 sections=COPY[lang]['sections'];out=[];titles=[]
 ids=['hero','history','services','team','mission','process','trust','work','geography','contact']
 for i,section in enumerate(sections):
  b=section['blocks'];heading=field(b,'H1' if i==0 else 'H2');titles.append(heading)
  body=''
  if i==0:
   home=route('home',lang)
   body=f'<nav class="breadcrumbs" aria-label="{ {"pl":"Ścieżka nawigacji","ru":"Навигационная цепочка","en":"Breadcrumbs"}[lang] }">{link(home,LABELS[lang][1])}<span aria-hidden="true">/</span><span aria-current="page">{LABELS[lang][0]}</span></nav>'
   body+=f'<span class="section-kicker">{e(field(b,"Eyebrow"))}</span><h1>{e(heading)}</h1><p class="about-lead">{e(field(b,"Subtitle"))}</p>'+paras([field(b,'Intro')])
   cta=field(b,'CTA').splitlines();body+='<div class="about-actions">'+link(route('realizacje',lang),cta[0],'btn btn-primary')+link(route('kontakt',lang),cta[1],'btn btn-outline')+'</div>'
  else:
   body=f'<h2>{e(heading)}</h2>'
   if i==1:
    start=b.index('Body:')+1;end=b.index('Highlight:')
    body+=f'<p class="about-lead">{e(field(b,"Lead"))}</p><div class="about-prose">'+paras(b[start:end])+f'</div><blockquote>{e(field(b,"Highlight"))}</blockquote>'
   elif i==2:
    body+=paras([field(b,'Intro')])+'<div class="about-grid">'
    keys=['uslugi:diagnostyka-laserow-diodowych','uslugi:regeneracja-glowic-i-manipulatorow','uslugi:naprawa-zasilaczy-i-elektroniki','uslugi:naprawa-ukladow-chlodzenia','uslugi:konserwacja-urzadzen-kosmetologicznych','uslugi:serwis-dla-sieci-salonow']
    for j,match in enumerate(k for k in range(len(b)) if b[k].startswith('Card ')):
     name=b[match].split(' — ',1)[1].removesuffix(':')
     body+=f'<article class="about-card"><h3>{link(route(keys[j],lang),name)}</h3>{paras([b[match+1]])}</article>'
    body+='</div><div class="about-actions">'+link(route('uslugi',lang),field(b,'CTA'),'btn btn-primary')+'</div>'
   elif i==3:
    body+=paras([field(b,'Intro')])+'<div class="about-team">'
    assets = {asset['slug']: asset for asset in IMAGES}
    for slug,idx in zip(section['image_order'],[k for k,x in enumerate(b) if x.startswith('**')]):
     asset = assets[slug]
     name=b[idx].strip('*');body+=f'<article class="about-person" data-person="{slug}"><div class="about-portrait">{photo(asset,name)}</div><div class="about-person__body"><h3>{e(name)}</h3><p class="about-role">{e(b[idx+1])}</p>{paras([b[idx+2]])}</div></article>'
    body+='</div>'
   elif i==4:
    body+=f'<p class="about-statement">{e(field(b,"Statement"))}</p>'+paras(b[b.index('Body:')+1:])
   elif i in (5,6):
    lines=[line for x in b[1:] for line in x.splitlines() if re.match(r'(?:\d+\. |\- )',line)]
    tag='ol' if i==5 else 'ul';body+=f'<{tag} class="about-list">'
    for line in lines:
     title,description=re.sub(r'^(?:\d+\. |\- )','',line).split(' — ',1)
     body+=f'<li><h3>{e(title)}</h3><p>{e(description)}</p></li>'
    body+=f'</{tag}>'
   elif i==7:
    body+=paras([b[1]])
    listing=(ROOT/route('realizacje',lang).lstrip('/')/'index.html').read_text()
    cards=re.findall(r'<article class="realizacja-card".*?</article>',listing,re.S)[:3]
    assert len(cards)==3
    body+='<div class="about-cases">'+''.join(c.replace('<h2','<h3').replace('</h2>','</h3>') for c in cards)+'</div>'
    body+='<div class="about-actions">'+link(route('realizacje',lang),field(b,'CTA'),'btn btn-primary')+link(route('blog',lang),LABELS[lang][4],'btn btn-outline')+'</div>'
    stem='/img/blog/laser-tech-service-zlota-firma-2026/nagroda-zlota-firma-2026-laser-tech-service'
    body+=f'<figure class="about-award"><img src="{stem}-responsive-640w.webp" srcset="{stem}-responsive-320w.webp 320w, {stem}-responsive-640w.webp 640w, {stem}-responsive-960w.webp 960w" sizes="(max-width: 767px) calc(100vw - 40px), 360px" width="640" height="512" loading="lazy" decoding="async" alt="{e(LABELS[lang][2])}" /><figcaption>{e(LABELS[lang][2])}<span>Złota Firma</span></figcaption></figure>'
   elif i==8:
    body+=paras(b[1:])+'<div class="about-actions">'+link(route('uslugi:serwis-dla-sieci-salonow',lang),LABELS[lang][3],'btn btn-outline')+'</div>'
   elif i==9:
    body+=paras([b[1]])
    labels=field(b,'Buttons').splitlines()
    body+='<div class="about-actions">'+link('tel:+48790402597',labels[0],'btn btn-primary')+link('https://wa.me/48790402597',labels[1],'btn btn-outline')+link(route('realizacje',lang),labels[2],'btn btn-outline')+'</div>'
    body+='<address>Laser Tech Service<br />ul. Marszałka Józefa Piłsudskiego 74, lok. 320<br />50-020 Wrocław, Polska<br />'+link('tel:+48790402597','+48 790 402 597')+'<br />'+link('mailto:contact@lasertechservice.pl','contact@lasertechservice.pl')+'</address>'
    warranty={'pl':'Czas trwania i warunki gwarancji zależą od rodzaju naprawy oraz uzgodnionych warunków.','ru':'Срок и условия гарантии зависят от вида ремонта и согласованных условий.','en':'Warranty duration and conditions depend on the type of repair and the agreed terms.'}
    body+=paras([warranty[lang]])
  out.append(f'<section class="about-section'+(' about-hero' if i==0 else '')+f'" id="{ids[i]}" aria-labelledby="about-{ids[i]}-title"><div class="container">'+body.replace('<h1>','<h1 id="about-hero-title">',1).replace('<h2>',f'<h2 id="about-{ids[i]}-title">',1)+'</div></section>')
 return '<main class="about-page">\n'+'\n'.join(out)+'\n</main>',titles[0]
def build(check=False):
 changed=[]
 for lang,url in ROUTES.items():
  template=(ROOT/route('partnerzy',lang).lstrip('/')/'index.html').read_text()
  main,h1=render_main(lang)
  template=re.sub(r'<main\b.*?</main>',lambda m:main,template,flags=re.S)
  head,body=template.split('</head>',1)
  title,desc=META[lang];base=REG['base_url'];canonical=base+url
  head=re.sub(r'<title>.*?</title>',lambda m:f'<title>{e(title)}</title>',head,flags=re.S)
  values={'description':desc,'og:title':title,'og:description':desc,'og:url':canonical,'twitter:title':title,'twitter:description':desc}
  for key,val in values.items():
   head=re.sub(r'(<meta\s+(?:name|property)="'+re.escape(key)+r'"\s+content=")[^"]*("\s*/?>)',lambda m:m[1]+e(val,quote=True)+m[2],head)
  head=re.sub(r'<link\b[^>]*(?:rel="canonical"|hreflang=|rel="alternate"[^>]*text/markdown)[^>]*>','',head)
  head+=f'\n<link rel="canonical" href="{canonical}" />\n'+''.join(f'<link rel="alternate" hreflang="{l}" href="{base+r}" />\n' for l,r in {**ROUTES,'x-default':ROUTES['pl']}.items())
  head=re.sub(r'<meta property="og:locale:alternate"[^>]*>','',head)
  head+=''.join(f'<meta property="og:locale:alternate" content="{v}" />\n' for l,v in {'pl':'pl_PL','ru':'ru_RU','en':'en_GB'}.items() if l!=lang)
  schemas=[{'@context':'https://schema.org','@type':'AboutPage','@id':canonical+'#webpage','name':h1,'description':desc,'url':canonical,'inLanguage':lang,'isPartOf':{'@id':base+'/#website'},'about':{'@id':base+'/#organization'},'breadcrumb':{'@id':canonical+'#breadcrumb'}}, {'@context':'https://schema.org','@type':'BreadcrumbList','@id':canonical+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':1,'name':LABELS[lang][1],'item':base+route('home',lang)},{'@type':'ListItem','position':2,'name':LABELS[lang][0],'item':canonical}]}]
  head=re.sub(r'<script type="application/ld\+json">.*?</script>','',head,flags=re.S)
  head+=''.join('<script type="application/ld+json">\n'+json.dumps(s,ensure_ascii=False,indent=2)+'\n</script>\n' for s in schemas)
  head=head.replace('<link rel="stylesheet" href="/css/partnerzy.css" />','<link rel="stylesheet" href="/css/about.css" />').replace('<link rel="stylesheet" href="/css/blog.css" />','')
  # The language and corporate navigation generators run after this source builder.
  body=body.replace('nav-list__link nav-list__link--active" aria-current="page"','nav-list__link"')
  source=head+'</head>'+body
  path=ROOT/url.lstrip('/')/'index.html';path.parent.mkdir(parents=True,exist_ok=True)
  if not path.exists() or source!=path.read_text():
   changed.append(str(path.relative_to(ROOT)))
   if not check:path.write_text(source)
 print('About source pages:',len(ROUTES))
 return changed
if __name__=='__main__':build()
