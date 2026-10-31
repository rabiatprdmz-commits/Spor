"""program.json -> program.pdf (Turkish, figures included). Run: python3 build.py"""
import json, os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Group, Line, Circle, Rect
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
st=[P(d['title'],T),P(d['subtitle'],S),P(d['how_to_read'],S)]
st+= [day(x) for x in d['days']]
st+=[P('Dinlenme günleri',H),P(d['rest_days']),P('İlerleme',H)]+[P('• '+t) for t in d['progression']]
st+=[P('Beslenme ve su',H)]+[P('• '+t) for t in d['nutrition']]
st+=[P('Güvenlik',H)]+[P('• '+t) for t in d['safety']]
st+=[Spacer(1,6),P('Bu program genel bilgi amaçlıdır; sağlık sorunun olursa bir hekime danış.',S)]
SimpleDocTemplate(os.path.join(HERE,'program.pdf'),pagesize=A4,leftMargin=16*mm,rightMargin=16*mm,topMargin=14*mm,bottomMargin=14*mm,title=d['title']).build(st)
print('ok')
