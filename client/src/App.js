import React, {useRef, useState} from "react";
import SearchBox from "./SearchBox";
import Maps from "./Maps";
import FindPath from "./FindPath";

function App() {
  const [sourcePosition, setSourcePosition] = useState(null);
  const [destPosition, setDestPosition] = useState(null);
  const [path, setPath] = useState(null);
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
        path={path}
        setPath={setPath}
        />
      </div>
      <div style={{ width: "70vw" }}>
        <Maps
          path={path}
          setPath={setPath}
          sourcePosition={sourcePosition}
          setSourcePosition= {setSourcePosition}
          setDestPosition = {setDestPosition}
          destPosition={destPosition}
          mapRef={mapRef} // Truyền tham chiếu đến bản đồ vào component Maps
        />
      </div>
    </div>
  );
}

export default App;