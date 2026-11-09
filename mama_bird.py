"""Mama bird: a stylised sand3d version of the sculpt (front is -Y, up is +Z, mm)."""
import sand3d as s3d

GREY = "#c9c9c9"


def mama_bird(leg_h=70, body_w=125, head_h=150, head_w=105):
    legs = legs_part(leg_h)
    body = s3d.at(body_part(body_w), z=leg_h - 8)
    neck_z = leg_h - 8 + 62
    scarf = s3d.at(scarf_part(d=head_w * 0.95), z=neck_z)
    head = s3d.at(head_part(head_h, head_w), z=neck_z + 4)
    wing = s3d.at(wing_part(), x=body_w / 2 - 6, z=leg_h + 28, y=6)
    twin = s3d.transform(s3d.copy(wing), mirror="x")
    tail = s3d.at(tail_part(), y=body_w / 2 - 20, z=leg_h + 4)
    return s3d.assembly("mama_bird", legs, body, scarf, head, wing, twin, tail)


def body_part(w=125, h=75):
    ob = s3d.loft("body",
                  s3d.station(z=0, w=w * 0.5, d=w * 0.45),
                  s3d.station(z=h * 0.4, w=w, d=w * 0.85),
                  s3d.station(z=h * 0.8, w=w * 0.8, d=w * 0.7),
                  s3d.station(z=h, w=w * 0.45, d=w * 0.4))
    s3d.material(ob, "plastic", color=GREY)
    return ob


def head_part(h=150, w=105):
    ob = s3d.loft("head",
                  s3d.station(z=0, w=w * 0.55, d=w * 0.5, y=-4),
                  s3d.station(z=h * 0.25, w=w * 0.98, d=w * 0.88, y=-2),
                  s3d.station(z=h * 0.5, w=w, d=w * 0.9),
                  s3d.station(z=h * 0.8, w=w * 0.78, d=w * 0.75, y=2),
                  s3d.station(z=h, w=w * 0.3, d=w * 0.3, y=3))
    s3d.material(ob, "plastic", color=GREY)
    front = -w * 0.45
    nose = s3d.at(s3d.loft("nose", s3d.station(z=0, w=14, d=10),
                           s3d.station(z=18, w=20, d=16), s3d.station(z=30, w=14, d=12)),
                  y=front + 12, z=h * 0.38, rx=90)
    ear = s3d.at(s3d.sphere("ear", 22), x=w / 2 - 2, y=2, z=h * 0.4)
    ear2 = s3d.transform(s3d.copy(ear), mirror="x")
    brow = s3d.at(s3d.box("brow", 30, 8, 5), x=-19, y=front + 6, z=h * 0.56)
    brow2 = s3d.transform(s3d.copy(brow), mirror="x")
    lips = s3d.at(s3d.box("lips", 26, 10, 7), y=front + 4, z=h * 0.2)
    s3d.join(ob, nose, ear, ear2, brow, brow2, lips)
    crest = crest_part()
    return s3d.group("head", ob, s3d.at(crest, z=h - 4, y=3))


def crest_part(n=7, r=11, h=34):
    spike = s3d.at(s3d.cone("spike", 9, h, d2=1), on=s3d.ring(n, r))
    base = s3d.cylinder("crest_base", 2 * r + 4, 6)
    s3d.material(base, "plastic", color=GREY)
    return s3d.group("crest", base, spike)


def scarf_part(d=100, wire=22, n=9, loop=14):
    band = s3d.torus("scarf_band", d, wire)
    s3d.material(band, "fabric", color="#bdbdbd")
    loops = s3d.at(s3d.torus("loop", loop, 3.5), on=s3d.ring(n, d / 2 + 8, start=140, angle=260), z=2)
    s3d.material(loops[0] if isinstance(loops, list) else loops, "fabric", color="#d6d6d6")
    return s3d.group("scarf", band, loops)


def wing_part(l=75, w=30, t=14):
    ob = s3d.loft("wing",
                  s3d.station(z=0, w=w * 0.5, d=t),
                  s3d.station(z=l * 0.4, w=w, d=t * 1.2),
                  s3d.station(z=l, w=w * 0.2, d=t * 0.5))
    s3d.material(ob, "plastic", color=GREY)
    return s3d.at(ob, rx=-135, ry=-10)    # folded down and back


def tail_part(l=40):
    ob = s3d.wedge("tail", 50, 14, l, top=14)
    s3d.material(ob, "plastic", color=GREY)
    return s3d.at(ob, rx=80)


def legs_part(h=70, gap=34, d=6):
    leg = s3d.wire("leg", [(0, 0, h), (0, 0, 10)], d)
    toes = [s3d.wire("toe", [(0, 0, 4), (dx, dy, 0)], 4)
            for dx, dy in ((0, -20), (-14, -12), (14, -12))]
    foot = s3d.group("foot", leg, *toes)
    s3d.material(foot, "plastic", color=GREY)
    left = s3d.at(foot, x=-gap / 2)
    right = s3d.transform(s3d.copy(left), mirror="x")
    return s3d.group("legs", left, right)


if __name__ == "__main__":
    s3d.export(mama_bird(), "mama_bird.glb")
