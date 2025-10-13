<h1 align="center">A platform for supporting onshore windfarm siting in Australia</h1>  

Selecting optimal sites for wind farms is complex, involving environmental, social, economic, and technical factors. Traditional GIS maps are static and often do not explain the reasoning behind site selection.

This tool provides an **interactive and explainable interface** for exploring wind farm suitability, understanding trade-offs, and visualizing the impact of different variables.

## Some of the Features
- **Interactive suitability index**: users can assign different weights to key variables and see the map update in real time
- **Pareto optimization**: to identify optimal trade-offs and move along the Pareto frontier
- **A new variable**: to account for wind correlation between potential new sites and existing wind farms

<p align="center">
  
https://github.com/user-attachments/assets/1d2370cc-2cf2-48c7-ad8a-ed5c19da586c

</p>

## Run the Dashboard


```bash
git clone https://github.com/fbizza/XGeoAI
pip install -r requirements.txt
python run_app.py
```
## Documentation and Methodology
A more detailed explanation of the methodology, including variable definitions, is available in the Documentation page within the dashboard itself.
You can access it directly from the dashboard’s main menu once the application is running.
