# Features

### Base Map
- Generated using **Folium** (Python → HTML), embedded in a **Jinja2** template.
- Initially displays your city/region.

### List of POIs (Points of Interest) DONE
- Stored in a database (e.g., **Postgres + PostGIS**).
- Each point includes:
  - name,
  - category (e.g., café, park, landmark),
  - description,
  - coordinates.

### Adding New Points BACKEND DONE
- HTML form (no JS), sending a **POST** request to **FastAPI**.
- After saving the point to the database, the map is regenerated with the new marker.
- If new point is too close to an existing one, suggest merging it into one

### Filtering / Searching IN PROGRESS
- Simple **GET** forms – e.g., category selection or name search.
- Results are displayed both in a list and marked on the map.

### Detailed POI View
- Clicking on a list item leads to a subpage with a description + a mini map focused on that point.

### Route Mode (Steps: Get route and distance between A-B, suggest points by backed, return editable route)
- Create, display and modify routes between chosen POI (Geoapify or Valhalla)
- Allowing for multiple POI in a route
- Making suggestions of POI on chosen route based on user preferences
- Routes are by default private and can be shared to other users directly via a link
- Rating routes themselves (unsure about need for this functionality, pushed off for later)

### Sending Routes or Objects to Other Users
- Suggesting routes, their modifications, or objects based on similar entries in the database.

### Rating system
- Allowing users to rate routes and points, calculating average rate

### Rating based Points status change
- Based on rating routes or points may be more, or less suggested (becoming private if really low rated)
---

📎 FastAPI integration documentation with Ariadne:
https://ariadnegraphql.org/docs/fastapi-integration
