"""Mama bird, v2: a stylised sand3d version of the sculpt, built as ONE solid for 3D printing.

Front is -Y, up is +Z, millimetres. Feet stand flat on z = 0.
"""
import math

import sand3d as s3d

GREY = "#c9c9c9"


def mama_bird(leg_h=75, body_w=125, head_h=150, head_w=105):
    """The head of the program: one line per part, all fused into one printable solid."""
    body_z = leg_h - 8
    neck_z = body_z + 62
    body = s3d.at(body_part(body_w), z=body_z)
    legs = s3d.at(chicken_legs(leg_h + 12), y=-4)
    scarf = s3d.at(scarf_part(d=head_w * 0.95), z=neck_z)
    head = s3d.at(head_part(head_h, head_w), z=neck_z + 4)
    wing = s3d.at(wing_part(), x=body_w / 2 - 8, y=6, z=leg_h + 30)
    twin = s3d.transform(s3d.copy(wing), mirror="x")
    tail = s3d.at(tail_part(), y=body_w / 2 - 20, z=leg_h + 4)
    s3d.join(body, legs, scarf, head, wing, twin, tail)
    s3d.material(body, "plastic", color=GREY)
    return body


def blob(name, w, d, thick):
    """A soft lump: w wide, d tall once it is turned to face front, thick deep. Built along Z."""
    return s3d.loft(name,
                    s3d.station(z=0, w=w * 0.7, d=d * 0.7),
                    s3d.station(z=thick * 0.45, w=w, d=d),
                    s3d.station(z=thick, w=w * 0.35, d=d * 0.35))


def face_blob(name, w, d, thick, x=0, y=0, z=0, tilt=0):
    """A blob that bulges toward -Y, its base at y."""
    return s3d.at(blob(name, w, d, thick), x=x, y=y, z=z, rx=90, ry=tilt)


def head_part(h=150, w=105):
    skull = s3d.loft("skull",
                     s3d.station(z=0, w=w * 0.55, d=w * 0.5, y=-4),
                     s3d.station(z=h * 0.25, w=w * 0.98, d=w * 0.88, y=-2),
                     s3d.station(z=h * 0.5, w=w, d=w * 0.9),
                     s3d.station(z=h * 0.8, w=w * 0.78, d=w * 0.75, y=2),
                     s3d.station(z=h, w=w * 0.3, d=w * 0.3, y=3))
    f = -w * 0.33                     # where the face blobs start, inside the skull
    # one side of the face (heavy closed lids and brows, cheeks, jowls, nostril), mirrored below
    side = [
        face_blob("lid", w * 0.30, h * 0.10, 16, x=-w * 0.21, y=f, z=h * 0.55, tilt=4),
        face_blob("brow", w * 0.36, h * 0.07, 15, x=-w * 0.22, y=f, z=h * 0.64, tilt=-10),
        face_blob("cheek", w * 0.40, h * 0.22, 19, x=-w * 0.27, y=f, z=h * 0.30),
        face_blob("jowl", w * 0.30, h * 0.16, 19, x=-w * 0.27, y=f, z=h * 0.13),
        face_blob("nostril", w * 0.13, h * 0.06, 18, x=-w * 0.07, y=f, z=h * 0.38),
    ]
    mirrored = [s3d.transform(s3d.copy(p), mirror="x") for p in side]
    centre = [
        face_blob("bridge", w * 0.17, h * 0.22, 24, y=f, z=h * 0.50),
        face_blob("nose_tip", w * 0.21, h * 0.10, 28, y=f, z=h * 0.39),
        face_blob("upper_lip", w * 0.30, h * 0.055, 21, y=f, z=h * 0.265),
        face_blob("lower_lip", w * 0.26, h * 0.06, 21, y=f, z=h * 0.20),
        face_blob("chin", w * 0.38, h * 0.12, 24, y=f, z=h * 0.075),
    ]
    ear = s3d.at(s3d.sphere("ear", 24), x=w / 2 - 2, y=3, z=h * 0.42)
    twin_ear = s3d.transform(s3d.copy(ear), mirror="x")
    crest = s3d.at(crest_part(), z=h - 6, y=3)
    s3d.join(skull, *side, *mirrored, *centre, ear, twin_ear, crest)
    return skull


def crest_part(n=7, r=11, h=34):
    base = s3d.cylinder("crest_base", 2 * r + 4, 8)
    spikes = s3d.at(s3d.cone("spike", 10, h, d2=1), on=s3d.ring(n, r), z=4)
    s3d.join(base, spikes)
    return base


def body_part(w=125, h=75):
    return s3d.loft("body",
                    s3d.station(z=0, w=w * 0.5, d=w * 0.45),
                    s3d.station(z=h * 0.4, w=w, d=w * 0.85),
                    s3d.station(z=h * 0.8, w=w * 0.8, d=w * 0.7),
                    s3d.station(z=h, w=w * 0.45, d=w * 0.4))


def scarf_part(d=100, wire=24, n=9, loop=15):
    band = s3d.torus("scarf_band", d, wire)
    loops = s3d.at(s3d.torus("loop", loop, 5), on=s3d.ring(n, d / 2 + 10, start=140, angle=260), z=2)
    s3d.join(band, loops)
    return band


def wing_part(l=75, w=30, t=16):
    ob = s3d.loft("wing",
                  s3d.station(z=0, w=w * 0.5, d=t),
                  s3d.station(z=l * 0.4, w=w, d=t * 1.2),
                  s3d.station(z=l, w=w * 0.25, d=t * 0.6))
    return s3d.at(ob, rx=-135, ry=-10)    # folded down and back


def tail_part(l=40):
    return s3d.at(s3d.wedge("tail", 50, 16, l, top=16), rx=80)


def chicken_legs(h=87, gap=62):
    left = s3d.at(chicken_leg(h), x=-gap / 2)
    right = s3d.transform(s3d.copy(left), mirror="x")
    s3d.join(left, right)
    return left


def chicken_leg(h=87, d=11, toe_l=40, toe_w=9, toe_h=7):
    """A shank on a flat foot: three toes forward, one back, claws at the tips."""
    shank = s3d.cylinder("shank", d, h)
    ankle = s3d.cylinder("ankle", d * 2, toe_h)
    toes = [toe("toe_f", toe_l, toe_w, toe_h, -90 + a) for a in (-38, 0, 38)]
    toes.append(toe("toe_b", toe_l * 0.6, toe_w, toe_h, 90))
    s3d.join(shank, ankle, *toes)
    return shank


def toe(name, l, w, h, angle):
    """A flat toe of length l from the ankle, turned by angle about the ankle, a claw at its tip."""
    bar = s3d.extrude(name, s3d.slot(l, w), h)
    claw = s3d.at(s3d.cone(name + "_claw", w * 0.9, w * 1.4, d2=1), x=l / 2 + w * 0.5, z=h / 2, ry=90)
    s3d.join(bar, claw)
    c, s = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    return s3d.at(bar, x=c * l / 2, y=s * l / 2, rz=angle)


if __name__ == "__main__":
    s3d.export(mama_bird(), "mama_bird.glb")
    s3d.export(mama_bird(), "mama_bird.stl")
