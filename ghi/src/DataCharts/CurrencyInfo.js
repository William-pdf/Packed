import React, { useEffect, useState } from "react";
import { loadCurrencyData } from "./LoadApiData";
import "./data.css";

const useCurrencyData = (origin_country, destination_country) => {
  const [currencyRate, setCurrencyRate] = useState(null);

  useEffect(() => {
    async function fetchData() {
      const currency_response = await loadCurrencyData(
        origin_country,
        destination_country
      );
      setCurrencyRate(parseFloat(currency_response));
    }
    fetchData();
  }, [origin_country, destination_country]);

  return currencyRate;
};

export default function CurrencyInfo(props) {
  const { origin_code, destination_code, detailPage } = props;
  const currencyRate = useCurrencyData(origin_code, destination_code);

  const [currencyInput, setCurrencyInput] = useState(1);

  // in case there is a delay in fetching currency data, render Loading...
  if (currencyRate === null) {
    return "Loading...";
  }
  if (origin_code === destination_code) {
    return (
      <h3 id="currency">Looks like your destination uses the same currency!</h3>
    );
  }

  // update exchangeOutput as user changes currencyInput on the browser
  const exchangeOutput = currencyInput / currencyRate;

  const onChangeCurrencyInput = (event) => {
    setCurrencyInput(() => event.target.value);
  };

  return (
    // component layout is different if viewing on Detail Page vs Travel Detail Page
    <div className={!detailPage ? "container-sm" : ""}>
      {!detailPage ? (
        <h3 className="mt-5">Current Exchange Rate</h3>
      ) : (
        <h6>Current Exchange Rate</h6>
      )}
      <input
        onChange={onChangeCurrencyInput}
        value={currencyInput}
        placeholder="1"
        required
        type="text"
        name="currency_input"
        id="currency_input"
        className={
          !detailPage
            ? "currency_input rounded"
            : "currency_input_detail_page rounded"
        }
      />
      <h5 className="currency_output">
        {origin_code} = {exchangeOutput.toFixed(2)} {destination_code}
      </h5>
    </div>
  );
}
