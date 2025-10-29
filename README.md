# Features

### Base Map
- Generated using **Folium** (Python → HTML), embedded in a **Jinja2** template.
- Initially displays your city/region.

### List of POIs (Points of Interest)
- Stored in a database (e.g., **Postgres + PostGIS**).
- Each point includes:
  - name,
  - category (e.g., café, park, landmark),
  - description,
  - coordinates.

### Adding New Points
- HTML form (no JS), sending a **POST** request to **FastAPI**.
- After saving the point to the database, the map is regenerated with the new marker.

### Filtering / Searching
- Simple **GET** forms – e.g., category selection or name search.
- Results are displayed both in a list and marked on the map.

### Detailed POI View
- Clicking on a list item leads to a subpage with a description + a mini map focused on that point.

### Route Mode
- Create, display and modify routes between chosen POI

### Sending Routes or Objects to Other Users
- Suggesting routes, their modifications, or objects based on similar entries in the database.

---

📎 FastAPI integration documentation with Ariadne:  
https://ariadnegraphql.org/docs/fastapi-integration
