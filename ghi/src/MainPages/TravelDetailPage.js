import { useSearchParams } from "react-router-dom";
import WeatherChart from "../DataCharts/WeatherChart";
import FlightChart from "../DataCharts/FlightChart";
import CurrencyInfo from "../DataCharts/CurrencyInfo";
import { UserItemForm } from "../PackingListComponents/UserInputItems";
import SuggestedItems from "../PackingListComponents/Items";
import WorkingList from "../PackingListComponents/WorkingList";
import React, { useState, useEffect } from "react";
import "./pages.css";

export default function TravelDetailPage() {
  const [searchParams] = useSearchParams();
  const origin_country = searchParams.get("origin_country");
  const origin_code = searchParams.get("origin_code");
  const destination_city = searchParams.get("destination_city");
  const destination_country = searchParams.get("destination_country");
  const destination_code = searchParams.get("destination_code");
  const departure_date = searchParams.get("departure_date");
  const return_date = searchParams.get("return_date");
  const [items, setItems] = useState([]);

  // Will need to pass the above variable to the corresponding components
  return (
    <div>
      <div className="detail-page-header">
        <h1 className="detail-page-header-text display-4 fw-normal text-center g-5">
          Get ready to pack for {destination_city}, {destination_country}!
        </h1>
        <img src="../luggage_cartoon_v2.png" alt="luggage" className="luggage" />
      </div>
      <div className="container">
        <div className="row">
          <div className="col item-column border rounded">
            <UserItemForm setItems={setItems} items={items} />
            <SuggestedItems setItems={setItems} items={items} />
          </div>
          <div className="col item-column  border rounded">
            <WorkingList setItems={setItems} items={items}
              destination_city={destination_city}
              destination_country={destination_country}
              departure_date={departure_date}
              return_date={return_date}
            />
          </div>
          <div className="col data-column border rounded">
            <div className="row">
              <WeatherChart
                destination_city={destination_city}
                destination_country={destination_country}
                departure_date={departure_date}
                return_date={return_date}
              />
            </div>
            {/* <div className="row">
              <FlightChart />
            </div> */}
            <div className="row currency-data">
              <CurrencyInfo
                origin_code={origin_code}
                destination_code={destination_code}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
