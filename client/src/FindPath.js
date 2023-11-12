// FindPath.js
import React from "react";
import L from "leaflet";
import Button from "@material-ui/core/Button";

export default function FindPath(props) {
  const { sourceNote, destNote, map} = props;
  var SERVER_URL = "http://localhost:5000";
  console.log(sourceNote,destNote);

  // Hàm vẽ đường lên bản đồ
  const drawPathOnMap = (data) => {
        const latlngs = data.map((point) => {
          console.log("Latitude:", point.lat, "Longitude:", point.lng); // Log the latitude and longitude
          return [point.lat, point.lng];
        });

        const path = L.polyline(latlngs, { color: "blue" }).addTo(map);

        map.fitBounds(path.getBounds());
  };

  const handleFindPath = () => {
    if (sourceNote && destNote) {
      const REST_API = `${SERVER_URL}/calculate?pntdata=${sourceNote},${destNote}`;
      fetch(REST_API)
        .then((response) => response.text())
        .then((data) => {
          console.log("Con đường ngắn nhất:", JSON.parse(data));
          drawPathOnMap(JSON.parse(data)); // Gọi hàm callback để truyền dữ liệu đường đi
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
