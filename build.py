"""program.json -> program.pdf + gunluk.html (Turkish, figures included). Run: python3 build.py"""
import json, os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Group, Line, Circle, Rect
from reportlab.platypus import Image
HERE=os.path.dirname(os.path.abspath(__file__))
FD='/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('D',FD+'DejaVuSans.ttf')); pdfmetrics.registerFont(TTFont('DB',FD+'DejaVuSans-Bold.ttf'))
A=colors.HexColor('#d4506a'); G=colors.HexColor('#2f5d50'); L=colors.HexColor('#e1ead9')
T=ParagraphStyle('T',fontName='DB',fontSize=19,leading=24,textColor=G,spaceAfter=4)
S=ParagraphStyle('S',fontName='D',fontSize=9.5,leading=13,textColor=colors.HexColor('#5d6b62'),spaceAfter=6)
H=ParagraphStyle('H',fontName='DB',fontSize=12.5,leading=17,textColor=A,spaceBefore=10,spaceAfter=3)
N=ParagraphStyle('N',fontName='D',fontSize=9,leading=12.5)
B=ParagraphStyle('B',fontName='DB',fontSize=9,leading=12.5)
P=lambda t,s=N:Paragraph(t,s)
# stick figures: head, limbs, band line, dumbbell
PO={'squat':([48,13],[[46,21,38,42],[38,42,56,47],[56,47,54,62],[46,22,58,32]],None,[58,32]),
'rdl':([68,26],[[36,34,62,30],[36,34,37,48],[37,48,36,62],[62,30,60,46]],None,[60,46]),
'row':([68,26],[[36,34,62,30],[36,34,37,48],[37,48,36,62],[62,30,52,38],[52,38,58,46]],None,[58,46]),
'bridge':([8,55],[[14,56,46,38],[46,38,68,40],[68,40,70,62],[14,56,30,60]],[60,40,76,40],None),
'lunge':([50,12],[[50,22,50,38],[50,38,62,48],[62,48,60,62],[50,38,40,54],[40,54,28,60],[50,22,54,38]],None,[54,38]),
'lateral':([50,10],[[50,18,50,38],[50,38,38,50],[38,50,34,62],[50,38,62,50],[62,50,66,62],[50,22,42,32],[50,22,58,32]],[38,50,62,50],None),
'kpush':([16,36],[[24,38,60,48],[24,38,24,60],[60,48,70,60],[70,60,86,54]],None,None),
'press':([50,16],[[50,24,50,44],[50,44,46,62],[50,44,54,62],[50,26,38,24],[38,24,38,8],[50,26,62,24],[62,24,62,8]],None,[38,8]),
'pull':([50,12],[[50,20,50,42],[50,42,46,62],[50,42,54,62],[50,26,20,26],[50,26,80,26]],[20,26,80,26],None),
'plank':([14,40],[[22,42,90,58],[22,42,22,58],[22,58,34,58]],None,None),
'dead':([8,56],[[14,56,44,56],[44,56,46,36],[46,36,66,36],[44,56,80,58],[18,56,18,34],[18,56,2,52]],None,None),
'donkey':([16,34],[[24,38,56,40],[24,38,24,60],[56,40,56,60],[56,40,72,42],[72,42,74,26]],[56,52,72,42],None),
'walk':([50,10],[[50,18,50,40],[50,40,42,62],[50,40,60,60],[50,22,42,34],[50,22,58,32]],None,None)}
def fig(k):
    h,ls,b,d=PO[k]; Y=lambda y:70-y
    dr=Drawing(84,59); g=Group(); g.transform=(0.84,0,0,0.84,0,0); dr.add(g)
    g.add(Rect(0,0,100,70,fillColor=L,strokeColor=None))
    g.add(Line(4,Y(64),96,Y(64),strokeColor=colors.HexColor('#b9c7b3'),strokeWidth=1.2))
    for x1,y1,x2,y2 in ls: g.add(Line(x1,Y(y1),x2,Y(y2),strokeColor=G,strokeWidth=3.4,strokeLineCap=1))
    g.add(Circle(h[0],Y(h[1]),6,fillColor=G,strokeColor=None))
    if b: g.add(Line(b[0],Y(b[1]),b[2],Y(b[3]),strokeColor=A,strokeWidth=2.4,strokeDashArray=[4,3]))
    if d: g.add(Rect(d[0]-5,Y(d[1])-3,10,6,fillColor=A,strokeColor=None))
    return dr
def day(x):
    rows=[[P('',B),P('Hareket',B),P('Set × Tekrar',B),P('İpucu / Alternatif',B)]]
    for e in x['ex']:
        rows.append([fig(e['fig']),P(e['n']),P(e['sr'],B),P(e['tip']+'<br/><font color="#5d6b62">Alternatif: '+e['alt']+'</font>')])
    t=Table(rows,colWidths=[27*mm,40*mm,30*mm,77*mm],repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),L),('LINEBELOW',(0,0),(-1,-1),.4,colors.HexColor('#d6ded2')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
    return KeepTogether([P(f"{x['name']}: {x['focus']} ({x['dur']})",H),P(x['warm']),Spacer(1,3),t,Spacer(1,3),P(x['cool'])])
d=json.load(open(os.path.join(HERE,'program.json'),encoding='utf-8'))
st=[P(d['title'],T),P(d['subtitle'],S),P(d['how_to_read'],S),P('Her hareketin fotoğraflı anlatımı programın sonundaki "Hareket rehberi" bölümünde.',S)]
st+= [day(x) for x in d['days']]
st+=[P('Dinlenme günleri',H),P(d['rest_days']),P('İlerleme',H)]+[P('• '+t) for t in d['progression']]
st+=[P('Beslenme ve su',H)]+[P('• '+t) for t in d['nutrition']]
st+=[P('Güvenlik',H)]+[P('• '+t) for t in d['safety']]
st+=[Spacer(1,6),P('Bu program genel bilgi amaçlıdır; sağlık sorunun olursa bir hekime danış.',S)]
GS=TableStyle([('BACKGROUND',(0,0),(-1,0),L),('LINEBELOW',(0,0),(-1,-1),.4,colors.HexColor('#d6ded2')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)])
def weeks(ws):
    rows=[[P(h,B) for h in ('Hafta','Evre','Setler','Zorluk (kalan tekrar)','Odak / değişiklik','Yürüyüş')]]
    for w in ws: rows.append([P(str(w['hafta']),B),P(w['evre']),P(w['set']),P(w['zorluk']),P(w['odak']),P(w['yuruyus'])])
    t=Table(rows,colWidths=[16*mm,30*mm,22*mm,25*mm,63*mm,22*mm],repeatRows=1); t.setStyle(GS)
    for i,w in enumerate(ws,1):
        if w['evre']=='Hafif hafta': t.setStyle(TableStyle([('BACKGROUND',(0,i),(-1,i),colors.HexColor('#fbe9ed'))]))
    return t
st+=[PageBreak(),P('12 haftalık plan',H),P('Her hafta aynı 4 gün ve aynı hareketler; değişen set, zorluk ve varyasyon. Zorluk parantez içinde günlükteki 1-10 ölçeğiyle.',S),weeks(d['weeks'])]
def bandli(f,segs):
    # loop band fotoğrafta görünmüyor: pembe şerit olarak çiz (beyaz kenarlı)
    from PIL import Image as PI, ImageDraw
    import io
    im=PI.open(f).convert('RGB'); dr=ImageDraw.Draw(im)
    for w,c in ((11,'white'),(7,'#ff2d95')):
        for x1,y1,x2,y2 in segs: dr.line([(x1,y1),(x2,y2)],fill=c,width=w)
        for x1,y1,x2,y2 in segs:
            for x,y in ((x1,y1),(x2,y2)): dr.ellipse([x-w/2,y-w/2,x+w/2,y+w/2],fill=c)
    b=io.BytesIO(); im.save(b,'JPEG',quality=85); b.seek(0); return b
def guide(g):
    def im(i):
        f=os.path.join(HERE,'gorseller',f"{g['img']}_{i}.jpg")
        if str(i) in g.get('band',{}): f=bandli(f,g['band'][str(i)])
        return Image(f,width=38*mm,height=38*mm,kind='proportional')
    txt=[P('<b>Nasıl yapılır</b>')]+[P(f'{i}. {t}') for i,t in enumerate(g['steps'],1)]
    txt+=[Spacer(1,3),P('<b>Dikkat:</b> '+g['watch'])]
    if g['note']: txt.append(P('<font color="#5d6b62">Fotoğraf notu: '+g['note']+'</font>'))
    lb=lambda x:P('<font color="#5d6b62" size="7.5">'+x+'</font>')
    t=Table([[[im(0),lb('Başlangıç')],[im(1),lb('Bitiş')],txt]],colWidths=[40*mm,40*mm,98*mm])
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),2),('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
    return KeepTogether([P(g['n'],H),t,Spacer(1,2)])
st+=[PageBreak(),P('Hareket rehberi',T),P('Her hareketin başlangıç ve bitiş pozisyonu. İlk 2 hafta her hareketi önce ağırlıksız, aynada yavaşça dene. '+d['guide_source'],S)]+[guide(g) for g in d['guide']]
LOG=['Tarih','Hareket','Set','Tekrar','Bant / kg','Zorluk 1-10','Not']
lt=Table([[P(h,B) for h in LOG]]+[['']*7 for _ in range(24)],colWidths=[20*mm,50*mm,12*mm,18*mm,22*mm,20*mm,36*mm],rowHeights=[None]+[8.6*mm]*24,repeatRows=1)
lt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),L),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#c9d3c4')),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
st+=[PageBreak(),P('Antrenman günlüğü',H),P('Çıktı alıp doldurabilirsin; bilgisayar/telefonda gunluk.html daha pratik. Bant: mavi / kırmızı / siyah / North Pacific.',S),lt]
SimpleDocTemplate(os.path.join(HERE,'program.pdf'),pagesize=A4,leftMargin=16*mm,rightMargin=16*mm,topMargin=14*mm,bottomMargin=14*mm,title=d['title']).build(st)
# gunluk.html: hareket listesi program.json'dan gelir
ex={x['name']:[e['n'] for e in x['ex']] for x in d['days']}
tpl=open(os.path.join(HERE,'gunluk_sablon.html'),encoding='utf-8').read()
open(os.path.join(HERE,'gunluk.html'),'w',encoding='utf-8').write(tpl.replace('/*PROGRAM*/{}',json.dumps(ex,ensure_ascii=False)))
print('ok')
