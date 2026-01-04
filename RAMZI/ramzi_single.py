
import gdsfactory as gf
gf.gpdk.PDK.activate()

port_offset=10
ring_gap=0.5
ring_radius=20
ring_delx=0
ring_dely=0

bend_radius=5
bend_width=0.5
bend_angle=90
bend_layer=(1,0)

arm_length=50
delta_length=20
top=gf.Component('top')

@gf.cell
def straight(l,o):
    c=gf.Component()
    sth = c << gf.components.straight(length=l, npoints=2)
    sth.rotate(o)
    c.add_port("o1", port=sth.ports["o1"])
    c.add_port("o2", port=sth.ports["o2"])
    return c
@gf.cell
def bend(r,w,a,l,o):
    c=gf.Component()
    arc = c << gf.components.bend_circular(radius=r, width=w, angle=a, layer=l)
    arc.rotate(o)
    c.add_port("o1", port=arc.ports["o1"])
    c.add_port("o2", port=arc.ports["o2"])
    return c
@gf.cell
def ring_single(g,r,x0,y0):
    c=gf.Component()
    rs=c<< gf.components.ring_single(gap=g, radius=r, length_x=x0, length_y=y0)
    c.add_port("o1", port=rs.ports["o1"])
    c.add_port("o2", port=rs.ports["o2"])
    return c
  
quad1=top<<bend(bend_radius,bend_width,bend_angle,bend_layer,0)
quad11=top<<bend(bend_radius,bend_width,bend_angle,bend_layer,0)
quad2=top<<bend(bend_radius,bend_width,bend_angle,bend_layer,90)
quad22=top<<bend(bend_radius,bend_width,bend_angle,bend_layer,90)
quad3=top<<bend(bend_radius,bend_width,bend_angle,bend_layer,180)
quad33=top<<bend(bend_radius,bend_width,bend_angle,bend_layer,180)
quad4=top<<bend(bend_radius,bend_width,bend_angle,bend_layer,270)
quad44=top<<bend(bend_radius,bend_width,bend_angle,bend_layer,270)
ring1=top<<ring_single(ring_gap,ring_radius,ring_delx,ring_dely)
delta_arm_left=top<<straight(delta_length,90)
delta_arm_right=top<<straight(delta_length,90)
upper_arm=top<<straight(arm_length,0)
lower_arm=top<<straight(arm_length+ring1.xsize,0)
print(ring1.xsize)

quad1.movey(port_offset)
quad3.connect("o2", other=quad1.ports["o2"])
ring1.connect("o1", other=quad3.ports["o1"])
upper_arm.connect("o2", other=ring1.ports["o2"])
quad22.connect("o2", other=upper_arm.ports["o1"])
quad44.connect("o1", other=quad22.ports["o1"])

quad2.move([bend_radius,-bend_radius])
delta_arm_left.connect("o1", other=quad2.ports["o1"])
quad4.connect("o1", other=delta_arm_left.ports["o2"])
lower_arm.connect("o2", other=quad4.ports["o2"])
quad11.connect("o1", other=lower_arm.ports["o1"])
delta_arm_right.connect("o2", other=quad11.ports["o2"])
quad33.connect("o2", other=delta_arm_right.ports["o1"])

top.show()

#c.write_gds("ramzi.gds")  # Write it to a GDS file. You can open it in klayout.
