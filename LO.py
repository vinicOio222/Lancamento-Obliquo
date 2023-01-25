from vpython import *

def deslocar(corpo):
    global dt
    queda = True
    p = corpo.traj.point(corpo.traj.npoints - 1)["pos"]
    corpo.pos += dt*corpo.v + dt**2*corpo.a/2.
    if corpo.v.y < 0 and corpo.pos.y < corpo.radius:
        if p.y != corpo.pos.y:
            f = (p.y - corpo.radius)/(p.y - corpo.pos.y)
            corpo.pos -= (1 - f)*(corpo.pos - p)
            corpo.v += f*dt*corpo.a
            corpo.t += f*dt
        queda = False
    else:
        corpo.t += dt 
        corpo.v += dt*corpo.a
    corpo.traj.append(pos = vec(corpo.pos))
    corpo.d += mag(corpo.pos - p)
    return queda

def resultados(corpo):
    p0 = corpo.traj.point(0)["pos"]
    alcance = corpo.pos.x - p0.x
    velocidade = corpo.d / corpo.t
    scene.caption += "<b>" + corpo.legenda + "</b>\n"
    scene.caption += "Tempo total = {:.2f} s\n".format(corpo.t)
    scene.caption += "Alcance horizontal = {:.2f} m\n".format(alcance)
    scene.caption += "Distância percorrida = {:.2f} m\n".format(corpo.d)
    scene.caption += "Velocidade média = {:.2f} m/s\n".format(velocidade)
    scene.caption += "Altura máxima = {:.2f} m\n\n".format(corpo.alt)
    return 

def projetar(corpo, vel, ang, leg):
    corpo.v = vel*vec(cos(ang*pi/180.), sin(ang*pi/180.), 0)
    corpo.t = corpo.d = 0
    corpo.legenda = leg 
    corpo.traj = curve(pos = vec(corpo.pos),color = corpo.color) 
    corpo.alt = (vel**2)*(sin(ang*pi/180.)**2) / (2*9.8)

scene = canvas(title = "<h1>Movimento Balístico Completo</h1>", forward = vec(-0.5, -0.2, -1))
scene.caption = ""
a = 47.
dt = 0.01
g = vec(0, -9.8, 0)
q1 = q2 = q3 = True

bola1 = sphere(pos = vec(-7.5, 0.2, 1), radius = 0.2, color = vec(0.93, 1, 0.16))
bola2 = sphere(pos = vec(-7.5, 0.1, 0), radius = 0.2, color = vec(1, 0, 0))
bola3 = sphere(pos = vec(-7.5, 0.1, -1), radius = 0.2, color = vec(1, 0.49, 0.05))
solo = box(pos = vec(0, -0.1, 0), size = vec(16 , 0.2, 10),texture = textures.metal)
parede = box(pos = vec(0, 2.8, -5.05), size = vec(16, 6, 0.1), color = vec(0.7, 0.7, 0.7))
sitio = text(pos = vec(0, 2.8, - 5), text = "Movimento balístico", color = color.blue, align = "center", depht = 0)

projetar(bola1, 8, 37., "Bola Amarela")
projetar(bola2, 7, 45., "Bola Vermelha")
projetar(bola3, 12.5, 60., "Bola Laranja")

bola2.a = g
bola1.a = g
bola3.a = g

while q1 or q2 or q3:
     rate(100)
     if q1: q1 = deslocar (bola1)
     if q2: q2 = deslocar (bola2)
     if q3: q3 = deslocar (bola3)

resultados(bola1)
resultados(bola2)
resultados(bola3)