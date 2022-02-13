# 基本的数据分析与可视化

> 有使用到Python3.10独有的match-case语法

可视化使用pyecharts框架

将来可能封装成处理**问卷星直出表格**的工具箱

---

- `core.py` 主要实现了“截存并展示”html单元。支持主流浏览器内核。实现了**多线程**、**多进程**。
- `main.py` 实现了pyecharts的绘图方面的脚手架。目标是让数据分析的主notebook里尽可能少写代码。
- `main_1.ipynb` 是一个应用案例。得益于main种的封装，基本上每个cell都只有一行
- `main_2.ipynb` 是一个应用案例，从txt中读取数据
- `main_3.ipynb` 是一个应用案例
