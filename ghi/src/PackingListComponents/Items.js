import React, { useEffect, useState } from "react";
import { loadItemsList } from "./PackingListApi";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlusSquare } from "@fortawesome/free-solid-svg-icons";
import AuthContext from "../context/AuthContext";
import { useContext, useCallback, useMemo } from "react";
function analyzeTemp(tempData) {
  const temperature = tempData[0].temperature;
  if (temperature > 70) {
    return "hot";
  } else if (temperature > 55) {
    return "moderate";
  } else {
    return "cold";
  }
}

export default function SuggestedItems({ setItems, items, temperature }) {

//  Takes 3 parameters to determine the best suggested items for a user.
//  setItems/items is used to pull items from our suggested list to be 
//  rendered to the user. Temperature makes sure only items that fall under
//  specific weather data points are rendered in the conditional items table. 
//  For example we would not want to suggest a heavy coat for a user if weather 
//  data states it will be hot.
  const [conditionalItems, setConditionalItems] = useState([]);
  const [generalItems, setGeneralItems] = useState([]);
  let { authTokens } = useContext(AuthContext);
  const fetchConfig = useMemo(() => {
    const params = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    };
    if (authTokens) {
      params.headers.Authorization = "Bearer " + String(authTokens?.access);
    }
    return params;
  }, [authTokens]);

  const validate = useCallback(() => {
    const tempItems = [...items];
    for (let i = 0; i < tempItems.length; i++) {
      let item = tempItems[i];
      for (let generalItem of generalItems) {
        if (item.name.toLowerCase() === generalItem.name.toLowerCase()) {
          setGeneralItems(
            generalItems.filter(
              (generalItem) =>
                generalItem.name.toLowerCase() !== item.name.toLowerCase()
            )
          );
          item.suggested = true;
          item.id = generalItem.id;
          setItems(tempItems);
        }
      }
      for (let conditionalItem of conditionalItems) {
        if (item.name.toLowerCase() === conditionalItem.name.toLowerCase()) {
          setConditionalItems(
            conditionalItems.filter(
              (conditionalItem) =>
                conditionalItem.name.toLowerCase() !== item.name.toLowerCase()
            )
          );
          item.suggested = true;
          item.id = conditionalItem.id;
          setItems(tempItems);
        }
      }
    }
  }, [generalItems, conditionalItems, items, setItems]);
  validate();

  const fetchData = useCallback(async () => {
    if (temperature) {
      const response = await loadItemsList(
        analyzeTemp(temperature),
        fetchConfig
      );
      const conditional = response.conditional_items.concat(
        response.user_favorite_items
      );
      const general = response.general_items;
      setConditionalItems(conditional);
      setGeneralItems(general);
    }
  }, [fetchConfig, temperature]);
  useEffect(() => {
    fetchData();
  }, [fetchData]);
  function addGItem(newItem) {

//  Takes newItem parameter that allows the user to add
//  an item from our general items suggested list, if the
//  item is already in their packing list it will not be
//  duplicated
    newItem.quantity = 1;
    setItems([...items, newItem]);
    setGeneralItems(generalItems.filter((item) => item.id !== newItem.id));
  }
  function addCItem(newCItem) {

//  Takes newCItem parameter that allows the user to add
//  an item from our conditional items suggested list, if the
//  item is already in their packing list it will not be
//  duplicated
    newCItem.quantity = 1;
    setItems([...items, newCItem]);
    setConditionalItems(
      conditionalItems.filter((item) => item.id !== newCItem.id)
    );
  }
  return (
    <div className="container">
      <h4 className="items-heading">Things you might need</h4>
      <div className="input-group mb-3">
           <table className="table table-hover">
            <thead>
              <tr>
                <th scope="col">General Items To Pack</th>
              </tr>
            </thead>
            <tbody>
            {generalItems.map((item) => {
                return (
                  <tr key={item.name}>
                    <td>{item.name}</td>
                    <td>
                      <button
                        className="btn btn-success btn-sm"
                        onClick={(e) => addGItem(item)}
                      >
                        <FontAwesomeIcon icon={faPlusSquare} />
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          <table className="table table-hover">
            <thead>
              <tr>
                <th scope="col">Recommended For You</th>
              </tr>
            </thead>
            <tbody>
              {conditionalItems.map((item) => {
                return (
                  <tr key={item.name}>
                    <td>{item.name}</td>
                    <td>
                      <button
                        className="btn btn-success btn-sm"
                        onClick={(e) => addCItem(item)}
                      >
                        <FontAwesomeIcon icon={faPlusSquare} />
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
  );
}
