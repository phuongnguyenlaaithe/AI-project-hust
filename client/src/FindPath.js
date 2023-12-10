// FindPath.js
import React from "react";
import L from "leaflet";
import Button from "@material-ui/core/Button";

export default function FindPath(props) {
  const { sourcePosition, destPosition, map, path, setPath  } = props;
  var SERVER_URL = "http://localhost:5000";

  // Hàm vẽ đường lên bản đồ
  const drawPathOnMap = (data) => {
        const latlngs = data.map((point) => {
          console.log("Latitude:", point.lat, "Longitude:", point.lng); // Log the latitude and longitude
          return [point.lat, point.lng];
        });

        const pathGroup = L.layerGroup().addTo(map);

        const newPath = L.polyline(latlngs, { color: "blue" }).addTo(pathGroup);
        const sourceToFirst = L.polyline([sourcePosition,  latlngs[latlngs.length - 1]], { dashArray: "5, 5", color: "blue" }).addTo(pathGroup);
        const destToLast = L.polyline([destPosition, latlngs[0]], { dashArray: "5, 5", color: "blue" }).addTo(pathGroup);
        setPath(pathGroup);

        map.fitBounds(pathGroup.getBounds());
  };

  const handleFindPath = () => {
    if (sourcePosition && destPosition) {
      const REST_API = `${SERVER_URL}/calculate?pntdata=${sourcePosition.lat},${sourcePosition.lon},${destPosition.lat},${destPosition.lon}`;
      fetch(REST_API)
        .then((response) => response.text())
        .then((data) => {
          console.log("Con đường ngắn nhất:", JSON.parse(data));
          drawPathOnMap(JSON.parse(data), sourcePosition, destPosition); // Gọi hàm callback để truyền dữ liệu đường đi
        })
        .catch((error) => {
          console.error("Lỗi khi gọi API:", error);
        });
    }
  };

  return(
    <Button variant="contained" color="primary" onClick={handleFindPath}>Find Path</Button>
  );   
}