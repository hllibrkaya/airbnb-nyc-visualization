import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QComboBox, QPushButton, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

dataset = pd.read_csv("AB_NYC_2019.csv")


class Plot(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New York City Airbnb Plots")
        self.screen_width, self.screen_height = self.geometry().width(), self.geometry().height()
        self.resize(self.screen_width * 3, self.screen_height * 3)

        layout = QVBoxLayout()
        self.combo_box = QComboBox()
        self.combo_box.addItem("Correlation Matrix")
        self.combo_box.addItem("Pie Chart- Room Type-Price")
        self.combo_box.addItem("Bar Plot- Average prices by neighbourhood")
        self.combo_box.addItem("Bar Plot Horizontal- Amount of Room Types")
        self.combo_box.addItem("Bar Plot- Amount of Neighbourhood Groups")
        self.combo_box.addItem("Bar Plot- Neighbourhood Density")
        self.combo_box.addItem("Bar Plot- N-GROUP - PRICE - ROOM-TYPE")
        self.combo_box.addItem("Violin-Plot Distribution of Prices by Room Type")
        self.combo_box.addItem("Scatter Plot- Price Distribution by Neighborhood Group")
        self.combo_box.addItem("Scatter Plot- Prices by coordinates")
        self.combo_box.addItem("Line Plot- Change of prices over the years according to room type")
        self.combo_box.addItem("Hist Plot- Price Count")
        self.combo_box.addItem("Kde Plot- Price Density")
        layout.addWidget(self.combo_box)

        self.button = QPushButton("Show the graph")
        self.button.clicked.connect(self.show_plot)
        layout.addWidget(self.button)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()

    def show_plot(self):
        selection = self.combo_box.currentText()

        temp = dataset
        plt.clf()
        plt.rcParams.update({'font.size': 20})

        if selection == "Correlation Matrix":
            sns.heatmap(temp.corr(), annot=True)

        elif selection == "Pie Chart- Room Type-Price":
            temp.groupby("room_type")["price"].sum().plot.pie(autopct="%.2f%%", ylabel="", legend=True)
            plt.title("Room Type - Price")

        elif selection == "Bar Plot- Average prices by neighbourhood":
            mean_prices = temp.groupby("neighbourhood_group")["price"].mean().reset_index()
            sns.barplot(data=mean_prices, x='neighbourhood_group', y='price').set_title(
                "Average prices by neighbourhood")
            plt.xlabel("Neighbourhood")
            plt.ylabel("Price")

        elif selection == "Bar Plot Horizontal- Amount of Room Types":
            temp["room_type"].value_counts().plot.barh().set_title("Amount of Room Types")

        elif selection == "Bar Plot- Amount of Neighbourhood Groups":
            temp["neighbourhood_group"].value_counts().plot.bar().set_title("Neighbourhood Groups")

        elif selection == "Bar Plot- Neighbourhood Density":
            sns.barplot(x="neighbourhood_group", y=temp["neighbourhood_group"].index, data=temp).set_title(
                "Neighbourhood Density")
            plt.xlabel("Neighbourhood Groups")

        elif selection == "Bar Plot- N-GROUP - PRICE - ROOM-TYPE":
            sns.barplot(x="neighbourhood_group", y="price", hue="room_type", data=temp).set_title(
                "N-GROUP - PRICE - ROOM-TYPE")
            plt.xlabel("Neighbourhood Groups")
            plt.ylabel("Price")

        elif selection == "Violin-Plot Distribution of Prices by Room Type":
            sns.violinplot(data=temp, x="room_type", y="price").set_title("Distribution of Prices by Room Type")
            plt.ylim(0, 600)
            plt.xlabel("Room Type")
            plt.ylabel("Price")

        elif selection == "Scatter Plot- Price Distribution by Neighborhood Group":
            sns.scatterplot(data=temp, x="neighbourhood_group", y="price").set_title(
                "Price distribution by Neighborhood Group")
            plt.xlabel("Neighbourhood Groups")
            plt.ylabel("Price")

        elif selection == "Line Plot- Change of prices over the years according to room type":
            temp["last_review"] = pd.to_datetime(temp["last_review"])
            temp.set_index("last_review", inplace=True)
            group = temp.groupby(['room_type', pd.Grouper(freq='M')])['price'].mean().reset_index()
            sns.lineplot(data=group, x="last_review", y="price", hue="room_type").set_title(
                "Change of prices over the years according to room type")
            plt.xlabel("Year")
            plt.ylabel("Price")

        elif selection == "Hist Plot- Price Count":
            sns.histplot(temp["price"], kde=True)
            plt.xlim(0, 600)
            plt.xlabel("Price")

        elif selection == "Kde Plot- Price Density":
            sns.kdeplot(temp["price"], shade=True)
            plt.xlim(0, 600)
            plt.xlabel("Price")


        elif selection == "Scatter Plot- Prices by coordinates":
            bins = [0, 100, 200, 300, 400, 500, float('inf')]
            labels = ["0-100", "100-200", "200-300", "300-400", "400-500", "500+"]
            temp["price_group"] = pd.cut(temp["price"], bins=bins, labels=labels, right=False)
            sns.scatterplot(data=temp, x="longitude", y="latitude", hue="price_group", palette="coolwarm")
            plt.title("Prices by coordinates")
            plt.xlabel("Longitude")
            plt.ylabel("Latitude")

        self.canvas.draw()


app = QApplication(sys.argv)
window = Plot()
window.show()
sys.exit(app.exec_())
