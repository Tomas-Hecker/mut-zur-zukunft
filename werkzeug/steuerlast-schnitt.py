from PIL import Image, ImageDraw
D='/mnt/project-files/rechenmodell-mikrosim/steuerlast/'
O='/home/user/mut-zur-zukunft/bilder/steuerlast/'
plan={
 'steuerlast-feld-einkommen-vermoegen':[(8,100),(200,1440)],
 'steuerlast-nach-einkommen':[(8,960)],
 'steuerlast-anteile':[(8,700)],
 'steuerlast-nach-vermoegen':[(8,680)],
 'wer-bezahlt-einkommen-vermoegen':[(8,100),(200,1200)],
 'vermoegen-sparen':[(8,100),(200,1135)],
}
for f,segs in plan.items():
    im=Image.open(D+f+'.png').convert('RGB')
    if f=='steuerlast-nach-einkommen':
        ImageDraw.Draw(im).rectangle([1080,36,1680,120],fill=(255,255,255))
    W=im.width-8
    parts=[im.crop((4,a,im.width-4,b)) for a,b in segs]
    H=sum(p.height for p in parts)+30
    out=Image.new('RGB',(W,H),(255,255,255)); y=0
    for p in parts: out.paste(p,(0,y)); y+=p.height
    out.save(O+f+'.webp',quality=88,method=6)
    print(f,out.size)
