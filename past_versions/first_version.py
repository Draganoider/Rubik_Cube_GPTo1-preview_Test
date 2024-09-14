from vpython import *
import random

# Создаем окно сцены
scene = canvas(
    title="Кубик Рубика",
    width=800,
    height=600,
    center=vector(0, 0, 0),
    background=color.gray(0.2),
)

# Определяем цвета граней
face_colors = {
    "U": color.white,  # Верхняя грань - белый
    "D": color.yellow,  # Нижняя грань - желтый
    "F": color.green,  # Передняя грань - зеленый
    "B": color.blue,  # Задняя грань - синий
    "L": color.orange,  # Левая грань - оранжевый
    "R": color.red,  # Правая грань - красный
}


# Создаем маленькие кубики (кубики называются "кубики")
def create_cubes():
    cubes = []
    positions = [-1, 0, 1]
    for x in positions:
        for y in positions:
            for z in positions:
                pos = vector(x, y, z)
                # Создаем каждый маленький кубик как compound объект из шести сторон
                faces = []
                size = 0.98
                # Определяем позиции граней
                face_defs = [
                    {
                        "normal": vector(0, 0, 1),
                        "color": face_colors["F"],
                        "condition": z == 1,
                    },  # Передняя грань
                    {
                        "normal": vector(0, 0, -1),
                        "color": face_colors["B"],
                        "condition": z == -1,
                    },  # Задняя грань
                    {
                        "normal": vector(0, 1, 0),
                        "color": face_colors["U"],
                        "condition": y == 1,
                    },  # Верхняя грань
                    {
                        "normal": vector(0, -1, 0),
                        "color": face_colors["D"],
                        "condition": y == -1,
                    },  # Нижняя грань
                    {
                        "normal": vector(-1, 0, 0),
                        "color": face_colors["L"],
                        "condition": x == -1,
                    },  # Левая грань
                    {
                        "normal": vector(1, 0, 0),
                        "color": face_colors["R"],
                        "condition": x == 1,
                    },  # Правая грань
                ]
                for face_def in face_defs:
                    if face_def["condition"]:
                        face = box(
                            pos=pos + 0.5 * face_def["normal"],
                            size=vector(size, size, 0.02),
                            color=face_def["color"],
                            up=face_def["normal"],
                        )
                        faces.append(face)
                # Создаем серый кубик без видимых граней
                inner_cube = box(
                    pos=pos,
                    size=vector(size, size, size),
                    color=color.gray(0.5),
                    opacity=0,
                )
                # Объединяем грани и внутренний кубик
                cubie = compound([inner_cube] + faces)
                cubes.append({"cubie": cubie, "pos": pos})
    return cubes


cubes = create_cubes()


# Функция вращения слоя кубика с анимацией
def rotate_layer(axis, layer, angle):
    steps = 20
    dt = angle / steps
    for step in range(steps):
        rate(60)
        for item in cubes:
            cubie = item["cubie"]
            pos = item["pos"]
            if axis == "x" and abs(pos.x - layer) < 0.1:
                cubie.rotate(angle=dt, axis=vector(1, 0, 0), origin=vector(layer, 0, 0))
            elif axis == "y" and abs(pos.y - layer) < 0.1:
                cubie.rotate(angle=dt, axis=vector(0, 1, 0), origin=vector(0, layer, 0))
            elif axis == "z" and abs(pos.z - layer) < 0.1:
                cubie.rotate(angle=dt, axis=vector(0, 0, 1), origin=vector(0, 0, layer))
    # Обновляем позиции кубиков после вращения
    for item in cubes:
        cubie = item["cubie"]
        # Исправление: используем округление для каждого компонента отдельно
        item["pos"] = vector(round(cubie.pos.x), round(cubie.pos.y), round(cubie.pos.z))


# Стек ходов для решения
solution_steps = []


# Функция решения кубика (пошагово)
def solve_cube_step():
    if solution_steps:
        move = solution_steps.pop(0)
        rotate_layer(move["axis"], move["layer"], move["angle"])
    else:
        print("Кубик собран!")


# Генерация случайных ходов и заполнение стека решения
def generate_scramble():
    moves = ["x", "y", "z"]
    layers = [-1, 0, 1]
    scramble = []
    for _ in range(10):  # Меньше ходов для быстрого перемешивания
        axis = random.choice(moves)
        layer = random.choice(layers)
        angle = random.choice([pi / 2, -pi / 2])
        scramble.append({"axis": axis, "layer": layer, "angle": angle})
        # Добавляем обратный ход в решение
        solution_steps.insert(0, {"axis": axis, "layer": layer, "angle": -angle})
    return scramble


# Применяем перемешивание
def apply_scramble(scramble):
    for move in scramble:
        rotate_layer(move["axis"], move["layer"], move["angle"])


# Инициализация кубика
scramble = generate_scramble()
apply_scramble(scramble)


# Обработка нажатий клавиш
def keyInput(evt):
    s = evt.key
    if s == " ":
        solve_cube_step()


scene.bind("keydown", keyInput)
