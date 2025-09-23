Funkcjonalności:
Mapa bazowa
Generowana przy użyciu Folium (Python → HTML), osadzana w szablonie Jinja2.
Startowo pokazuje Twoje miasto / region.
Lista POI (points of interest)
Przechowywane w bazie (np. Postgres + PostGIS).
Każdy punkt ma: nazwę, kategorię (np. kawiarnia, park, zabytek), opis, współrzędne.
Dodawanie nowych punktów
Formularz w HTML (bez JS), wysyłający POST do FastAPI.
Po zapisaniu punktu w bazie, mapa generuje się ponownie z nowym markerem.
Filtrowanie / wyszukiwanie
Proste formularze GET – np. wybór kategorii lub szukanie po nazwie.
Wyniki wyświetlane zarówno na liście, jak i zaznaczone na mapie.
Widok szczegółowy POI
Kliknięcie na liście prowadzi do podstrony z opisem + mini mapką skupioną na tym punkcie.

https://ariadnegraphql.org/docs/fastapi-integration
