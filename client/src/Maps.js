import React, { useEffect } from "react";
import { MapContainer, Marker, Popup, TileLayer, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

const icon = L.icon({
  iconUrl: "./placeholder.png",
  iconSize: [38, 38],
});

const position = [51.505, -0.09];

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

function ResetCenterView(props) {
  const { sourcePosition, destPosition} = props;
  const map = useMap();

  useEffect(() => {
    if (sourcePosition && destPosition) {
      // Tạo một mảng chứa tọa độ của cả hai điểm
      const bounds = [
        [sourcePosition.lat, sourcePosition.lon],
        [destPosition.lat, destPosition.lon],
      ];

      // Sử dụng fitBounds để điều chỉnh tầm nhìn đến khoảng giữa cả hai điểm
      map.fitBounds(bounds, { animate: true });
    }
  }, [sourcePosition, destPosition]);
  return null;
}

export default function Maps(props) {
  const { sourcePosition, destPosition, mapRef} = props;
  const sourceLocation = [sourcePosition?.lat, sourcePosition?.lon];
  const destLocation = [destPosition?.lat, destPosition?.lon];

  return (
    <MapContainer
      center={position}
      zoom={8}
      style={{ width: "100%", height: "100%" }}
      whenCreated={(map) => {
        mapRef.current = map; // Lưu tham chiếu đến bản đồ trong mapRef
      }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://api.maptiler.com/maps/streets-v2/256/{z}/{x}/{y}.png?key=AR4n4rVEAJ8meIE8G53B"
      />
      {sourcePosition && (
        <Marker position={sourceLocation} icon={icon}>
          <Popup>Source: {sourcePosition?.display_name}</Popup>
        </Marker>
      )}
      {destPosition && (
        <Marker position={destLocation} icon={icon}>
          <Popup>Destination: {destPosition?.display_name}</Popup>
        </Marker>
      )}
      <ResetView selectPosition={sourcePosition}/>
      <ResetView selectPosition={destPosition}/>
      <ResetCenterView sourcePosition={sourcePosition} destPosition={destPosition} />
    </MapContainer>
  );
}