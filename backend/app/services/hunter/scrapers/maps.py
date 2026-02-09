"""
Module 9: Local Map Grid Scraping.
Divides a target area into a geo-grid and scrapes ALL businesses in target
categories, bypassing the 60-result limit of Google Maps API.
Finds unlisted warehouses and local distributors.
"""

import os
import time
from typing import List, Dict, Any
from app.services.hunter.scrapers.base import BaseScraper


class MapGridScraper(BaseScraper):
    SOURCE_NAME = "maps_grid"

    LAT_STEP = 0.0045   # ~500m
    LNG_STEP = 0.0045

    def __init__(self, maps_api_key: str = None, **kwargs):
        super().__init__(**kwargs)
        self.maps_key = maps_api_key or os.getenv("GOOGLE_MAPS_API_KEY", "")

    def _get_gmaps_client(self):
        import googlemaps
        return googlemaps.Client(key=self.maps_key)

    def _geocode(self, location: str):
        gmaps = self._get_gmaps_client()
        results = gmaps.geocode(location)
        if results:
            loc = results[0]["geometry"]["location"]
            return loc["lat"], loc["lng"]
        return None, None

    def _generate_grid(self, lat: float, lng: float, radius_km: int) -> List[tuple]:
        steps = int(radius_km * 2)
        points = []
        for i in range(-steps, steps + 1):
            for j in range(-steps, steps + 1):
                points.append((lat + i * self.LAT_STEP, lng + j * self.LNG_STEP))
        return points

    def _fetch_cell(self, gmaps, lat: float, lng: float, keyword: str) -> List[Dict]:
        places = []
        try:
            resp = gmaps.places_nearby(location=(lat, lng), keyword=keyword, radius=500)
            places.extend(resp.get("results", []))
            while "next_page_token" in resp:
                time.sleep(2)
                resp = gmaps.places_nearby(page_token=resp["next_page_token"])
                places.extend(resp.get("results", []))
        except Exception as e:
            print(f"      ⚠ Cell {lat:.4f},{lng:.4f}: {e}")
        return places

    def _enrich_place(self, gmaps, place_id: str) -> Dict:
        """Get extra details (phone, website) from Place Details API."""
        try:
            details = gmaps.place(place_id, fields=[
                "formatted_phone_number", "website", "formatted_address",
                "opening_hours", "business_status",
            ])
            r = details.get("result", {})
            return {
                "phone": r.get("formatted_phone_number"),
                "website": r.get("website"),
                "full_address": r.get("formatted_address"),
                "business_status": r.get("business_status"),
            }
        except Exception:
            return {}

    def execute(self, query: str, location: str, **kwargs) -> List[Dict[str, Any]]:
        if not self.maps_key:
            print("    ⚠ MapsGrid: Missing GOOGLE_MAPS_API_KEY")
            return []

        radius_km = kwargs.get("radius_km", 3)
        enrich = kwargs.get("enrich_details", True)

        print(f"    🗺️  Grid scraping '{query}' in '{location}' (radius={radius_km}km)...")

        lat, lng = self._geocode(location)
        if lat is None:
            print(f"    ❌ Could not geocode: {location}")
            return []

        gmaps = self._get_gmaps_client()
        grid = self._generate_grid(lat, lng, radius_km)
        print(f"      Generated {len(grid)} grid cells")

        all_places: Dict[str, Dict] = {}

        for i, (clat, clng) in enumerate(grid):
            results = self._fetch_cell(gmaps, clat, clng, query)
            for place in results:
                pid = place.get("place_id")
                if pid and pid not in all_places:
                    rating = place.get("rating", 0)
                    total = place.get("user_ratings_total", 0)
                    confidence = (rating / 5) * 100 if rating else 30.0
                    if total > 50:
                        confidence = min(confidence + 10, 100)

                    all_places[pid] = {
                        "name": place.get("name"),
                        "address": place.get("vicinity"),
                        "rating": rating,
                        "total_reviews": total,
                        "types": place.get("types", []),
                        "place_id": pid,
                        "confidence": confidence,
                    }

            time.sleep(0.3)

            if (i + 1) % 25 == 0:
                print(f"      Scanned {i+1}/{len(grid)} cells, found {len(all_places)} unique")

        print(f"      Grid scan complete: {len(all_places)} unique businesses")

        # Enrich top leads with details
        leads = []
        for pid, p in all_places.items():
            extra = {}
            if enrich and len(leads) < 50:
                extra = self._enrich_place(gmaps, pid)
                time.sleep(0.2)

            leads.append(self._base_lead(
                company_name=p["name"],
                formatted_address=extra.get("full_address") or p["address"],
                phone=extra.get("phone"),
                website=extra.get("website"),
                confidence_score=p["confidence"],
                meta_data={
                    "place_id": pid,
                    "rating": p["rating"],
                    "total_reviews": p["total_reviews"],
                    "types": p["types"],
                    "business_status": extra.get("business_status"),
                },
            ))

        print(f"    ✅ MapsGrid: {len(leads)} businesses found")
        return leads
