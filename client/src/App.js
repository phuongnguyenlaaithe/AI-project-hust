import React, { useEffect, useRef, useState} from "react";
import L from "leaflet";
import SearchBox from "./SearchBox";
import Maps from "./Maps";
import FindPath from "./FindPath";

function App() {
  const [sourcePosition, setSourcePosition] = useState(null);
  const [destPosition, setDestPosition] = useState(null);
  const mapRef = useRef(null); // Thêm một tham chiếu đến bản đồ

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "row",
        width: "100vw",
        height: "100vh",
      }}
    >
      <div style={{ width: "30vw", height: "100%" }}>
        <SearchBox
          selectPosition={sourcePosition}
          setSelectPosition={setSourcePosition}
          inputType="source"
        />
        <SearchBox
          selectPosition={destPosition}
          setSelectPosition={setDestPosition}
          inputType="destination"
        />
        <FindPath
        sourcePosition={sourcePosition}
        destPosition={destPosition}
        map={mapRef.current} // Truyền tham chiếu đến bản đồ vào component FindPath
        />
      </div>
      <div style={{ width: "70vw" }}>
        <Maps
          sourcePosition={sourcePosition}
          destPosition={destPosition}
          mapRef={mapRef} // Truyền tham chiếu đến bản đồ vào component Maps
        />
      </div>
    </div>
  );
}

export default App;
