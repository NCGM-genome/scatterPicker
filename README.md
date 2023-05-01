# scatterPicker

This application allows users to upload a CSV file, display a scatter plot, and interactively select data points. Users can customize the x and y axes and export the selected data points as a new CSV file by clicking the "Export CSV" button.

## Features

- Upload CSV files
- Interactive scatter plot with customizable x and y axes
- Select data points using Box Select or Lasso Select tools
- Export selected data points as a new CSV file

## Installation

1. Clone the repository:
git clone https://github.com/NCGM-genome/scatterPicker.git

2. Change to the project directory:
cd scatterPicker

3. Install the required packages:
pip install -r requirements.txt


## Usage

1. Run the Dash application:
python scatterPicker.py


2. Open your web browser and go to `http://127.0.0.1:8050`.

3. Upload a CSV file by dragging and dropping it onto the designated area or by clicking "Select Files" and choosing the file from your computer.

4. Select the x and y axes from the dropdown menus.

5. Use the Box Select or Lasso Select tools to select data points on the scatter plot.

6. Click the "Export CSV" button to download the selected data points as a new CSV file.

## Customization

You can customize the plot's appearance, such as point colors, sizes, and the style of selected points, by modifying the `create_scatter_plot` function in the `app.py` file. Please refer to the [Plotly Express documentation](https://plotly.com/python/plotly-express/) for more information on customizing the plot.
