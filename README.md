# COMPUTER GRAPHICS (1)
## Programming Assignment No. 1 — QuadTree

**Topic:** QuadTree Data Structure and Visualization

## 1. Project Overview

This project implements an interactive QuadTree data structure for storing, organizing, and visualizing a finite set of two-dimensional points.

The application provides a graphical interface that allows users to insert points, generate random point sets, visualize QuadTree subdivisions, find the path to a selected point, and perform rectangular range queries.

## 2. Application Screenshot

![QuadTree Application](Output.png)

## 3. Technologies Used

- **Programming Language:** Python 3
- **Graphical User Interface:** Tkinter
- **Additional Modules:** Python standard library (`random`)

No external Python packages are required.

## 4. Running the Application

Make sure Python 3 is installed on your computer. Tkinter is normally included with standard Python installations.

Open a terminal in the project folder and execute:

```bash
python main.py
```

The application window will open.

## 5. User Instructions

### 5.1 Drawing Area

The large square on the left side of the application is the drawing area.

Points can be added and selected directly using the mouse. The QuadTree subdivision is updated automatically when new points are inserted.

### 5.2 Control Modes

**Add Points (Click)**

Select this mode and click inside the drawing area to insert a point. All inserted points remain visible until the application is cleared or closed.

**Path to a Point (Click)**

Select this mode and click near an existing point. The application highlights the QuadTree regions from the root node to the leaf containing the selected point.

The corresponding path is also displayed in the information area. The application searches for a point within a distance of 12 pixels from the mouse click.

**Select Rectangle (Drag)**

Select this mode, hold the left mouse button, and drag across the drawing area to create an axis-aligned rectangle R.

Points located inside the rectangle are highlighted, and the information area displays the number of points found.

### 5.3 Application Buttons

- **Generate Random Points:** Inserts 50 points at randomly selected positions inside the drawing area.
- **Clear Area:** Removes all points, resets the QuadTree, and clears the current selection.

## 6. Color Legend

The application uses different colors to distinguish points, selections, and QuadTree regions.

| Color | Meaning |
|---|---|
| Blue | Normal points |
| Orange | Points inside rectangle R |
| Purple | Selected point and path outlines |
| Pink | Selection rectangle R |
| Light Purple | Highlighted QuadTree regions along the selected path |
| Light Cyan | Drawing background and QuadTree grid lines |

## 7. Quadrant Naming Convention

The four child regions of each QuadTree node are named as follows:

```text
       IV | I
      --------
      III | II
```

The quadrant names correspond to these regions:

- **I:** Upper-right
- **II:** Lower-right
- **III:** Lower-left
- **IV:** Upper-left

These names are used when displaying the path from the root node to a selected point.

## 8. Information Area

The information area below the controls displays instructions and results of the current operations, including:

- Number of points in the drawing area.
- Path to the selected point.
- Number of points inside the selected rectangle.
- Short messages describing the current operation.

## 9. Project Structure

```text
QuadTree/
│
├── main.py
├── README.md
└── Output.png
```

## 10. Project Purpose

The purpose of this assignment is to demonstrate the implementation and practical visualization of a QuadTree data structure.

The application provides an interactive way to explore spatial subdivision, point insertion, point searching, and rectangular range queries.

---

**Course:** Computer Graphics (1)  
**Assignment:** Programming Assignment No. 1  
**Topic:** QuadTree