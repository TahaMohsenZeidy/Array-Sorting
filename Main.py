from PyQt5 import QtWidgets
import sys
from PyQt5.QtGui import QPixmap
import matplotlib.animation as animation
import TableSorting
import master as srt
import random
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt



class designWindow(QtWidgets.QMainWindow, TableSorting.Ui_MainWindow):
    def __init__(self):
        super(designWindow, self).__init__()
        self.setupUi(self)
        self.fig=plt.figure()
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.non_sorted_list = []
        self.validate=False
        self.choosing=False
        self.res_test=False
        self.pos = self.horizontalSlider.sliderPosition()
        self.vlBtn.clicked.connect(self.inputlist)
        self.vlBtn.clicked.connect(self.set_etat)
        self.pushButton_1.clicked.connect(self.selectionSort)
        self.pushButton_2.clicked.connect(self.insertionSort)
        self.pushButton_3.clicked.connect(self.quickSort)
        self.pushButton_4.clicked.connect(self.fusionSort)
        self.pushButton_5.clicked.connect(self.bubbleSort)
        self.bgn_btn.clicked.connect(self.validate_sort)
        self.random_btn.clicked.connect(self.generate_random)
        self.listview_btn.clicked.connect(self.listview)
        self.res_btn.clicked.connect(self.reset_def)


    def set_etat(self):
        self.validate=True

    def inputlist(self):
        mylist = self.lineEdit_1.text()
        try:
            self.non_sorted_list = list(map(int, mylist.split(' ')))
            tale = self.non_sorted_list[:]
            self.table = srt.E_sort(tale)
        except:
            self.lineEdit_1.clear()
            self.lineEdit_1.setText("ERROR, NON-COMPATIBLE LIST, INPUT A VALID LIST !!")
            self.lineEdit_1.setStyleSheet("color:rgb(255, 0, 0);\n""font: 75 18pt \"MS Shell Dlg 2\";\n")
        self.random_btn.setEnabled(False)
        self.listview_btn.setEnabled(True)
        self.lineEdit_2.clear()


    def validate_sort(self):
        self.horizontalLayoutWidget_4.setEnabled(True)
        self.random_btn.setEnabled(True)
        self.pushButton_1.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        chaine = ""
        for var in self.table:
            if type(var) == int:
                chaine += str(var) + "  "
        self.lineEdit_2.setText(chaine)
        if self.validate == False or self.choosing == False :
            self.lineEdit_1.setText("You need to choose a sorting algorithm and validate !")
            self.lineEdit_1.setStyleSheet(
                    "color:rgb(255, 0, 0);\n""font-weight:bold;""font: 75 22pt \"MS Shell Dlg 2\";\n")
        else:
            self.pos = self.horizontalSlider.sliderPosition()
            self.horizontalSlider.setEnabled(False)
            if self.pos == 1:
                self.plot_fig(60)
            if self.pos == 2:
                self.plot_fig(30)
            if self.pos == 0:
                self.plot_fig()

    def selectionSort(self):
        self.generator = srt.selectionsort(self.non_sorted_list)
        self.show_image('selection.png')
        self.choosing=True

    def insertionSort(self):
        self.generator = srt.insertionsort(self.non_sorted_list)
        self.show_image('insertion.png')
        self.choosing = True

    def quickSort(self):
        self.generator = srt.quicksort(self.non_sorted_list, 0,len(self.non_sorted_list) -1)
        self.show_image('quick.png')
        self.choosing = True


    def fusionSort(self):
        self.generator = srt.mergesort(self.non_sorted_list,0 ,len(self.non_sorted_list) -1)
        self.show_image('fusion.png')
        self.choosing = True

    def bubbleSort(self):
        self.generator = srt.bubblesort(self.non_sorted_list)
        self.show_image('bubble.png')
        self.choosing = True



    def plot_fig(self,delay=100):
        layout = self.horizontalLayout_4
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.horizontalLayoutWidget_4.show()
        ax = self.figure.add_subplot(111)
        ax.clear()
        iteration = [0]
        bar_rects = ax.bar(range(len(self.non_sorted_list)), self.non_sorted_list, align="edge")
        def update_fig(A, rects, iteration):
            for rect, val in zip(rects, A):
                rect.set_height(val)
            iteration[0] += 1
        anim = animation.FuncAnimation(self.figure, func=update_fig,fargs=(bar_rects, iteration), frames=self.generator, interval=delay, repeat=False)
        plt.show(block=False)
        plt.ion()
        plt.close()
        self.canvas.draw()
        self.bgn_btn.setEnabled(False)




    def generate_random(self):
        self.non_sorted_list = [random.randint(-200, 200) for x in range(random.randint(15,16))]
        chaine = ""
        last_el = self.non_sorted_list[-1]
        for i in self.non_sorted_list:
            if i != last_el:
                chaine += str(i) + " "
            else:
                chaine += str(last_el)
        self.lineEdit_1.setText(chaine)
        self.pushButton_1.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(True)
        self.pushButton_5.setEnabled(True)
        self.bgn_btn.setEnabled(True)

    def after_sort(self):
        self.lineEdit_2.clear()
        chaine = ""
        for var in self.table:
            if type(var) == int:
                chaine += str(var) + "  "
        self.lineEdit_2.setText(chaine)
        self.listview_btn.setText("List View")
        self.listview_btn.clicked.connect(self.listview)


    def listview(self):
        self.lineEdit_2.clear()
        chaine = "|"
        for var in self.table:
            if type(var) == int:
                chaine += str(var) + "|"
        self.lineEdit_2.setStyleSheet("color:rgb(0, 0, 0);\n""font-weight:bold;""font: 75 22pt \"MS Shell Dlg 2\";\n")
        self.lineEdit_2.setText(chaine)
        self.listview_btn.setText("Text View")
        self.listview_btn.clicked.connect(self.after_sort)


    def show_image(self,img):
        pixmap = QPixmap(img)
        self.label_1.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        self.show()


    def reset_def(self):
        self.lineEdit_1.clear()
        self.lineEdit_2.clear()
        self.res_test=True
        self.pushButton_1.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(True)
        self.pushButton_5.setEnabled(True)
        self.listview_btn.setEnabled(True)
        self.bgn_btn.setEnabled(True)
        self.horizontalLayoutWidget_4.hide()
        self.horizontalSlider.setEnabled(True)
        


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = designWindow()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()
