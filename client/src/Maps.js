import React, { useEffect } from "react";
import { MapContainer, Marker, Popup, TileLayer, useMap, Polyline } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

const iconSource = L.icon({
  iconUrl: "./placeholder2.png",
  iconSize: [38, 38],
});

const iconDes = L.icon({
  iconUrl: "./placeholder1.png",
  iconSize: [38, 38],
});

const position = [51.505, -0.09];

const phanChuTrinhBoundary = [
  [21.024984, 105.860061],
  [21.024729, 105.858314],
  [21.023486, 105.858631],
  [21.023766, 105.857161],
  [21.022534, 105.857252],
  [21.022684, 105.856349],
  [21.022696, 105.855111],
  [21.022111, 105.854936],
  [21.022279, 105.854363],
  [21.021559, 105.854143],
  [21.021455, 105.854631],
  [21.018368, 105.853138],
  [21.018177, 105.854665],
  [21.018903, 105.855795],
  [21.019092, 105.858711],
  [21.018555, 105.861869],
  [21.01946, 105.861713],
  [21.024984, 105.860061],
];

function ResetView(props) {
  const { selectPosition } = props;
  const map = useMap();

  useEffect(() => {
    if (selectPosition) {
      map.setView(
        L.latLng(selectPosition?.lat, selectPosition?.lon),
        map.getZoom(),
        {
          animate: true
        }
      )
    }
  }, [selectPosition]);
  return null;
}

function ResetPath(props) {
  const { path, setPath, sourcePosition, destPosition} = props;
  const map = useMap();

  useEffect(() => {
    if (path) {
      path.removeFrom(map);
      setPath(null);
    }
  }, [sourcePosition, destPosition]);
  return null;
}

function ResetCenterView(props) {
  const { sourcePosition, destPosition} = props;
  const map = useMap();

  useEffect(() => {
    if (sourcePosition && destPosition) {
      const bounds = [
        [sourcePosition.lat, sourcePosition.lon],
        [destPosition.lat, destPosition.lon],
      ];

      map.fitBounds(bounds, { animate: true });
    }
  }, [sourcePosition, destPosition]);

  return null;
}

export default function Maps(props) {
  const { path, setPath, sourcePosition, destPosition, mapRef} = props;
  const sourceLocation = [sourcePosition?.lat, sourcePosition?.lon];
  const destLocation = [destPosition?.lat, destPosition?.lon];

  return (
    <MapContainer
      center={[21.0210957, 105.8579407]}
      zoom={16.6}
      style={{ width: "100%", height: "100%" }}
      whenCreated={(map) => {
        mapRef.current = map;
      }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://api.maptiler.com/maps/streets-v2/256/{z}/{x}/{y}.png?key=AR4n4rVEAJ8meIE8G53B"
      />
      {/* Draw the boundary of Phan Chu Trinh ward */}
      <Polyline positions={phanChuTrinhBoundary} color="red" dashArray="5, 5" />
      
      {sourcePosition && (
        <Marker position={sourceLocation} icon={iconSource}>
          <Popup>Source: {sourcePosition?.display_name}</Popup>
        </Marker>
      )}
      {destPosition && (
        <Marker position={destLocation} icon={iconDes}>
          <Popup>Destination: {destPosition?.display_name}</Popup>
        </Marker>
      )}
      
      <ResetView selectPosition={sourcePosition}/>
      <ResetView selectPosition={destPosition}/>
      <ResetPath path={path} setPath={setPath} sourcePosition={sourcePosition} destPosition={destPosition}/>
      <ResetCenterView sourcePosition={sourcePosition} destPosition={destPosition} />
    </MapContainer>
  );
}
