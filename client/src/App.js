import React, { useRef, useState} from "react";
import SearchBox from "./SearchBox";
import Maps from "./Maps";
import FindPath from "./FindPath";

function App() {
  const [sourcePosition, setSourcePosition] = useState(null);
  const [destPosition, setDestPosition] = useState(null);
  const [sourceNote, setSourceNote] = useState("");
  const [destNote, setDestNote] = useState("");
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
          searchText={sourceNote}
          setSearchText={setSourceNote}
        />
        <SearchBox
          selectPosition={destPosition}
          setSelectPosition={setDestPosition}
          searchText={destNote}
          setSearchText={setDestNote}
        />
        <FindPath
        sourceNote={sourceNote}
        destNote={destNote}
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
