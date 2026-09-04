from pathlib import Path
import math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'poster_robot_network.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
for name, file in [('Regular', 'segoeui.ttf'), ('Bold', 'segoeuib.ttf'), ('Light', 'segoeuil.ttf'), ('Mono', 'DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name, 'C:/Windows/Fonts/' + file))
pdfmetrics.registerFontFamily('Regular', normal='Regular', bold='Bold', italic='Regular', boldItalic='Bold')

W, H = 1190, 1684
MM = 72 / 25.4
c = canvas.Canvas(str(OUT), pagesize=(594*MM, 841*MM), pageCompression=1)
c.setTitle('Mindstorms Party | Robot control and network communication')
c.setAuthor('Mindstorms Party | University of Bayreuth')
c.setSubject('Source-based overview of Rust EV3 control, collision avoidance, steering, UDP, TCP and MQTT')
c.scale(594*MM/W, 841*MM/H)
NAVY = '#122D38'; INK = '#18343F'; MUTED = '#516A73'; TEAL = '#007C7A'; CYAN = '#42DDC7'
BLUE = '#386DC8'; PURPLE = '#7957B5'; GOLD = '#E4AA39'; RED = '#B54D47'
PAPER = '#F5F7F5'; LINE = '#D9E3E3'; PALE = '#EAF3F1'; WHITE = '#FFFFFF'

def rect(x,y,w,h,fill,stroke=None,r=0,lw=1):
    c.setFillColor(HexColor(fill)); c.setStrokeColor(HexColor(stroke or fill)); c.setLineWidth(lw)
    if r: c.roundRect(x,H-y-h,w,h,r,fill=1,stroke=bool(stroke))
    else: c.rect(x,H-y-h,w,h,fill=1,stroke=bool(stroke))

def text(s,x,y,size=16,font='Regular',color=INK,align='left'):
    c.setFillColor(HexColor(color)); c.setFont(font,size)
    {'left':c.drawString,'center':c.drawCentredString,'right':c.drawRightString}[align](x,H-y-size*.79,s)

def para(s,x,y,w,size=16,leading=None,color=INK,maxh=None):
    p=Paragraph(s,ParagraphStyle('p',fontName='Regular',fontSize=size,leading=leading or size*1.32,textColor=HexColor(color)))
    _,h=p.wrap(w,1800)
    if maxh is not None and h>maxh: raise ValueError(f'Overflow {h:.1f}>{maxh}: {s[:55]}')
    p.drawOn(c,x,H-y-h)
    return h

def line(x1,y1,x2,y2,col=LINE,lw=1,dash=None):
    c.setStrokeColor(HexColor(col)); c.setLineWidth(lw); c.setDash(dash or [])
    c.line(x1,H-y1,x2,H-y2); c.setDash([])

def path(points,col=TEAL,lw=3,dash=None):
    c.setStrokeColor(HexColor(col)); c.setLineWidth(lw); c.setDash(dash or []); c.setLineJoin(1); c.setLineCap(1)
    p=c.beginPath(); p.moveTo(points[0][0],H-points[0][1])
    for x,y in points[1:]: p.lineTo(x,H-y)
    c.drawPath(p,stroke=1,fill=0); c.setDash([])

def head(x,y,angle,col=TEAL,size=7):
    a=math.radians(angle)
    p=c.beginPath(); p.moveTo(x,H-y)
    for offset in (-.5,.5):
        xx=x-size*math.cos(a)+offset*size*math.sin(a)
        yy=y-size*math.sin(a)-offset*size*math.cos(a)
        p.lineTo(xx,H-yy)
    p.close(); c.setFillColor(HexColor(col)); c.drawPath(p,stroke=0,fill=1)

def arrow(points,col=TEAL,lw=2.5,both=False):
    path(points,col,lw)
    a,b=points[-2:]; head(*b,math.degrees(math.atan2(b[1]-a[1],b[0]-a[0])),col)
    if both:
        a,b=points[1],points[0]; head(*b,math.degrees(math.atan2(b[1]-a[1],b[0]-a[0])),col)

def circle(x,y,r,fill,stroke=None,lw=1):
    c.setFillColor(HexColor(fill)); c.setStrokeColor(HexColor(stroke or fill)); c.setLineWidth(lw)
    c.circle(x,H-y,r,fill=1,stroke=bool(stroke))

def pill(s,x,y,w,col=TEAL,bg=PALE,size=12):
    rect(x,y,w,25,bg,r=12); text(s,x+w/2,y+6,size,'Bold',col,'center')

def section(n,title,y,tag):
    text(n,42,y+3,17,'Bold',TEAL); text(title,82,y,25,'Bold',NAVY)
    text(tag,1148,y+7,12,'Bold',MUTED,'right')

def label(s,x,y,col=TEAL,size=12,bg=WHITE):
    wid=pdfmetrics.stringWidth(s,'Bold',size)+14
    rect(x-wid/2,y-2,wid,size+6,bg,r=3); text(s,x,y,size,'Bold',col,'center')

def kart(cx,cy,scale=1,col=TEAL,heading=0):
    c.saveState(); c.translate(cx,H-cy); c.rotate(-heading); c.scale(scale,scale)
    # Original vector schematic, viewed from above; nose faces right.
    def rr(x,y,w,h,fill,r=3):
        c.setFillColor(HexColor(fill)); c.roundRect(x,y,w,h,r,stroke=0,fill=1)
    rr(-27,-31,37,13,NAVY); rr(-27,18,37,13,NAVY)
    rr(-33,-23,65,46,col,7); rr(17,-15,29,30,col,4)
    rr(-21,-18,36,36,'#F5F7F5',3); rr(-15,-12,24,24,NAVY,1)
    rr(-11,-8,7,7,WHITE,0); rr(1,1,5,7,WHITE,0); rr(-9,3,4,5,WHITE,0)
    rr(25,-7,12,14,'#DAE9E4',2)
    c.restoreState()

rect(0,0,W,H,PAPER)
rect(0,0,W,197,NAVY)
# Preserve the supplied logo's proportions and original colors on white.
rect(914,14,234,70,WHITE,r=7)
c.drawImage(str(Path(__file__).resolve().parent / 'assets' / 'universitaet-bayreuth.png'),
            928,H-17-206*396/1280,width=206,height=206*396/1280,mask='auto')
# Transparent three-robot formation in the header.
c.drawImage(str(Path(__file__).resolve().parent / 'assets' / 'ev3-three-robots-transparent.png'),
            841,H-86-108,width=307,height=108,mask='auto')
text('MINDSTORMS PARTY',42,30,18,'Bold',CYAN)
text('UNIVERSITY OF BAYREUTH  /  BACHELOR PROJECT',42,57,11.5,'Bold','#B6D0D1')
text('Robot Control & Communication',39,91,50,'Bold',WHITE)
text('Collision avoidance, steering & network protocols',43,158,19,'Regular','#D8E9E8')
rect(42,194,126,4,CYAN)

section('01','One system. Three communication channels.',226,'ARCHITECTURE')
rect(42,271,1106,238,WHITE,r=13)
# Direct manual link is deliberately separate from desktop autonomous driving.
arrow([(181,324),(181,292),(1020,292),(1020,324)],TEAL)
label('DIRECT PHONE CONTROL  /  UDP 7778',596,284,TEAL,12)

def node(x,w,title,sub1,sub2,col):
    rect(x,324,w,96,'#F7FAF9',LINE,10)
    rect(x,324,5,96,col,r=2)
    text(title,x+20,342,23,'Bold',NAVY)
    text(sub1,x+20,373,14,'Regular',MUTED)
    text(sub2,x+20,395,12,'Bold',col)

node(66,230,'AR App','Unity / C#','Joystick + game interface',BLUE)
node(467,261,'Desktop','C++ / Qt / OpenCV','Camera, planner, path follower',TEAL)
node(912,216,'EV3 robot','Native Rust / ev3dev','Motor execution + status',PURPLE)
arrow([(300,363),(463,363)],BLUE,both=True)
label('TCP 1234',423,340,BLUE)
text('game events',382,382,12,'Regular',MUTED,'center')
arrow([(732,352),(908,352)],TEAL)
label('UDP 7778',858,332,TEAL)
text('autonomous drive',820,364,11.5,'Regular',MUTED,'center')
arrow([(908,391),(732,391)],TEAL)
label('UDP 7779',779,399,TEAL,11.5)

text('Sends: mind/<robot_id>/cmd',481,425,9.8,'Mono',PURPLE)
text('Receives: mind/+/status',481,443,9.8,'Mono',PURPLE)
text('Receives: mind/<robot_id>/cmd',925,425,9.8,'Mono',PURPLE)
text('Sends: mind/<robot_id>/status',925,443,9.8,'Mono',PURPLE)
rect(480,463,245,42,'#F0ECF7',r=8)
text('MOSQUITTO / MQTT 1883',602.5,471,12,'Bold',PURPLE,'center')
text('Auto reconnect + restore subscriptions',602.5,490,9.5,'Bold',PURPLE,'center')
arrow([(705,423),(705,459)],PURPLE,both=True)
arrow([(729,484),(1114,484),(1114,424)],PURPLE,both=True)
rect(66,427,397,21,PALE,r=5)
circle(76,437.5,1.8,TEAL)
c.setStrokeColor(HexColor(TEAL)); c.setLineWidth(1.2)
for radius in (6,10):
    c.arc(76-radius,H-437.5-radius,76+radius,H-437.5+radius,-60,120)
text('UDP broadcast: device discovery on the local network',94,432,11.3,'Bold',TEAL)
text('1 Hz heartbeats report state and refresh robot IPs.',67,455,12.2,'Regular',MUTED)
text('3 s without status: desktop marks it offline.',67,476,12.2,'Bold',MUTED)

# Three protocol explanations, arranged with matching transport colors.
for x,col in [(42,TEAL),(416,BLUE),(790,PURPLE)]:
    rect(x,517,358,211,WHITE,LINE,11)
    rect(x+17,536,4,22,col,r=2)
text('UDP: binary for low latency',73,535,18.5,'Bold',TEAL)
para('<b>4-byte binary packets</b> cut message size and parsing time for <b>low latency</b>. Default: <b>20 Hz</b>. New setpoints replace old ones without retries.',61,570,320,15.1,20,maxh=82)
for i,(s,sub) in enumerate([('01','ev3_01'),('01','drive'),('32','+50%'),('00','0% turn')]):
    xx=61+i*80
    rect(xx,657,74,27,PALE,r=4); text(s,xx+37,663,15,'Mono',TEAL,'center')
    text(sub,xx+37,691,11.7,'Regular',MUTED,'center')
text('Binary drive packet: 4 bytes, shown in hex',61,711,10.5,'Regular',MUTED)

text('TCP: structured game events',447,535,18.5,'Bold',BLUE)
para('Phones exchange <b>JSON game events</b> with the desktop. The <b>type</b> field selects a handler, e.g. <b>shop_buy</b>. Shared game updates reach all connected phones; <b>shop_open</b> carries the player\'s shop inventory.',435,570,320,15.1,20,maxh=102)
line(435,678,755,678,LINE)
para('<b>Splatoon UDP:</b> input → desktop <b>12346</b>;<br/>grid updates → phones <b>12345</b>.',435,688,320,12.6,16.4,maxh=36)

text('MQTT: commands & replies',821,535,18.5,'Bold',PURPLE)
para('Binary <b>drive_for, turn, stop, ping</b> use <b>QoS 1 (at least once)</b>; ACKs echo IDs. Both clients restore subscriptions. <b>Desktop:</b> automatically reconnects, with up to 10 seconds between retry attempts.',809,570,320,15.1,20,maxh=102)
text('mind/<robot_id>/cmd',809,679,13.5,'Mono',PURPLE)
text('mind/<robot_id>/status',809,701,13.5,'Mono',PURPLE)

section('02','From a target to controlled movement',762,'DESKTOP CONTROL')
rect(42,806,539,415,WHITE,LINE,12); rect(609,806,539,415,WHITE,LINE,12)
text('Plan around other robots',63,826,23,'Bold',NAVY)
text('Global board routes + local collision avoidance',63,858,14.6,'Regular',MUTED)

# Three original plan-view diagrams.
for x,cap in [(63,'ROUTE'),(237,'YIELD'),(411,'CLEAR A NODE')]:
    rect(x,889,152,111,'#F0F5F3',r=7)
    text(cap,x+76,901,11,'Bold',MUTED,'center')
path([(76,969),(101,948),(141,948),(196,936)],TEAL,3)
for x,y in [(76,969),(101,948),(141,948),(196,936)]: circle(x,y,4,WHITE,TEAL,1.5)
kart(102,948,.30,TEAL,-5)
circle(307,957,20,'#E8DFF3')
path([(247,969),(278,969),(293,932),(327,932),(374,969)],TEAL,2.5)
arrow([(352,974),(331,963)],PURPLE,2)
kart(306,960,.28,PURPLE,180); kart(272,960,.28,TEAL,-24)
line(425,962,548,962,'#A9BEBB',3)
circle(485,962,6,WHITE,TEAL,2)
kart(451,962,.28,TEAL)
arrow([(487,956),(509,932)],PURPLE,2)
kart(521,932,.28,PURPLE,-35)

def item(title,body,x,y,w=494,size=15):
    return para(f'<b>{title}</b> {body}',x,y,w,size,20,maxh=64)

item('1 / Route.', 'Dijkstra selects the board-node route. Grid A* detours around parked robots; clearance-checked corner rounding smooths the waypoints.',63,1016)
item('2 / Yield.', 'A central coordinator watches nearby paths. The higher robot ID yields, replans around the other robot, or holds if no detour exists.',63,1084)
item('3 / Clear.', 'If a destination is occupied, the blocker is routed to a free parking spot off the lanes. The arriving robot waits for the node to clear.',63,1152)

text('Follow the path, correct the heading',630,826,22,'Bold',NAVY)
text('Camera pose → lookahead target → steering → wheels',630,858,14.2,'Regular',MUTED)
rect(630,889,497,111,'#F0F5F3',r=7)
path([(650,970),(753,970),(812,946),(938,946),(1107,924)],'#97C9C1',5)
kart(758,970,.58,TEAL,-3)
# A real QR code replaces the schematic marker on this robot. Rotate it with
# the robot and preserve the standard quiet zone for reliable scanning.
rickroll_url='https://youtu.be/dQw4w9WgXcQ'
rickroll_qr=qr.QrCodeWidget(rickroll_url,barLevel='L',barBorder=4)
rbx,rby,rbw,rbh=rickroll_qr.getBounds()
rickroll_drawing=Drawing(21,21,transform=[21/(rbw-rbx),0,0,21/(rbh-rby),0,0])
rickroll_drawing.add(rickroll_qr)
c.saveState()
c.translate(756.3,H-970.1)
c.rotate(3)
c.setFillColor(HexColor(WHITE))
c.setStrokeColor(HexColor(NAVY))
c.setLineWidth(.8)
c.rect(-10.5,-10.5,21,21,stroke=1,fill=1)
renderPDF.draw(rickroll_drawing,c,-10.5,-10.5)
c.restoreState()
c.linkURL(rickroll_url,(746,H-981,767,H-960),relative=0,thickness=0)
circle(903,946,7,WHITE,TEAL,2)
arrow([(787,965),(895,947)],TEAL,1.6)
line(785,970,875,970,MUTED,1,[4,3])
text('heading error',817,977,11.5,'Regular',MUTED)
text('20 cm lookahead',930,922,12,'Bold',TEAL)
text('planned path',662,913,11.5,'Regular',MUTED)
item('1 / Observe.', 'ArUco markers provide position and heading. A board homography converts camera pixels into physical centimetres.',630,1016)
item('2 / Steer.', 'A lookahead point sets the heading error. A PID controller computes turn rate; forward speed falls in corners and near the goal.',630,1084)
item('3 / Settle.', 'Sharp turns use pivot pulses and pauses for camera feedback to catch up. Calibration scales compensate drive and turn bias.',630,1152)

# Presentation takeaway for the autonomous control pipeline.
rect(42,1233,1106,43,NAVY,r=7)
text('AUTONOMOUS DRIVING',59,1249,10.5,'Bold',CYAN)
text('Plan the route',325,1246,17,'Bold',WHITE,'center')
arrow([(439,1255),(485,1255)],CYAN,1.7)
text('Avoid obstacles',607,1246,17,'Bold',WHITE,'center')
arrow([(733,1255),(779,1255)],CYAN,1.7)
text('Steer with camera feedback',953,1246,17,'Bold',WHITE,'center')

section('03','Inside the brick',1293,'RUST + EV3DEV')
rect(42,1335,692,340,WHITE,LINE,12); rect(754,1335,394,211,WHITE,LINE,12)
text('Ferris at the wheel',62,1355,25,'Bold',NAVY)
text('Four workers, one motor controller',62,1388,15,'Regular',MUTED)
c.drawImage(str(Path(__file__).resolve().parent / 'assets' / 'ferris-happy.png'),
            597,H-1349-112*307/460,width=112,height=112*307/460,mask='auto')
para('Native Rust runs directly on the EV3\'s Linux system. A mutex protects shared drive state; each valid UDP packet overwrites the setpoint and wakes the motor worker. A 10 ms timeout keeps watchdog checks running between packets.',62,1414,652,14.5,19,maxh=58)
workers=[('UDP','Decode + ID filter','Wake the motor loop',TEAL),('MOTOR','10 ms check interval','Regulated B/C motors',TEAL),('MQTT','Dispatch commands','Interruptible moves',PURPLE),('HEARTBEAT','1 Hz to desktop','State + battery + ID',BLUE)]
for i,(title,a,b,col) in enumerate(workers):
    xx=62+i*165
    rect(xx,1481,157,62,'#F0F5F3',r=6)
    text(title,xx+11,1491,12.5,'Bold',col)
    text(a,xx+11,1511,11.2,'Regular',MUTED)
    text(b,xx+11,1526,11.2,'Regular',MUTED)
para('<b>Two ways to move:</b> stream speed + turn or independent wheel speeds; queue <b>drive_for</b> and <b>turn</b> for distance and angle moves. The motor worker sends the completion ACK.',62,1555,652,14.2,18.5,maxh=38)
para('<b>Differential drive:</b> v<sub>L</sub> = v - ωb/2; v<sub>R</sub> = v + ωb/2.<br/>v: forward speed; ω: turn rate; b: wheel spacing.<br/>At the speed limit, both wheels slow together to keep the curve.<br/>Motors B/C; 56 mm wheels; b = 126 mm.',62,1599,450,13.2,16,maxh=65)
# Turning symbol uses the same vector robot and palette as the path diagrams.
rect(541,1599,173,64,'#F0F5F3',r=7)
c.setStrokeColor(HexColor(TEAL)); c.setLineWidth(3); c.setLineCap(1)
turn_path = c.beginPath()
turn_path.moveTo(556,H-1646)
turn_path.curveTo(615,H-1646,659,H-1648,684,H-1614)
c.drawPath(turn_path,stroke=1,fill=0)
head(684,1614,-54,TEAL,8)
kart(606,1643,.48,TEAL,-5)

text('Independent stop mechanisms',774,1353,20,'Bold',NAVY)
def safety(y,number,body,col):
    text(number,774,y,22,'Bold',col)
    para(body,873,y-1,252,13.6,17,maxh=38)
safety(1390,'150 ms','No fresh drive packet: the EV3 watchdog stops continuous motion.',TEAL)
safety(1441,'400 ms','Stale camera pose: the desktop commands zero drive.',BLUE)
safety(1492,'STOP','MQTT sets an interrupt flag for precision moves; motors poll it.',PURPLE)

url='https://github.com/st-fr/mindstorms-docs'
qw=qr.QrCodeWidget(url)
bx,by,bw,bh=qw.getBounds(); d=Drawing(104,104,transform=[104/(bw-bx),0,0,104/(bh-by),0,0]); d.add(qw)
renderPDF.draw(d,c,1044,H-1558-104)
c.linkURL(url,(1044,H-1662,1148,H-1558),relative=0,thickness=0)
c.showPage(); c.save()
print(OUT)
