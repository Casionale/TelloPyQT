#!/usr/bin/python3
# -*- coding: utf-8 -*-
import math
import sys

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QThread
from PyQt5.QtWidgets import QGraphicsScene

import start
from MainWindow import Ui_MainWindow


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.BtnStart.clicked.connect(self.btn_start)
        self.ui.BtnStop.clicked.connect(self.btn_landing)
        self.ui.BtnSave.clicked.connect(self.btn_generate)
        self.configure_method()

        self.graphic = self.ui.GWindow

        scene = GraphicsScene()
        for i in range(0, 26):
            scene.addLine(i * 20, 0, i * 20, 510, QPen(Qt.green))
        for i in range(0, 26):
            scene.addLine(0, i * 20, 510, i * 20, QPen(Qt.green))
        # font = QFont("Arial", 14, 2, False)
        # scene.addText("Черти путь сдесь", font)
        self.graphic.setScene(scene)
        self.ui.GWindow.scene().changed.connect(self.ui.GWindow.updateScene)

    def configure_method(self):
        self.worker_thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.worker_thread)
        self.worker.points.connect(self.flying)
        self.worker_thread.started.connect(self.worker.run)

    @staticmethod
    def btn_start():
        print("Нажата кнопка старт")
        application.worker_thread.start()

    @staticmethod
    def btn_landing():
        print("Нажата кнопка принудительной пасадки")

    @staticmethod
    def btn_generate():
        print("Нажата кнопка генерации маршрута")
        generator = CommandGenerator()
        generator.generating_commands()
        print(Commands)

    """Здеся буит обработка сообщений шо там с коптером"""
    @QtCore.pyqtSlot(object)
    def flying(self, points):

        print(points)

    def keyPressEvent(self, e):
        if e.key() in [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]:
            pass
        else:
            super(MyWindow, self).keyPressEvent(e)
            if (e.key() == QtCore.Qt.Key_Control):
                print("БЫЛ НАЖАТ КОНТРЛ!")


class Worker(QObject):
    running = False
    points = pyqtSignal(object)

    def run(self):
        start.starting(Commands)


class CommandGenerator():
    def generating_commands(self):
        Commands.clear()
        if len(Points) > 2:
            for i in range(0, len(Points)):
                if i == 0:
                    Commands.append("command")
                    Commands.append("takeoff")
                    # angle = math.acos((Points[0][1] - Points[1][1]) /
                    # math.sqrt((Points[1][1] - Points[2][1]) * (Points[1][1] - Points[2][1]) +
                    # (Points[2][0] - Points[1][0]) * (Points[2][0] - Points[1][0]))) * (180 / math.pi)
                    # Commands.append("cw "+str(round(angle)))
                else:
                    if (i != len(Points)-1):
                        angle = self.angle3(Points[i-1][0], Points[i-1][1], Points[i][0], Points[i][1], Points[i + 1][0],
                                            Points[i + 1][1])
                        Commands.append(self.forward_command(Points[i][0], Points[i][1], Points[i+1][0], Points[i+1][1]))
                        Commands.append(self.direction_command(
                            Points[i-1][0], Points[i-1][1], Points[i][0], Points[i][1], Points[i + 1][0], Points[i + 1][1]
                        ) + str(round(angle)))
            Commands.append("land")
        else:
            print("Точек слишком мало")


    def forward_command(self, x, y, x1, y1):
        distance = math.sqrt((x1-x)*(x1-x) + (y1-y)*(y1-y))
        return "forward " + str(round(distance))

    def direction_command(self, px, py, x, y, x1, y1):
        if y >= py and (((x-px)*(y1-py) / (y-py)) + px) >= x1 or (x1 > x and py > y):
            return "сcw "
        else:
            return "cw "

    def angle3(self, ax, ay, bx, by, dx, dy):
        cx = bx
        cy = by
        x1 = bx - ax
        y1 = by - ay
        x2 = dx - cx
        y2 = dy - cy
        abcd = x1 * x2 + y1 * y2
        longa = math.sqrt(x1 * x1 + y1 * y1)
        longb = math.sqrt(x2 * x2 + y2 * y2)
        return math.acos(abcd / (longa * longb)) * 180 / math.pi

    def super_angle2(self, ax, ay, bx, by, dx, dy):
        top = (bx - ax) * (dx - ax) + (by - ay) * (dy - bx)
        bottom = math.sqrt(
            ((bx - ax) ** 2 + (by - ay) ** 2) * ((dx - bx) ** 2 * (dy - by) ** 2)
        )
        return (top / bottom) * (180 / math.pi)


class GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)
        self.setSceneRect(0, 0, 520, 520)

    def mousePressEvent(self, event):
        x = event.scenePos().x()
        y = 520 - event.scenePos().y()
        Points.append([x, y])
        print([x, y])
        scense = GraphicsScene()
        for i in range(0, 26):
            scense.addLine(i * 20, 0, i * 20, 510, QPen(Qt.green))
        for i in range(0, 26):
            scense.addLine(0, i * 20, 510, i * 20, QPen(Qt.green))
        for i in range(0, len(Points)):
            scense.addEllipse(Points[i][0] - radiusPoint, 520 - Points[i][1] - radiusPoint, radiusPoint * 2, radiusPoint * 2,
                              QPen(), QBrush())
            if i > 0:
                scense.addLine(Points[i-1][0], 520 - Points[i-1][1], Points[i][0], 520 - Points[i][1], QPen())
        application.graphic.setScene(scense)
        application.window().update()


Points = []
Commands = []

radiusPoint = 5

app = QtWidgets.QApplication([])

application = MyWindow()
application.show()
sys.exit(app.exec())
