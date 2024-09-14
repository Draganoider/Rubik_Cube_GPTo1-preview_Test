from vpython import *
import random

# Scene setup
scene = canvas(title="3D Rubik's Cube", width=800, height=600, center=vector(0, 0, 0))
scene.userspin = True
scene.userzoom = True
scene.autoscale = False

# Defining colors
colors = {
    "U": color.white,  # Up
    "D": color.yellow,  # Down
    "F": color.green,  # Front
    "B": color.blue,  # Back
    "L": color.orange,  # Left
    "R": color.red,  # Right
}

# Initializing cube pieces
cube_pieces = []

offset = 1.05  # Slightly more than 1 to avoid overlapping
for x in [-offset, 0, offset]:
    for y in [-offset, 0, offset]:
        for z in [-offset, 0, offset]:
            piece = box(
                pos=vector(x, y, z),
                size=vector(0.98, 0.98, 0.98),
                color=color.gray(0.2),
            )
            # Adding stickers
            stickers = []
            if y > 0.5:
                stickers.append(
                    box(
                        pos=piece.pos + vector(0, 0.51, 0),
                        size=vector(0.95, 0.02, 0.95),
                        color=colors["U"],
                    )
                )
            if y < -0.5:
                stickers.append(
                    box(
                        pos=piece.pos + vector(0, -0.51, 0),
                        size=vector(0.95, 0.02, 0.95),
                        color=colors["D"],
                    )
                )
            if z > 0.5:
                stickers.append(
                    box(
                        pos=piece.pos + vector(0, 0, 0.51),
                        size=vector(0.95, 0.95, 0.02),
                        color=colors["F"],
                    )
                )
            if z < -0.5:
                stickers.append(
                    box(
                        pos=piece.pos + vector(0, 0, -0.51),
                        size=vector(0.95, 0.95, 0.02),
                        color=colors["B"],
                    )
                )
            if x < -0.5:
                stickers.append(
                    box(
                        pos=piece.pos + vector(-0.51, 0, 0),
                        size=vector(0.02, 0.95, 0.95),
                        color=colors["L"],
                    )
                )
            if x > 0.5:
                stickers.append(
                    box(
                        pos=piece.pos + vector(0.51, 0, 0),
                        size=vector(0.02, 0.95, 0.95),
                        color=colors["R"],
                    )
                )
            cube_pieces.append({"piece": piece, "stickers": stickers})


# Rotation functions
def rotate_face(axis, coord, angle):
    moving_pieces = []
    for cubie in cube_pieces:
        if abs(getattr(cubie["piece"].pos, axis) - coord) < 0.1:
            moving_pieces.append(cubie)
    for i in range(90):
        rate(480)
        for cubie in moving_pieces:
            cubie["piece"].rotate(
                angle=radians(angle / 90),
                axis=vector_axis(axis),
                origin=vector_origin(axis, coord),
            )
            for sticker in cubie["stickers"]:
                sticker.rotate(
                    angle=radians(angle / 90),
                    axis=vector_axis(axis),
                    origin=vector_origin(axis, coord),
                )


def vector_axis(axis):
    return {"x": vector(1, 0, 0), "y": vector(0, 1, 0), "z": vector(0, 0, 1)}[axis]


def vector_origin(axis, coord):
    if axis == "x":
        return vector(coord, 0, 0)
    elif axis == "y":
        return vector(0, coord, 0)
    else:
        return vector(0, 0, coord)


# Defining moves
def U():
    rotate_face("y", offset, -90)


def U_prime():
    rotate_face("y", offset, 90)


def D():
    rotate_face("y", -offset, 90)


def D_prime():
    rotate_face("y", -offset, -90)


def F():
    rotate_face("z", offset, -90)


def F_prime():
    rotate_face("z", offset, 90)


def B():
    rotate_face("z", -offset, 90)


def B_prime():
    rotate_face("z", -offset, -90)


def L():
    rotate_face("x", -offset, -90)


def L_prime():
    rotate_face("x", -offset, 90)


def R():
    rotate_face("x", offset, 90)


def R_prime():
    rotate_face("x", offset, -90)


# Scrambling the cube
moves = [U, U_prime, D, D_prime, F, F_prime, B, B_prime, L, L_prime, R, R_prime]
scramble_moves = random.choices(moves, k=10)

for move in scramble_moves:
    move()

# Creating a list of reverse moves for solving
solution_moves = []
for move in reversed(scramble_moves):
    # Adding the reverse move to the solution list
    if move == U:
        solution_moves.append(U_prime)
    elif move == U_prime:
        solution_moves.append(U)
    elif move == D:
        solution_moves.append(D_prime)
    elif move == D_prime:
        solution_moves.append(D)
    elif move == F:
        solution_moves.append(F_prime)
    elif move == F_prime:
        solution_moves.append(F)
    elif move == B:
        solution_moves.append(B_prime)
    elif move == B_prime:
        solution_moves.append(B)
    elif move == L:
        solution_moves.append(L_prime)
    elif move == L_prime:
        solution_moves.append(L)
    elif move == R:
        solution_moves.append(R_prime)
    elif move == R_prime:
        solution_moves.append(R)

# Index of the current move in the solution
current_move_index = 0
solving = True


def on_keydown(evt):
    global current_move_index, solving
    s = evt.key
    if s == " " and solving:
        if current_move_index < len(solution_moves):
            solution_moves[current_move_index]()
            current_move_index += 1
        else:
            solving = False
            print("Cube is solved!")
    # You can add other key functions here


# Binding the keydown event handler
scene.bind("keydown", on_keydown)

# Keeping the window open and processing events
while True:
    rate(240)
    pass  # Just waiting for events
