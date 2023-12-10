import React, { useState } from "react";
import OutlinedInput from "@material-ui/core/OutlinedInput";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import Divider from "@material-ui/core/Divider";
import RoomIcon from "@material-ui/icons/Room";
import geojsonData from "./map.json"; // Import GeoJSON data

export default function SearchBox(props) {
  const { selectPosition, setSelectPosition, inputType } = props;

  const [searchText, setSearchText] = useState("");
  const [listPlace, setListPlace] = useState([]);

const filterLocations = (text) => {
  console.log("Filtering with text:", text);
  const filteredLocations = geojsonData.features.filter((feature) => {
    const address = `${feature.properties['addr:housenumber']} ${feature.properties['addr:street']}`;
    return address.toLowerCase().includes(text.toLowerCase());
  });
  console.log("Filtered Locations:", filteredLocations);
  setListPlace(filteredLocations);
};


  return (
    <div style={{ display: "flex", flexDirection: "column" }}>
      <div style={{ display: "flex", alignItems: "center" }}>
        {inputType === "source" && (
          <RoomIcon style={{ marginRight: "10px", color: "green" }} />
        )}
        {inputType === "destination" && (
          <RoomIcon style={{ marginRight: "10px", color: "red" }} />
        )}
        <div style={{ flex: 1 }}>
          <OutlinedInput
            style={{ width: "100%" }}
            value={searchText}
            onChange={(event) => {
              const text = event.target.value;
              setSearchText(text);
              filterLocations(text);
            }}
            placeholder={inputType === "source" ? "From" : "To"}
          />
        </div>
      </div>
      <div>
        <List component="nav" aria-label="main mailbox folders">
        {listPlace.map((feature) => (
  <div key={feature?.properties?.display_name}>
    <ListItem
      button
      onClick={() => {
        setSelectPosition({
          lat: feature.geometry.coordinates[1],
          lon: feature.geometry.coordinates[0],
          display_name: feature.properties.display_name,
        });
        setSearchText(`${feature.properties['addr:housenumber']} ${feature.properties['addr:street']}`);
        setListPlace([]); // Clear the list after selection
      }}
    >
      <ListItemText
        primary={`${feature.properties['addr:housenumber']} ${feature.properties['addr:street']}`}
      />
    </ListItem>
    <Divider />
  </div>
))}
        </List>
      </div>
    </div>
  );
}
