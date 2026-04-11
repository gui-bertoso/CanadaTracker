from __future__ import annotations

from PySide6.QtCharts import (
    QBarCategoryAxis,
    QBarSeries,
    QBarSet,
    QChart,
    QChartView,
    QDateTimeAxis,
    QLineSeries,
    QValueAxis,
)
from PySide6.QtCore import QDateTime, Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget


def _base_chart(title: str) -> QChart:
    chart = QChart()
    chart.setTitle(title)
    chart.setBackgroundVisible(False)
    chart.setMargins(__import__("PySide6.QtCore").QtCore.QMargins(10, 10, 10, 10))
    chart.legend().setVisible(False)
    chart.setTitleBrush(QColor("#e7edf5"))
    chart.setPlotAreaBackgroundVisible(True)
    chart.setPlotAreaBackgroundBrush(QColor("#0d141b"))
    return chart


def line_chart(points: list[tuple[str, float]], title: str, color: str, height: int = 240) -> QChartView:
    chart = _base_chart(title)
    series = QLineSeries()
    series.setColor(QColor(color))
    for day, value in points:
        dt = QDateTime.fromString(f"{day}T00:00:00", Qt.ISODate)
        series.append(dt.toMSecsSinceEpoch(), float(value))
    chart.addSeries(series)
    axis_x = QDateTimeAxis()
    axis_x.setFormat("dd/MM")
    axis_x.setLabelsColor(QColor("#93a2b1"))
    axis_y = QValueAxis()
    axis_y.setLabelsColor(QColor("#93a2b1"))
    axis_y.setGridLineColor(QColor("#22303d"))
    chart.addAxis(axis_x, Qt.AlignBottom)
    chart.addAxis(axis_y, Qt.AlignLeft)
    series.attachAxis(axis_x)
    series.attachAxis(axis_y)
    chart.setPlotAreaBackgroundVisible(False)
    view = QChartView(chart)
    view.setRenderHint(QPainter.Antialiasing)
    view.setMinimumHeight(height)
    view.setMaximumHeight(height)
    view.setStyleSheet("background: #0d141b; border-radius: 12px;")
    return view


def bar_chart(labels: list[str], values: list[float], title: str, color: str, height: int = 240) -> QChartView:
    chart = _base_chart(title)
    bar_set = QBarSet(title)
    bar_set.setColor(QColor(color))
    for value in values:
        bar_set.append(float(value))
    series = QBarSeries()
    series.append(bar_set)
    chart.addSeries(series)
    axis_x = QBarCategoryAxis()
    axis_x.append(labels)
    axis_x.setLabelsColor(QColor("#93a2b1"))
    axis_y = QValueAxis()
    axis_y.setLabelsColor(QColor("#93a2b1"))
    axis_y.setGridLineColor(QColor("#22303d"))
    axis_y.setMin(0)
    axis_y.setMax(max(max(values, default=0), 100))
    chart.addAxis(axis_x, Qt.AlignBottom)
    chart.addAxis(axis_y, Qt.AlignLeft)
    series.attachAxis(axis_x)
    series.attachAxis(axis_y)
    view = QChartView(chart)
    view.setRenderHint(QPainter.Antialiasing)
    view.setMinimumHeight(height)
    view.setMaximumHeight(height)
    view.setStyleSheet("background: #0d141b; border-radius: 12px;")
    return view


def placeholder_chart(title: str, message: str, height: int = 240) -> QWidget:
    widget = QWidget()
    widget.setMinimumHeight(height)
    widget.setMaximumHeight(height)
    widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    widget.setStyleSheet(
        """
        QWidget {
            background: #0d141b;
            border: 1px dashed #2a3947;
            border-radius: 12px;
        }
        QLabel {
            background: transparent;
        }
        """
    )
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(18, 18, 18, 18)
    layout.setSpacing(8)
    title_label = QLabel(title)
    title_label.setStyleSheet("font-size: 15px; font-weight: 700; color: #edf4fb;")
    body_label = QLabel(message)
    body_label.setWordWrap(True)
    body_label.setStyleSheet("color: #8ea0b2;")
    layout.addWidget(title_label)
    layout.addStretch()
    layout.addWidget(body_label, alignment=Qt.AlignCenter)
    layout.addStretch()
    return widget


def multi_line_chart(
    lines: list[dict[str, object]],
    title: str,
    height: int = 240,
    y_max: float | None = None,
) -> QChartView:
    chart = _base_chart(title)
    chart.legend().setVisible(True)
    chart.legend().setLabelColor(QColor("#cfe0ef"))
    max_value = 0.0
    for line in lines:
        series = QLineSeries()
        series.setName(str(line["name"]))
        pen = QPen(QColor(str(line["color"])))
        pen.setWidth(2)
        if line.get("style") == "dashed":
            pen.setStyle(Qt.DashLine)
        series.setPen(pen)
        for day, value in line["points"]:
            dt = QDateTime.fromString(f"{day}T00:00:00", Qt.ISODate)
            series.append(dt.toMSecsSinceEpoch(), float(value))
            max_value = max(max_value, float(value))
        chart.addSeries(series)
    axis_x = QDateTimeAxis()
    axis_x.setFormat("dd/MM")
    axis_x.setLabelsColor(QColor("#93a2b1"))
    axis_y = QValueAxis()
    axis_y.setLabelsColor(QColor("#93a2b1"))
    axis_y.setGridLineColor(QColor("#22303d"))
    axis_y.setMin(0)
    axis_y.setMax(y_max if y_max is not None else max(max_value * 1.1, 10))
    chart.addAxis(axis_x, Qt.AlignBottom)
    chart.addAxis(axis_y, Qt.AlignLeft)
    for series in chart.series():
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)
    view = QChartView(chart)
    view.setRenderHint(QPainter.Antialiasing)
    view.setMinimumHeight(height)
    view.setMaximumHeight(height)
    view.setStyleSheet("background: #0d141b; border-radius: 12px;")
    return view
